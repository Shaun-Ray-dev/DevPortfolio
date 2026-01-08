import requests
from bs4 import BeautifulSoup
import time

def get_item_val(item_name):
    """
    Scrapes PriceCharting for item value.
    Returns a float if found, None otherwise.
    """
    try:
        search_url = f"https://www.pricecharting.com/search-products?q={item_name.replace(' ', '+')}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        for attempt in range(3):
            try:
                response = requests.get(search_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    break
                else:
                    print(f"Attempt {attempt+1} returned status {response.status_code}")
            except requests.RequestException as e:
                print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
        else:
            print(f"Failed to fetch data for {item_name} after 3 attempts.")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        selectors = [
            ".price.js-price",
            ".price",
            ".value",
            ".price-value",
            "td:nth-of-type(3)",
        ]

        for selector in selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                price_txt = price_elem.get_text(strip=True).replace("\xa0", "").replace("$", "").replace(",", "")
                try:
                    return float(price_txt)
                except ValueError:
                    continue

        print(f"No price found for {item_name}.")
        return None

    except Exception as e:
        print(f"Error fetching item value for {item_name}: {e}")
        return None