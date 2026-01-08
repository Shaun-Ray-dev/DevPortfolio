import psycopg
import requests
from bs4 import BeautifulSoup
from datetime import datetime



LL_Database = {
    "dbname" : "loot_locker",
    "user" : "loot_user",
    "password" : "loot_pass",
    "host" : "127.0.0.1",
    "port" : 5432 
}



def get_connection():
 
    return psycopg.connect(**LL_Database)


def add_item (item,  category, subcategory="", edition="", brand="", year="", condition=""):
    #Adds new item 

    subcategory = subcategory or None
    edition = edition or None
    brand = brand or None
    year = year or None
    condition = condition or None

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO collection (item, category, subcategory, edition, brand, year, condition, market_value)
                           VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                           RETURNING id;""",
                           (item, category, subcategory, edition, brand, year, condition, None))
            item_id = cur.fetchone()[0]
            conn.commit()
            return item_id
    finally:
        conn.close()
        


def retrieve_item (item="", category="", subcategory="", edition="", brand="", year="", condition=""):
    #Searches collection table 
    item = item or None
    category = category or None
    subcategory = subcategory or None
    edition = edition or None
    brand = brand or None
    year = year or None
    condition = condition or None

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM collection WHERE TRUE"
            params = []

            if item:
                query += " AND item ILIKE %s"
                params.append(f"%{item}%")
            if category:
                query += " AND category ILIKE %s"
                params.append(f"%{category}%")
            if subcategory:
                query += " AND subcategory ILIKE %s"
                params.append(f"%{subcategory}%")
            if edition:
                query += " AND edition ILIKE %s"
                params.append(f"%{edition}%")
            if brand:
                query += " AND brand ILIKE %s"
                params.append(f"%{brand}%")
            if year:
                query += " AND year = %s"
                params.append(year)
            if condition:
                query += " AND condition ILIKE %s"
                params.append(f"%{condition}%")

            cur.execute(query, tuple(params))
            results = cur.fetchall()
            return results
    finally:
        conn.close()



def get_item_val(item_name):
    # Scrapes PriceCharting for item value, returns None if none found
    try:
        search_url = f"https://www.pricecharting.com/search-products?q={item_name.replace(' ', '+')}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        import time

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
    
def add_wishlist_item(item, category, subcategory="", edition="", brand="", year="", condition="", desired_price=None):
    """Adds an item to the wishlist table with a timestamp for last_checked"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO wishlist
                (item, category, subcategory, edition, brand, year, condition, desired_price, last_checked)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING id;
            """, (item, category, subcategory or None, edition or None, brand or None, year or None, condition or None, desired_price, datetime.now()))
            item_id = cur.fetchone()[0]
            conn.commit()
            return item_id
    finally:
        conn.close()


def retrieve_wishlist(item="", category="", subcategory="", edition="", brand="", year="", condition=""):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM wishlist WHERE TRUE"
            params = []

            if item: 
                query += " AND item ILIKE %s"
                params.append(f"%{item}%")
            if category:
                query += " AND category ILIKE %s"
                params.append(f"%{category}%")
            if subcategory:
                query += " AND subcategory ILIKE %s"
                params.append(f"%{subcategory}%")
            if edition:
                query += " AND edition ILIKE %s"
                params.append(f"%{edition}%")
            if brand:
                query += " AND brand ILIKE %s"
                params.append(f"%{brand}%")
            if year:
                query += " AND year = %s"
                params.append(year)
            if condition:
                query += " AND condition ILIKE %s"
                params.append(f"%{condition}%")

            cur.execute(query, tuple(params))
            return cur.fetchall()
    finally:
        conn.close()
