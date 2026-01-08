from collection import get_item_val

test_items = ["Mega Man X SNES", "Amazing Fantasy #15 comic book", "Non Value"]

for item in test_items:
    print(f"Test: {item}")
    val = get_item_val(item)
    print(f"Result: {val}\n")