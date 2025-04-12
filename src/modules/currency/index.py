import requests

API_CONFIG = {
    "currencyapi": {
        "access_key": "cur_live_D0hTJNbg79DzKONmXYXzEwvVb7YaftpRYM6cExQe",
        "url": "https://api.currencyapi.com/v3",
        
        "currencies": "EUR,USD,CHF,RUB,JPY,GBP",
        
        "base_currency_header": "base_currency",
        "currencies_header": "currencies",
        "api_key_header": "apikey",
        
        "api_getall": "/currencies",
        "api_rates": "/latest",
        "status": "/status",
    },
}

class CurrencyAPI:
    def __init__(self, config: str):
        self.config = API_CONFIG[config]

    def _make_api_request(self, url, params=None):
        try:
            headers = {}
            headers[self.config["api_key_header"]] = self.config["access_key"]
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

    def get_all(self):
        currencies = self.config["currencies"]

        params = {}
        params[self.config["currencies_header"]] = currencies

        url = f"{self.config['url']}{self.config['api_getall']}"

        data = self._make_api_request(url, params)
        if not data or not data['data']:
            return []

        return data['data']

    def get_rates(self):
        url = f"{self.config['url']}{self.config['api_rates']}"
        all_currencies = self.config["currencies"].split(',')
        currencies_rates = {}

        for currency in all_currencies:
            params = {}
            params[self.config["base_currency_header"]] = currency
            
            params[self.config["currencies_header"]] = ",".join(filter(lambda x: x != currency, all_currencies))
            print(params)

            rates = self._make_api_request(url, params)

            if not rates or not rates['data']:
                continue
            currencies_rates[currency] = {
                'data': rates['data'],
                'base': currency
            }
        return currencies_rates
    
    def get_status(self):
        url = f"{self.config['url']}{self.config['status']}"
        data = self._make_api_request(url)
        return data
