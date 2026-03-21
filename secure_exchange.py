import os
import ccxt
from dotenv import load_dotenv

class LocalExchangeWrapper:
    def __init__(self, exchange_id='binance'):
        """
        Initializes the exchange connection strictly using local environment variables.
        Ensures API keys are never hardcoded.
        """
        # Load local .env file securely
        load_dotenv()
        
        api_key = os.getenv('BINANCE_API_KEY')
        secret_key = os.getenv('BINANCE_SECRET_KEY')
        
        if not api_key or not secret_key:
            raise EnvironmentError("[SECURITY FATAL] Local API keys not found in .env file. Execution halted.")

        # Initialize CCXT exchange class dynamically
        exchange_class = getattr(ccxt, exchange_id)
        
        self.exchange = exchange_class({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
        })
        
        print(f"[SYSTEM] Secure local connection to {self.exchange.name} initialized.")

    def fetch_local_balance(self, ticker='USDT'):
        """
        Safely fetches the balance of a specific asset.
        """
        try:
            balance = self.exchange.fetch_balance()
            free_balance = balance.get(ticker, {}).get('free', 0.0)
            return free_balance
        except ccxt.NetworkError as e:
            print(f"[NETWORK ERROR] Could not connect to exchange: {e}")
        except ccxt.ExchangeError as e:
            print(f"[EXCHANGE ERROR] Authentication failed or invalid keys: {e}")
        
        return None

if __name__ == "__main__":
    # Initialize the secure wrapper
    # Note: This will fail safely if you haven't set up your local .env file
    try:
        wrapper = LocalExchangeWrapper()
        usdt_balance = wrapper.fetch_local_balance('USDT')
        
        if usdt_balance is not None:
            print(f"[EXECUTION] Available Local Balance: {usdt_balance} USDT")
            
    except EnvironmentError as e:
        print(e)
