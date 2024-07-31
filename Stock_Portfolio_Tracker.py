import requests
import json


API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'
BASE_URL = 'https://www.alphavantage.co/query'


portfolio = {}


def fetch_stock_price(symbol):

    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    try:

        latest_time = list(data['Time Series (1min)'].keys())[0]
        latest_data = data['Time Series (1min)'][latest_time]
        return float(latest_data['1. open'])
    except KeyError:
        print(f"Error fetching data for {symbol}. Please check the symbol and try again.")
        return None


def add_stock(symbol, amount):

    if symbol in portfolio:
        portfolio[symbol] += amount
    else:
        portfolio[symbol] = amount
    print(f"Added {amount} shares of {symbol} to the portfolio.")


def remove_stock(symbol, amount):

    if symbol in portfolio:
        if portfolio[symbol] >= amount:
            portfolio[symbol] -= amount
            if portfolio[symbol] == 0:
                del portfolio[symbol]
            print(f"Removed {amount} shares of {symbol} from the portfolio.")
        else:
            print(f"Not enough shares of {symbol} to remove.")
    else:
        print(f"Stock {symbol} not found in portfolio.")


def track_portfolio():

    total_value = 0
    print("\nPortfolio Performance:")
    for symbol, amount in portfolio.items():
        price = fetch_stock_price(symbol)
        if price is not None:
            value = price * amount
            total_value += value
            print(f"{symbol}: {amount} shares @ ${price:.2f} each, Total value: ${value:.2f}")

    print(f"\nTotal Portfolio Value: ${total_value:.2f}")


def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Track Portfolio")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            amount = int(input("Enter number of shares: "))
            add_stock(symbol, amount)
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            amount = int(input("Enter number of shares to remove: "))
            remove_stock(symbol, amount)
        elif choice == '3':
            track_portfolio()
        elif choice == '4':
            print("Exiting the tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
