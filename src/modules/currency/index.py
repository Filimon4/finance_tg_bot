from asyncio.log import logger
from enum import Enum
import requests

class CurrencyEnum(Enum):
    currency_api: str = 'currency_api'
    coin_market: str = 'coin_market'

    @staticmethod
    def get_list():
        return [item.value for item in CurrencyEnum]
    
    @staticmethod
    def get_list_string():
        return ",".join([item.value for item in CurrencyEnum])

class BaseCurrencyAPI:
    def __init__(self):
        pass 

    def get_all(self):
        pass

    def get_rates(self):
        pass

    def get_status(self):
        pass

class ThirdCurrencyAPI(BaseCurrencyAPI):
    api_key = "cur_live_D0hTJNbg79DzKONmXYXzEwvVb7YaftpRYM6cExQe"
    url = "https://api.currencyapi.com/v3"
    base_currencies = ['EUR','USD','CHF','RUB','JPY','GBP']

    def __init__(self):
        super().__init__()

    def get_all(self):
        currencies = ",".join(self.base_currencies)

        params = {
            "currencies": currencies
        }

        url = f"{self.url}/currencies"
        data = self._make_api_request(url, params)
        if not data or not data['data']:
            return []

        return data['data']
    
    def get_rates(self):
        url = f"{self.url}/latest"
        currencies_rates = {}

        for currency in self.base_currencies:
            params = {}
            params['base_currency'] = currency
            params['currencies'] = ",".join(filter(lambda x: x != currency, self.base_currencies))

            rates = self._make_api_request(url, params)

            if not rates or not rates['data']:
                continue
            currencies_rates[currency] = {
                'data': rates['data'],
                'base': currency
            }
        return currencies_rates
    
    def _make_api_request(self, url, params):
        try:
            headers = {}
            headers['apikey'] = self.api_key
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Ошибка при выполнении запроса к {str(url)}: {str(e)}")
            return None
        except requests.HTTPError as e:
            logger.error(f"HTTP ошибка при запросе к {str(url)}: {str(e)}")
            return None
        except requests.JSONDecodeError as e:
            logger.error(f"Ошибка при обработке JSON из {str(url)}: {str(e)}")
            return None
        except requests.Timeout as e:
            logger.error(f"Таймаут при запросе к {str(url)}: {str(e)}")
            return None
        
    def get_status(self):
        url = f"{self.url}/status"
        data = self._make_api_request(url, {})
        result = {
            'active': False
        }
        quotas = data.get('quotas', {})

        if not data or not quotas:
            return result
        
        if 'month' in quotas:
            monthData = quotas['month'] 
            logger.error(f"{str(monthData)}")
            result['month'] = monthData
            if monthData['remaining'] > 0:
                result['active'] = True
            else:
                result['active'] = False

        return self._format_currency_api_status(result)
    
    def _format_currency_api_status(self, data):
        if not data or not data.get('active'):
            return "💱 Статус currency_api: неактивен ❌"

        month = data.get('month', {})
        total = month.get('total', '—')
        used = month.get('used', '—')
        remaining = month.get('remaining', '—')

        message = (
            f"💱 Статус currency_api: активен ✅\n\n"
            f"📊 Лимит на месяц:\n"
            f"• Всего запросов: {total}\n"
            f"• Использовано: {used}\n"
            f"• Осталось: {remaining}"
        )

        return message


