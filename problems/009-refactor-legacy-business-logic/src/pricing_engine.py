def calculate_price(plan, users, coupon=None, renewing=False):
    price = 0
    if plan == "free": price = 0
    elif plan == "starter": price = 19
    elif plan == "pro": price = 49
    elif plan == "enterprise": price = 199
    else: raise ValueError("bad plan")
    if users > 1 and plan != "free": price = price + ((users - 1) * 5)
    if coupon == "SAVE10": price = price * 0.9
    if coupon == "HALF": price = price * 0.5
    if renewing and plan in ("pro", "enterprise"): price = price * 0.95
    return round(price, 2)
