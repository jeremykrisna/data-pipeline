import requests

BASE_URL = "https://dummyjson.com"

def fetch_products():
    try:
        url = f"{BASE_URL}/products"
        response = requests.get(
            url,
            timeout=30,
            #for bypass ssl certificate for testing api public
            verify=False
        )
        response.raise_for_status()
        print("Request successful")
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Request failed:", str(e))
        raise