def summarize_orders(orders):
    total = 0
    customers = {}
    for order in orders:
        order["total"] = order.get("quantity", 1) * order.get("price", 0)
        if order.get("status") == "cancelled":
            continue
        total += order["total"]
        customer = order.get("customer", "unknown")
        if customer not in customers:
            customers[customer] = 0
        customers[customer] += order["total"]
    return {"total": total, "customers": customers, "count": len(orders)}
