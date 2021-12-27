import requests


gecko_base_url = "https://api.coingecko.com/api/v3/"

DEFAULT_IDS = ['bitcoin', 'ethereum', 'solana']
def get_coin_price(id=None):
    """looks up price of crypto"""
    if not id:
        id = ",".join(DEFAULT_IDS)
    url = gecko_base_url+f"/simple/price?ids={id}&vs_currencies=usd&include_market_cap=true&include_24hr_change=true"
    response = requests.get(url)
    if response.status_code == 200:
        json = response.json()

        return json
    else:
        print(f"Something went wrong getting coin price: {print(response.content)}")
        return None


def get_crypto_digest():
    """Gets coin prices and formats the text"""
    coin_data = get_coin_price()
    digest = ""

    for item in coin_data:
        print(item)
        price = coin_data[item].get("usd")
        digest += f"Price of {item} -> ${price}\n"

    print(digest)
    return digest





if __name__ == "__main__":
    print("running locally")
    print(get_crypto_digest())
