import asyncio
import logging
from typing import Optional
from src.modules.currency.index import CurrencyEnum, CurrencyManager
from src.modules.currency.currencyRepository import CurrencyRepository
from src.db.index import DB
from sqlalchemy.exc import SQLAlchemyError
from asyncio.log import logger

class CurrencySystem:
    def __init__(self):
      self._loop = asyncio.new_event_loop()
      self._fetch_interval = 604800
      self._task: Optional[asyncio.Task] = None
      self._stop_event = asyncio.Event()

    def _setup_scheduler(self):
      if not self._task or self._task.done():
            self._task = asyncio.create_task(self._run_periodically())

    async def _run_periodically(self):
      with DB.get_session() as session:
        CurrencyRepository.clear()
        CurrencyRepository.load(session)
      while not self._stop_event.is_set():
          await asyncio.sleep(self._fetch_interval)
          try:
              await self.updateAllApi()
          except Exception as e:
              logging.error(f"ReminderSystem error: {e}")

    def updateAllApi(self):
      logger.info('-- CurrencySystem: updateAllApi')
      self.updateCurrencies()
      self.updateRates()

    def updateRates(self):
      for api in CurrencyEnum.get_list():
        logger.info(f'-- CurrencySystem: update Rates for {api}')
        self.updateApiRates(api)

    def updateCurrencies(self):
      for api in CurrencyEnum.get_list():
        logger.info(f'-- CurrencySystem: update Currencies for {api}')
        self.updateApiCurrencies(api)

    def getApiStatus(self, api):
      return CurrencyManager.get_status(api)

    def updateApiCurrencies(self, api):
      with DB.get_session() as session:
        apiCurrencies = CurrencyManager.get_all(api)
        currenciesKeys = list(dict(apiCurrencies).keys())
        for currency in currenciesKeys:
          try:
            data = apiCurrencies[currency]
            symbol = data['symbol']
            name = data['name']
            CurrencyRepository.getOrCreateCurrency(session, symbol, name, name, symbol)
          except SQLAlchemyError as e:
            logger.error(f"{str(e)}")
        session.commit()
        # Обновление кэша
        CurrencyRepository.clear()
        CurrencyRepository.load(session)

    def updateApiRates(self, api):
      with DB.get_session() as session:
        apiRates = CurrencyManager.get_rates(api)
        apiRatesKeys = list(dict(apiRates).keys())
        for currency in apiRatesKeys:
          try:
            data = apiRates[currency]
            base = data['base']
            rates = data['data']
            CurrencyRepository.syncCurrencyRates(session, base, rates)
          except SQLAlchemyError as e:
            logger.error(f"{str(e)}")
        session.commit()
        # Обновление кэша
        CurrencyRepository.clear()
        CurrencyRepository.load(session)

CurrencySys = CurrencySystem()