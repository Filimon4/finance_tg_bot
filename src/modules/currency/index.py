from enum import Enum
import requests

class CurrencyEnum(Enum):
    currency_api = 'currency_api',
    coin_market = 'coin_market'

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
    base_currencies = ['EUR','USD','CHF','RUB','JPY','GBP'],

    def __init__(self):
        super().__init__()

    def get_all(self):
        currencies = ",".join(self.base_currencies)

        params = {}
        params["currencies"] = currencies

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
            print(f"Ошибка при выполнении запроса к {url}: {e}")
            return None
        except requests.HTTPError as e:
            print(f"HTTP ошибка при запросе к {url}: {e}")
            return None
        except requests.JSONDecodeError as e:
            print(f"Ошибка при обработке JSON из {url}: {e}")
            return None
        except requests.Timeout as e:
            print(f"Таймаут при запросе к {url}: {e}")
            return None
        
    def get_status(self):
        url = f"{self.url}/status"
        data = self._make_api_request(url)
        return data

class ThirdCoinMarkerAPI(BaseCurrencyAPI):
    api_key = "65054a26-7950-4765-9d8c-4bdcb2c1050b",
    url = "https://pro-api.coinmarketcap.com",
    base_currencies = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'ADA'],

    def get_rates(self):
        url = f"{self.url}/v2/cryptocurrency/quotes/latest"
        currencies_rates = {}

        for currency in self.base_currencies:
            params = {
                'symbol': currency,
                'convert': ",".join(filter(lambda x: x != currency, self.base_currencies))
            }

            rates = self._make_api_request(url, params)

            if not rates or not rates.get('data'):
                continue

            currencies_rates[currency] = {
                'data': rates['data'][currency]['quote'],
                'base': currency
            }
        return currencies_rates

    def get_all(self):
        url = f"{self.url}/v1/cryptocurrency/map"
        
        params = {
            'listing_status': 'active',
            'limit': 3500,  # Максимальное количество по API
            'symbol': ','.join(self.base_currencies)
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
            print(f"Ошибка при выполнении запроса к {url}: {e}")
            return None
        except requests.HTTPError as e:
            print(f"HTTP ошибка при запросе к {url}: {e}")
            return None
        except requests.JSONDecodeError as e:
            print(f"Ошибка при обработке JSON из {url}: {e}")
            return None
        except requests.Timeout as e:
            print(f"Таймаут при запросе к {url}: {e}")
            return None
        
    def get_status(self):
        url = f"{self.url}/v1/key/info"
        data = self._make_api_request(url)
        
        print(data)
        if not data:
            return {
                'status': 'error',
                'message': 'Unable to connect to CoinMarketCap API'
            }
        
        return {
            'status': 'success',
            'plan': data.get('data', {}).get('plan', {}),
            'usage': data.get('data', {}).get('usage', {}),
            'timestamp': data.get('status', {}).get('timestamp')
        }

class CurrencyStrategies(BaseCurrencyAPI):
    def __init__(self):
        super().__init__()
        objectPool = dict()
        objectPool[CurrencyEnum.currency_api] = ThirdCurrencyAPI()
        objectPool[CurrencyEnum.coin_market] = ThirdCoinMarkerAPI()

        self.objectPool = objectPool

    def get_all(self, type: CurrencyEnum):
        pass
    
    def get_rates(self, type: CurrencyEnum):
        pass
    
    def get_status(self, type: CurrencyEnum):
        pass
    

CurrencyManager = CurrencyStrategies()