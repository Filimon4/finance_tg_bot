import os
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy import create_engine, URL
from typing import ClassVar, Type
from dotenv import load_dotenv

load_dotenv()

class DBSinglton:
    """
    Общая обёртка над базой данных
    """

    url_object = URL.create(
        "postgresql",
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT"),
    )

    session: ClassVar[Type[Session]]

    def __init__(self):
        print("--- BD")
        try:
            self.engine = create_engine(DBSinglton.url_object)
            self.session = sessionmaker(bind=self.engine)()
        except Exception as e:
            print("Ошибка подключения ", e)

    def checkСonnection(self):
        """
        Проверка подключения к базе данных
        """
        try:
            with self.engine.connect() as connection:
                print("Подключение к базе данных успешно установлено!")
                return True
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def getSession(self):
        return self.session


DB = DBSinglton()


class Base(DeclarativeBase):
    """
    Обёртка над DeclarativeBase. Применять ко всем моделям бд
    """

    pass


Base.metadata.create_all(DB.engine)
