import os
import time
from typing import ClassVar, Type, Optional
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from pybreaker import CircuitBreaker, CircuitBreakerError
import logging
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', verbose=True, override=True)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DBCircuitBreaker:
    """
    Circuit Breaker для отслеживания состояния базы данных
    """
    def __init__(self):
        self.breaker = CircuitBreaker(
            fail_max=3,
            reset_timeout=30,
            name="Database Circuit Breaker"
        )

class DBSingleton:
    """
    Общая обёртка над базой данных с Circuit Breaker и повторными попытками
    """
    _instance = None
    _breaker = DBCircuitBreaker()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        logger.info("--- Initializing DB connection")
        
        # Проверка переменных окружения
        required_vars = ["DB_USERNAME", "DB_PASSWORD", "DB_HOST", "DB_NAME", "DB_PORT"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

        self.url_object = URL.create(
            "postgresql",
            username=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT"),
        )
        
        self.engine = None
        self.session_factory = None
        self._connect()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(OperationalError),
    )
    def _connect(self):
        """Попытка подключения с повторными попытками"""
        try:
            logger.info("Attempting to connect to DB")
            self.engine = create_engine(self.url_object, connect_args={"connect_timeout": 5})
            logger.info(f"DB URL: {self.engine.url}")
            
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.session_factory = sessionmaker(bind=self.engine)
            logger.info("Successfully connected to DB")
            
        except OperationalError as e:
            logger.error(f"Operational error during connection: {e}")
            raise
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error during connection: {e}")
            raise

    @property
    def circuit_state(self):
        """Текущее состояние Circuit Breaker"""
        return {
            "state": self._breaker.breaker.current_state,
            "fail_counter": self._breaker.breaker.fail_counter,
            "ready": not self._breaker.breaker.opened
        }

    def _execute_with_circuit_breaker(self, operation, *args, **kwargs):
        """Выполнение операции с защитой Circuit Breaker"""
        try:
            return self._breaker.breaker.call(operation, *args, **kwargs)
        except CircuitBreakerError as e:
            logger.error(f"Circuit breaker is open: {e}")
            raise ConnectionError("Database is temporarily unavailable due to too many errors") from e
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise ConnectionError(f"Database operation failed: {e}") from e

    def check_connection(self):
        """
        Проверка подключения к базе данных с использованием Circuit Breaker
        :raises: ConnectionError если подключение отсутствует
        """
        def _check():
            if self.engine is None:
                raise ConnectionError("Database connection is not initialized")
                
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("Database connection is active")
            return True

        return self._execute_with_circuit_breaker(_check)

    def get_session(self) -> Session:
        """
        Возвращает новую сессию базы данных
        :raises: ConnectionError если подключение отсутствует
        """
        def _get_session():
            if self.session_factory is None:
                raise ConnectionError("Database session factory is not initialized")
            return self.session_factory()

        return self._execute_with_circuit_breaker(_get_session)

    def close(self):
        """Закрытие соединений с БД"""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.session_factory = None
        logger.info("Database connections closed")

class Base(DeclarativeBase):
    """
    Обёртка над DeclarativeBase. Применять ко всем моделям бд
    """
    pass

DB = None
try:
    DB = DBSingleton()
    if DB.engine:
        Base.metadata.create_all(DB.engine)
        logger.info("Database tables verified/created successfully")
except (SQLAlchemyError, ConnectionError) as e:
    logger.error(f"FATAL: Failed to initialize database connection: {str(e)}")
    raise