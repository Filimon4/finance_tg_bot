from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from decimal import Decimal
from datetime import datetime

from db.index import DB
from db.models import Currency, ExchangeRate
from modules.currency.index import CurrencyAPI

class CurrencyRepository:
    @staticmethod
    def sync_currency_rates(session: Session):
        """Основной метод для синхронизации данных из API с базой данных"""
        api = CurrencyAPI()
        
        # Получаем данные из API
        exchange_rates = api.get_exchange_rates()
        crypto_rates = api.get_crypto_rates()
        
        # Обрабатываем фиатные валюты
        for rate_str in exchange_rates:
            parts = rate_str.split()
            from_currency = parts[0]  # USD
            rate_value = Decimal(parts[2])
            to_currency = parts[3]   # EUR, GBP и т.д.
            
            # Получаем или создаем валюты в таблице Currency
            from_currency_obj = CurrencyRepository._get_or_create_currency(
                session, from_currency, f"{from_currency} Dollar")
            
            to_currency_obj = CurrencyRepository._get_or_create_currency(
                session, to_currency, f"{to_currency} Currency")
            
            # Создаем запись в ExchangeRate
            CurrencyRepository._create_exchange_rate(
                session, 
                from_currency_obj.id, 
                to_currency_obj.id, 
                rate_value
            )
        
        # Обрабатываем криптовалюты (пример для BTC, ETH и т.д.)
        for crypto_str in crypto_rates:
            parts = crypto_str.split()
            symbol = parts[1][1:-1]  # Получаем символ из (BTC)
            name = parts[0]          # Bitcoin
            price = Decimal(parts[2][1:])  # Цена без $
            
            # Создаем криптовалюту
            crypto_obj = CurrencyRepository._get_or_create_currency(
                session, symbol, name, is_crypto=True)
            
            # Для криптовалют сохраняем курс к USD
            usd_obj = CurrencyRepository._get_or_create_currency(
                session, "USD", "US Dollar")
            
            CurrencyRepository._create_exchange_rate(
                session, 
                usd_obj.id, 
                crypto_obj.id, 
                price
            )
        
        session.commit()

    @staticmethod
    def _get_or_create_currency(session: Session, code: str, name: str, is_crypto: bool = False) -> Currency:
        """Вспомогательный метод для получения или создания валюты"""
        currency = session.query(Currency).filter(
            or_(
                Currency.code == code,
                Currency.name == name
            )
        ).first()
        
        if not currency:
            currency = Currency(
                code=code,
                name=f"{name} ({'Crypto' if is_crypto else 'Fiat'})",
            )
            session.add(currency)
            session.flush()
        
        return currency

    @staticmethod
    def _create_exchange_rate(session: Session, from_currency_id: int, to_currency_id: int, rate: Decimal):
        """Вспомогательный метод для создания записи о курсе"""
        # Проверяем, есть ли уже такой курс
        existing_rate = session.query(ExchangeRate).filter(
            ExchangeRate.from_currency_id == from_currency_id,
            ExchangeRate.to_currency_id == to_currency_id
        ).order_by(ExchangeRate.created_at.desc()).first()
        
        # Если курс изменился или его не было - создаем новый
        if not existing_rate or existing_rate.rate != rate:
            new_rate = ExchangeRate(
                from_currency_id=from_currency_id,
                to_currency_id=to_currency_id,
                rate=rate
            )
            session.add(new_rate)

    @staticmethod
    def get_latest_rates(session: Session, base_currency_code: str = "USD"):
        """Получение последних курсов для указанной базовой валюты"""
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
    
