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
    def update(cls, session: Session):
        cls._loaded = False
        cls.load(session)

    @classmethod
    def getCurrencyByCode(cls, code):
        return cls._currencies.get(code)

    @classmethod
    def getRate(cls, from_id, to_id):
        return cls._exchange_rates.get((from_id, to_id))

    @classmethod
    def clear(cls):
        cls._loaded = False
        cls._currencies = {}
        cls._exchange_rates = {}

    #region Queries

    @staticmethod
    def syncCurrencyRates(session: Session, base: str, rates: List[Dict[str, str]]):
        try:
            rateKeys = list(dict(rates).keys())
            for rateKey in rateKeys:
                rate = rates[rateKey]
                code_currency = rate['code']
                rate_value = rate['value']
                CurrencyRepository.updateOrCreateCurrencyRate(
                    session,
                    base,
                    code_currency,
                    rate_value
                )
                CurrencyRepository.checkRatesLinks(session)
        except SQLAlchemyError as e:
            logger.error(f"Database SQLAlchemyError: {str(e)}")


    @staticmethod
    def getCurrencyRate(session: Session, base_id, to_currency_id):
        currency_rate = session.query(ExchangeRate).filter(ExchangeRate.from_currency_id == base_id, ExchangeRate.to_currency_id == to_currency_id).first()

        if not currency_rate:
            return None
        
        return {
            'rate': float(currency_rate.rate),
            'updated_at': currency_rate.created_at
        }

    @staticmethod
    def getOrCreateCurrency(session: Session, symbol: str, code: str, name: str, symbol_native: str) -> Currency:
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
    def updateOrCreateCurrencyRate(session: Session, base: str, code: str, rate: Decimal):
        try:
            base_currency = session.query(Currency).filter(Currency.symbol == base).first()
            to_currency = session.query(Currency).filter(Currency.symbol == code).first()

            if not base_currency or not to_currency or base_currency.id == to_currency.id:
                return
            
            exist_to_rate = session.query(ExchangeRate).filter(
                ExchangeRate.from_currency_id == base_currency.id,
                ExchangeRate.to_currency_id == to_currency.id
            ).first()

            exist_from_rate = session.query(ExchangeRate).filter(
                ExchangeRate.from_currency_id == to_currency.id,
                ExchangeRate.to_currency_id == base_currency.id
            ).first()
        
            if exist_to_rate:
                if exist_to_rate.rate != rate:
                    exist_to_rate.rate = rate
                    session.flush()
            else:
                CurrencyRepository.createRate(session, base_currency.id, to_currency.id, rate)

            reversed_rate = round(1/rate, 8)
            if exist_from_rate:
                if exist_from_rate.rate != reversed_rate:
                    exist_from_rate.rate = reversed_rate
                    session.flush()
            else:
                CurrencyRepository.createRate(session, to_currency.id, base_currency.id, reversed_rate)    

            session.commit()
        except SQLAlchemyError as e:
            logger.error(f"{str(e)}")

    @staticmethod
    def createRate(session: Session, base_id: int, curr_id: int, rate: int) -> ExchangeRate :
        try:
            new_rate = ExchangeRate(
                from_currency_id=base_id,
                to_currency_id=curr_id,
                rate=rate
            )
            session.add(new_rate)
            session.commit()
            return new_rate
        except SQLAlchemyError as e:
            raise Exception(str(e))

    @staticmethod
    def getCurrencyRates(session: Session, base_currency_code: str):
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
    def getCurrentRates(session: Session, currency_id: int):
        rates = session.query(ExchangeRate).filter(
            ExchangeRate.from_currency_id == currency_id
        ).all()
        return [{
            'from_currency_id': int(rate.from_currency_id),
            'to_currency_id': int(rate.to_currency_id),
            'rate': float(rate.rate),
            'updated_at': str(rate.created_at)
        } for rate in rates]
    
    @staticmethod
    def getAll(session: Session):
        try:
            return session.query(Currency).all()
        except SQLAlchemyError as e:
            raise Exception(e)
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def checkRatesLinks(session: Session):
        try:
            currencies = CurrencyRepository.getAll(session)
            usd_currency = next((c for c in currencies if c.symbol == "USD"), None)
            if not usd_currency:
                raise Exception("Cannot find base USD currency")

            for curr in currencies:
                existRates = CurrencyRepository.getCurrentRates(session, curr.id)
                usdPair = next(
                    (r for r in existRates if int(r["to_currency_id"]) == usd_currency.id),
                    None
                )
                if not usdPair:
                    logger.error(f"No USD pair found for {curr.symbol}")
                    continue

                unExistCurrencyPairs: List[Currency] = [
                    cmp_currency for cmp_currency in currencies
                    if curr.id != cmp_currency.id and not any(
                        r["to_currency_id"] == cmp_currency.id for r in existRates
                    )
                ]
                if not unExistCurrencyPairs or len(unExistCurrencyPairs) == 0:
                    logger.error(f"All pairs exist for {curr.symbol}")
                    continue

                for unExistPair in unExistCurrencyPairs:
                    pairToUsd = CurrencyRepository.getCurrencyRate(
                        session, unExistPair.id, usd_currency.id
                    )
                    if not pairToUsd:
                        continue
                    try:
                        currencyToUsdRate = Decimal(str(usdPair["rate"]))
                        unExistToUsdRate = Decimal(str(pairToUsd["rate"]))
                        newRate = round(currencyToUsdRate / unExistToUsdRate, 8)
                        CurrencyRepository.createRate(session, curr.id, unExistPair.id, newRate)
                    except (ZeroDivisionError, ValueError) as e:
                        logger.error(f"Failed to calculate rate for {curr.symbol}/{unExistPair.symbol}: {e}")
                        continue
            session.commit() 
        except SQLAlchemyError as e:
            raise Exception(e)
        except Exception as e:
            raise Exception(e) 
    
