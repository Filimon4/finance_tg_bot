import requests

API_CONFIG = {
    "exchange_rates": {
        "access_key": "99243e221ad236b1ed453be5b215a5ad",
        "url": "http://apilayer.net/api/live",
        "default_currencies": "EUR,GBP,CAD,PLN",
        "source_currency": "USD"
    },
    "crypto": {
        "url": "https://api.coinlore.net/api/tickers/"
    }
}

class CurrencyAPI:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrencyAPI, cls).__new__(cls)
            # Инициализация конфигурации
            cls.exchange_config = API_CONFIG["exchange_rates"]
            cls.crypto_config = API_CONFIG["crypto"]
        return cls._instance

    def _make_api_request(self, url, params=None):
        """Общий метод для выполнения API-запросов"""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Проверка на ошибки HTTP
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса к {url}: {e}")
            return None
        except ValueError as e:
            print(f"Ошибка при обработке JSON из {url}: {e}")
            return None

    def get_exchange_rates(self, currencies=None):
        """Получение курсов валют"""
        if currencies is None:
            currencies = self.exchange_config["default_currencies"]

        params = {
            "access_key": self.exchange_config["access_key"],
            "currencies": currencies,
            "source": self.exchange_config["source_currency"],
            "format": 1
        }

        data = self._make_api_request(self.exchange_config["url"], params)
        if not data:
            return []

        mass_valuti = []
        if data.get("success"):
            quotes = data.get("quotes", {})
            print("Актуальные курсы валют:")
            for currency_pair, rate in quotes.items():
                target_currency = currency_pair[3:]
                mass_valuti.append(f"{self.exchange_config['source_currency']} = {rate} {target_currency}")
        else:
            print("Ошибка при получении данных:")
            print(data.get("error", {}).get("info", "Неизвестная ошибка"))

        print(f"ВАЛЮТЫ: {mass_valuti}")
        return mass_valuti

    def get_crypto_rates(self, limit=10):
        """Получение курсов криптовалют"""
        data = self._make_api_request(self.crypto_config["url"])
        if not data or "data" not in data:
            return []

        btc_mass = []
        for coin in data["data"][:limit]:
            btc_mass.append(f"{coin['name']} ({coin['symbol']}): ${coin['price_usd']}")

        print(f"КРИПТОВАЛЮТЫ: {btc_mass}")
        return btc_mass