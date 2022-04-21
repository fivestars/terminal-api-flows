import json

from terminal_api_flows import print_outcome, generate_ids, http_request, get_customers

# *********************** #
# Credit Transaction Flow #
# *********************** #
def credit_transaction():
    json_data, discount = get_customers()

    pos_checkout_id, pos_order_id, customer_uid = generate_ids(json_data)

    checkout_data = {
        "checkout": {
            "pos_checkout_id": pos_checkout_id,
            "type": "CREDIT",
            "total": 800,
            "customer_account_uid": customer_uid,
            "discounts_applied": discount
        },
        "order": {
            "currency": "USD",
            "pos_order_id": pos_order_id,
            "products": [
                {
                    "name": "hamburger",
                    "price": 250,
                    "price_with_vat": 0,
                    "quantity": 2,
                    "receipt_nest_level": 1,
                    "single_vat_amount": 0,
                    "total_price": 500,
                    "total_with_vat": 0,
                    "vat_rate": 0,
                    "vat_amount": 0
                }
            ],
            "subtotal": 0,
            "tax": 125
        }
    }

    # POST to checkouts
    res, json_data = http_request("checkouts", "POST", json.dumps(checkout_data).encode("utf-8"))

    if res.status == 200 and json_data["status"] == "TRANSACTION_STARTED":
        res, json_data = http_request(f"checkouts/{pos_checkout_id}", "GET")

        status =  json_data["status"]

        if status == "SUCCESSFUL":
            print_outcome("SUCCESS", res.status, json_data)
            exit(0)

        print(f"Transaction Status: {status}")

        while  status != "SUCCESSFUL":
            res, json_data = http_request(f"checkouts/{pos_checkout_id}", "GET")
            print_outcome("SUCCESS", res.status, json_data)
    else:
        print_outcome("FAILED", res.status, json_data)
