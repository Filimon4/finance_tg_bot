from asyncio.log import logger
from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal

from src.db.models import Currency, ExchangeRate
from sqlalchemy.exc import SQLAlchemyError

class CurrencyRepository:
    #region Cache
    _currencies = {}
    _exchange_rates = {}
    _loaded = False

    @classmethod
    def load(cls, session: Session):
        if not cls._loaded:
            cls._currencies = {
                c.code: c for c in session.query(Currency).all()
            }
            cls._exchange_rates = {
                (r.from_currency_id, r.to_currency_id): r
                for r in session.query(ExchangeRate).all()
            }
            cls._loaded = True

    @classmethod
    def get_currency_by_code(cls, code):
        return cls._currencies.get(code)

    @classmethod
    def get_rate(cls, from_id, to_id):
        return cls._exchange_rates.get((from_id, to_id))

    @classmethod
    def clear(cls):
        cls._loaded = False
        cls._currencies = {}
        cls._exchange_rates = {}

    #region Queries

    @staticmethod
    def sync_currency_rates(session: Session, base: str, rates: List[Dict[str, str]]):
        try:
            rateKeys = list(dict(rates).keys())
            for rateKey in rateKeys:
                rate = rates[rateKey]
                code_currency = rate['code']
                rate_value = rate['value']
                CurrencyRepository.update_or_create_currency_rate(
                    session,
                    base,
                    code_currency,
                    rate_value
                )
        except SQLAlchemyError as e:
            logger.error(f"Database SQLAlchemyError: {str(e)}")


    @staticmethod
    def get_currency_rate(session: Session, base_id, to_currency_id):
        currency_rate = session.query(ExchangeRate).filter(ExchangeRate.from_currency_id == base_id, ExchangeRate.to_currency_id == to_currency_id).first()

        if not currency_rate:
            return None
        
        return {
            'rate': float(currency_rate.rate),
            'updated_at': currency_rate.created_at
        }

    @staticmethod
    def get_or_create_currency(session: Session, symbol: str, code: str, name: str, symbol_native: str) -> Currency:
        currency = session.query(Currency).filter(Currency.code == code).first()
        if not currency:
            currency = Currency(
                code=code,
                name=name,
                symbol=symbol,
                symbol_native=symbol_native
            )
            session.add(currency)
            session.commit()
        return currency

    @staticmethod
    def update_or_create_currency_rate(session: Session, base: str, code: str, rate: Decimal):
        try:
            base_currency = session.query(Currency).filter(Currency.symbol == base).first()
            to_currency = session.query(Currency).filter(Currency.symbol == code).first()

            if not base_currency or not to_currency or base_currency.id == to_currency.id:
                return
            
            existing_rate = session.query(ExchangeRate).filter(
                ExchangeRate.from_currency_id == base_currency.id,
                ExchangeRate.to_currency_id == to_currency.id
            ).order_by(ExchangeRate.created_at.desc()).first()
        
            if existing_rate:
                if existing_rate.rate != rate:
                    existing_rate.rate = rate
                    session.commit()
            else:
                new_rate = ExchangeRate(
                    from_currency_id=base_currency.id,
                    to_currency_id=to_currency.id,
                    rate=rate
                )
                session.add(new_rate)
        except SQLAlchemyError as e:
            logger.error(f"{str(e)}")

    @staticmethod
    def create_exchange_rate(session: Session, from_currency_id: int, to_currency_id: int, rate: Decimal):
        existing_rate = session.query(ExchangeRate).filter(
            ExchangeRate.from_currency_id == from_currency_id,
            ExchangeRate.to_currency_id == to_currency_id
        ).order_by(ExchangeRate.created_at.desc()).first()
        
        if not existing_rate or existing_rate.rate != rate:
            new_rate = ExchangeRate(
                from_currency_id=from_currency_id,
                to_currency_id=to_currency_id,
                rate=rate
            )
            session.add(new_rate)

    @staticmethod
    def get_currency_rates(session: Session, base_currency_code: str):
        rates = session.query(ExchangeRate).join(
            Currency,
            ExchangeRate.to_currency_id == Currency.id
        ).filter(Currency.code == base_currency_code).all()
        return [{
            'from_currency': rate.from_currency.code,
            'to_currency': rate.to_currency.code,
            'rate': float(rate.rate),
            'updated_at': rate.created_at
        } for rate in rates]

    @staticmethod
    def get_latest_rates(session: Session, base_currency_code: str = "USD"):
        base_currency = session.query(Currency).filter(
            Currency.code == base_currency_code
        ).first()
        
        if not base_currency:
            return []
        
        subquery = session.query(
            ExchangeRate.to_currency_id,
            func.max(ExchangeRate.created_at).label('max_date')
        ).filter(
            ExchangeRate.from_currency_id == base_currency.id
        ).group_by(
            ExchangeRate.to_currency_id
        ).subquery()
        
        rates = session.query(ExchangeRate, Currency.code, Currency.name).join(
            subquery,
            (ExchangeRate.to_currency_id == subquery.c.to_currency_id) &
            (ExchangeRate.created_at == subquery.c.max_date)
        ).join(
            Currency,
            ExchangeRate.to_currency_id == Currency.id
        ).filter(
            ExchangeRate.from_currency_id == base_currency.id
        ).all()
        
        return [{
            'from_currency': base_currency.code,
            'to_currency': code,
            'to_currency_name': currency_name,
            'rate': float(rate.rate),
            'updated_at': rate.created_at
        } for rate, code, currency_name in rates]
    