class ThirdCoinMarkerAPI(BaseCurrencyAPI):
    api_key = "65054a26-7950-4765-9d8c-4bdcb2c1050b"
    url = "https://pro-api.coinmarketcap.com"
    base_currencies = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'ADA']
    currencies_ids = {
        "BTC": 1,
        "ETH": 1027,
        "BNB": 1839,
        "XRP": 52,
        "SOL": 5426,
        "ADA": 2010
    }

    def get_rates(self):
        url = f"{self.url}/v2/cryptocurrency/quotes/latest"
        currencies_rates = {}
        curr_ids_string = ",".join(list(map(lambda x: str(self.currencies_ids[x]), self.base_currencies)))
        params = {
            'id': curr_ids_string
        }
        rates = self._make_api_request(url, params)
        dataKeys = list(rates['data'].keys())
        for key in dataKeys:
            curr_data = rates['data'][key]
            symbol = curr_data['symbol']
            quote = curr_data['quote']
            quote_key = list(quote.keys())
            needed_data = {}
            for q_key in quote_key:
                needed_data[q_key] = {
                    'code': q_key,
                    'value': float(quote[q_key]['price']),
                }
            currencies_rates[symbol] = {
                'data': needed_data,
                'base': symbol
            }
        return currencies_rates

    def get_all(self):
        curr_ids_string = ",".join(list(map(lambda x: str(self.currencies_ids[x]), self.base_currencies)))
        url = f"{self.url}/v2/cryptocurrency/info"
        params = {
            'id': curr_ids_string
        }
        data = self._make_api_request(url, params)
        if not data or not data.get('data'):
            return []
        return data['data']

    def _make_api_request(self, url, params):
        if params is None:
            params = {}
        try:
            headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': self.api_key
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Ошибка при выполнении запроса к {str(url)}: {str(e)}")
            return None
        except requests.HTTPError as e:
            logger.error(f"HTTP ошибка при запросе к {str(url)}: {str(e)}")
            return None
        except requests.JSONDecodeError as e:
            logger.error(f"Ошибка при обработке JSON из {str(url)}: {str(e)}")
            return None
        except requests.Timeout as e:
            logger.error(f"Таймаут при запросе к {str(url)}: {str(e)}")
            return None
        
    def get_status(self):
        url = f"{self.url}/v1/key/info"
        data = self._make_api_request(url, {})
        
        result = {
            'active': False
        }

        if not data:
            return result

        if 'status' in data:
            result['timestamp'] = data.get('status', {}).get('timestamp')

        if 'plan' in data.get('data', {}):
            result['plan'] = data['data']['plan']
        
        if 'usage' in data.get('data', {}):
            result['usage'] = data['data']['usage']
            
            credits_left = data['data']['usage'].get('current_month', {}).get('credits_left')
            if credits_left is not None and credits_left <= 0:
                result['active'] = False
            else:
                result['active'] = True
        
        return self._format_status_message(result)
    
    def _format_status_message(self, data):
        if not data or not data.get('active'):
            return "🔐 Статус ключа: неактивен ❌"

        timestamp = data.get('timestamp', '—')
        plan = data.get('plan', {})
        usage = data.get('usage', {})

        plan_text = (
            f"💳 Тарифный план:\n"
            f"• Месячный лимит кредитов: {plan.get('credit_limit_monthly', '—')}\n"
            f"• Сброс лимита через: {plan.get('credit_limit_monthly_reset', '—')}\n"
            f"• Дата сброса: {plan.get('credit_limit_monthly_reset_timestamp', '—')}\n"
            f"• Лимит запросов в минуту: {plan.get('rate_limit_minute', '—')}"
        )

        usage_text = (
            f"📊 Использование:\n"
            f"🔁 Текущая минута:\n"
            f"  • Запросов сделано: {usage.get('current_minute', {}).get('requests_made', '—')}\n"
            f"  • Осталось запросов: {usage.get('current_minute', {}).get('requests_left', '—')}\n"
            f"📅 Сегодня:\n"
            f"  • Кредитов использовано: {usage.get('current_day', {}).get('credits_used', '—')}\n"
            f"🗓 Этот месяц:\n"
            f"  • Кредитов использовано: {usage.get('current_month', {}).get('credits_used', '—')}\n"
            f"  • Осталось кредитов: {usage.get('current_month', {}).get('credits_left', '—')}"
        )

        message = (
            f"🔐 Статус ключа: активен ✅\n\n"
            f"⏱ Время запроса:\n{timestamp}\n\n"
            f"{plan_text}\n\n"
            f"{usage_text}"
        )

        return message

class CurrencyStrategies(BaseCurrencyAPI):
    def __init__(self):
        super().__init__()
        objectPool = dict()
        objectPool[CurrencyEnum.currency_api.value] = ThirdCurrencyAPI()
        objectPool[CurrencyEnum.coin_market.value] = ThirdCoinMarkerAPI()

        self.objectPool = objectPool

    def get_all(self, type: CurrencyEnum):
        if not self.objectPool[type]:
            raise ValueError(f"Invalid currency type: {type}")
        return self.objectPool[type].get_all()
    
    def get_rates(self, type: CurrencyEnum):
        if not self.objectPool[type]:
            raise ValueError(f"Invalid currency type: {type}")
        return self.objectPool[type].get_rates()
    
    def get_status(self, type: CurrencyEnum):
        if not self.objectPool[type]:
            raise ValueError(f"Invalid currency type: {type}")
        return self.objectPool[type].get_status()

CurrencyManager = CurrencyStrategies()