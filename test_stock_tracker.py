from stock_tracker import StockTracker

import random
stock_tracker = StockTracker()
ids = random.sample(range(1, 1000001), 10000)
prices = [random.uniform(1, 100) for _ in range(10000)]
operations = []

# 10,000 insert-new-stock
for i in range(10000):
    operations.append(f"insert-new-stock {ids[i]} {prices[i]}")

# 10,000 update-price, 10,000 increase-volume, with price-range and max-vol
price_count = 0
vol_count = 0
last_price = None
for i in range(10000):
    # Update price
    new_price = random.uniform(1, 100)
    operations.append(f"update-price {ids[i]} {new_price}")
    price_count += 1
    last_price = new_price
    if price_count % 1000 == 0:
        operations.append(f"price-range {last_price} {last_price + 2}")
    
    # Increase volume
    vinc = random.randint(1, 100)
    operations.append(f"increase-volume {ids[i]} {vinc}")
    vol_count += 1
    if vol_count % 100 == 0:
        operations.append("max-vol")

# 10,000 lookup-by-id
for i in range(10000):
    operations.append(f"lookup-by-id {ids[i]}")

# Write operations
with open("test_result.txt", "w") as f:
    for op in operations:
        f.write(op + "\n")