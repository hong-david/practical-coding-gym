TAX_RATE = 0.10

def process_order(order, inventory):
    subtotal = 0
    for item in order.get("items", []):
        sku = item["sku"]
        qty = item.get("quantity", 1)
        if inventory.get(sku, 0) <= 0:
            raise ValueError("out of stock")
        subtotal += item["unit_price"] * qty
        inventory[sku] = inventory.get(sku, 0) - 1
    discount = order.get("discount", 0)
    if discount:
        subtotal = subtotal - discount
    tax = subtotal * TAX_RATE
    return {"subtotal": subtotal, "tax": tax, "total": subtotal + tax}

def refund_order(order, inventory):
    for item in order.get("items", []):
        inventory[item["sku"]] = inventory.get(item["sku"], 0) + 1
    return True
