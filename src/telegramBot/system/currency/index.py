import asyncio
import logging
from typing import Optional
import schedule
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
      while not self._stop_event.is_set():
          try:
              await self.updateAllApi()  # Ваш метод для обработки напоминаний
          except Exception as e:
              logging.error(f"ReminderSystem error: {e}")
          await asyncio.sleep(self._fetch_interval)

    def updateAllApi(self):
      logger.info('-- CurrencySystem: updateAllApi')
      self.updateCurrencies()
      self.updateRates()

    def updateRates(self):
      for api in CurrencyEnum.get_list():
        self.updateApiRates(api)

    def updateCurrencies(self):
      for api in CurrencyEnum.get_list():
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
            CurrencyRepository.get_or_create_currency(session, symbol, name, name, symbol)
          except SQLAlchemyError as e:
            print(e)
        session.commit()

    def updateApiRates(self, api):
      with DB.get_session() as session:
        apiRates = CurrencyManager.get_rates(api)
        apiRatesKeys = list(dict(apiRates).keys())
        for currency in apiRatesKeys:
          try:
            data = apiRates[currency]
            base = data['base']
            rates = data['data']
            CurrencyRepository.sync_currency_rates(session, base, rates)
          except SQLAlchemyError as e:
            print(e)
        session.commit()
    
CurrencySys = CurrencySystem()