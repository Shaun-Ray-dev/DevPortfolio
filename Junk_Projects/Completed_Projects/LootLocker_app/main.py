from collection import add_item, retrieve_item, get_item_val, get_connection, retrieve_wishlist, add_wishlist_item
from datetime import datetime

def new_item_prompt():
    print("\nEnter item details. Leave blank if unknown.\n")

    item = input("Item name: ").strip()
    category = input("Category: ").strip()

    if not item or not category:
        print("Item name and category are required!")
        return

    subcategory = input("Subcategory: ").strip()
    edition = input("Edition: ").strip()
    brand = input("Brand: ").strip()
    year = input("Year: ").strip()
    condition = input("Condition: ").strip()

    try:
        item_id = add_item(item, category, subcategory, edition, brand, year, condition)
        print(f"\nItem added successfully! (ID: {item_id})\n")

        # --- Fetch market value automatically ---
        print(f"Checking market value for: {item}...")
        value = get_item_val(item)

        if value is not None:
            print(f"Market value found: ${value:.2f}")

            # Update database with value
            try:
                conn = get_connection()
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE collection SET market_value = %s, last_checked = %s WHERE id = %s",
                        (value, datetime.now(), item_id)
                    )
                    conn.commit()
            except Exception as e:
                print(f"Error updating database with market value: {e}")
            finally:
                conn.close()
        else:
            print("Could not fetch a valid market value.")
    except Exception as e:
        print(f"\nError adding item: {e}\n")



def search_item_prompt():
    print("\nEnter search criteria. Leave blank if unknown.\n")

    item = input("Item name: ").strip()
    category = input("Category: ").strip()
    subcategory = input("Subcategory: ").strip()
    edition = input("Edition: ").strip()
    brand = input("Brand: ").strip()
    year = input("Year: ").strip()
    condition = input("Condition: ").strip()

    results = retrieve_item(item, category, subcategory, edition, brand, year, condition)

    if not results:
        print("\nNo matches found.\n")
        return

    print("\nMatching items:\n")
    for row in results:
        item_name = row[1]
        print(f"\nChecking current market value for: {item_name}...")
        value = get_item_val(item_name)

        if value is not None:
            print(f"Current market value: ${value:.2f}")

            # Update database with new market value and timestamp
            try:
                conn = get_connection()
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE collection SET market_value = %s, last_checked = %s WHERE id = %s",
                        (value, datetime.now(), row[0])
                    )
                    conn.commit()
            except Exception as e:
                print(f"Error updating database for {item_name}: {e}")
            finally:
                conn.close()
        else:
            print("Could not fetch a valid price.")

        # Display current DB row info
        print(
            f"ID: {row[0]}, Item: {row[1]}, Category: {row[2]}, "
            f"Subcategory: {row[3]}, Edition: {row[4]}, Brand: {row[5]}, "
            f"Year: {row[6]}, Condition: {row[7]}, Market Value (DB): {row[8]}"
        )



def view_stash():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, item, category, subcategory, edition, brand, year, condition, market_value
                FROM collection
                ORDER BY id;
            """)
            rows = cur.fetchall()

            if not rows:
                print("\nYour stash is empty.\n")
                return

            print("\n=== Your Loot Locker Stash ===\n")
            for row in rows:
                item_id, item_name, category, subcategory, edition, brand, year, condition, market_value = row

                # Refresh market value
                current_value = get_item_val(item_name)
                if current_value is not None:
                    try:
                        cur.execute(
                            "UPDATE collection SET market_value = %s, last_checked = %s WHERE id = %s",
                            (current_value, datetime.now(), item_id)
                        )
                        conn.commit()
                        market_value = current_value
                    except Exception as e:
                        print(f"Error updating value for {item_name}: {e}")

                print(
                    f"ID: {item_id}, Name: {item_name}, Category: {category}, "
                    f"Subcategory: {subcategory}, Edition: {edition}, Brand: {brand}, "
                    f"Year: {year}, Condition: {condition}, Market Value: ${market_value}"
                )

    except Exception as e:
        print(f"Error fetching stash: {e}")
    finally:
        conn.close()



def wishlist_prompt():
    print("\nAdd an item to your Wishlist. Leave blank if unknown.\n")

    item = input("Item name: ").strip()
    category = input("Category: ").strip()

    if not item or not category:
        print("Item name and category are required!")
        return

    subcategory = input("Subcategory: ").strip()
    edition = input("Edition: ").strip()
    brand = input("Brand: ").strip()
    year = input("Year: ").strip()
    condition = input("Condition: ").strip()
    desired_price = input("Desired price (optional): ").strip()

    if desired_price:
        try:
            desired_price = float(desired_price)
        except ValueError:
            print("Invalid price, ignoring.")
            desired_price = None
    else:
        desired_price = None

    try:
        item_id = add_wishlist_item(item, category, subcategory, edition, brand, year, condition, desired_price)
        print(f"\nItem added to wishlist! (ID: {item_id})")

        # fetch current market value
        current_value = get_item_val(item)
        if current_value is not None:
            print(f"Current market value: ${current_value:.2f}")
    except Exception as e:
        print(f"Error adding wishlist item: {e}")



def add_wishlist_item(item, category, subcategory="", edition="", brand="", year="", condition="", desired_price=None):
    """Adds an item to the wishlist table with a timestamp for last_checked"""
    subcategory = subcategory or None
    edition = edition or None
    brand = brand or None
    year = year or None
    condition = condition or None

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO wishlist
                (item, category, subcategory, edition, brand, year, condition, desired_price, last_checked)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (item, category, subcategory, edition, brand, year, condition, desired_price, datetime.now())
            )
            wishlist_id = cur.fetchone()[0]
            conn.commit()
            return wishlist_id
    finally:
        conn.close()



def view_wishlist():
    try:
        results = retrieve_wishlist()

        if not results:
            print("\nYour wishlist is empty.\n")
            return

        print("\n=== Your Wishlist ===\n")
        for row in results:
            item_id, item_name, category, subcategory, edition, brand, year, condition, desired_price, last_checked = row

            # Optionally fetch current market value
            current_value = get_item_val(item_name)
            market_value_display = f"${current_value:.2f}" if current_value else "N/A"

            print(
                f"ID: {item_id}, Name: {item_name}, Category: {category}, "
                f"Subcategory: {subcategory}, Edition: {edition}, Brand: {brand}, "
                f"Year: {year}, Condition: {condition}, "
                f"Desired Price: {desired_price}, Current Market Value: {market_value_display}"
            )

    except Exception as e:
        print(f"Error fetching wishlist: {e}")



def show_menu():
    print("\n=== Loot Locker ===")
    print("1. Add an item.")
    print("2. Search stash by item.")
    print("3. View your stash.")
    print("4. Add to Wishlist.")
    print("5. View your wishlist.")
    print("6. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            new_item_prompt()
        elif choice == "2":
            search_item_prompt()
        elif choice == "3":
            view_stash()
        elif choice == "4":
            wishlist_prompt()
        elif choice == "5":
            view_wishlist()    
        elif choice == "6":
            print("Exiting Loot Locker. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main()
