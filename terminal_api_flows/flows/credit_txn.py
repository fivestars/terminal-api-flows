import json
import uuid

from terminal_api_flows import print_outcome, generate_ids, http_request, get_customers
from terminal_api_flows.tools.decorators import terminal_ping_decorator_3_attempts


CARD_DECLINE_STATUSES = [
    "DECLINED_ERROR",
    "DECLINED_ERROR_DIP_MSG",
    "DECLINED_ERROR_SWIPE_MSG",
    "PAYMENT_GENERAL_ERROR",
    "PAYMENT_GENERAL_DIP_MSG",
    "PAYMENT_GENERAL_SWIPE_MSG",
    "DIP_READ_ERROR",
    "DIP_READ_ERROR_MSG",
    "SWIPE_READ_ERROR",
    "SWIPE_READ_ERROR_MSG",
    "NFC_READ_ERROR",
    "NFC_DECLINE_ERROR_MSG",
    "NFC_GENERAL_ERROR_MSG",
]


def handle_switch_to_cash_flow(status):
    if status in CARD_DECLINE_STATUSES:
        print(f"Credit Card Status: {status}")
        res, json_data = http_request(
            f"checkouts", "PUT",
            json.dumps({"checkout": {"type": "CASH"}}).encode("utf-8")
        )
        print_outcome("SWITCHED_TO_CASH", res.status, json_data)
        exit(0)


# *********************** #
# Credit Transaction Flow #
# *********************** #

@terminal_ping_decorator_3_attempts
def credit_to_cash_transaction(total=0):
    json_data, discount = get_customers()

    pos_checkout_id, pos_order_id, customer_uid = generate_ids(json_data)

    checkout_data = {
        "checkout": {
            "pos_checkout_id": pos_checkout_id,
            "type": "CREDIT",
            "total": total,
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

        status = json_data["status"]

        if status == "SUCCESSFUL":
            print_outcome("SUCCESS", res.status, json_data)
            exit(0)

        print(f"Transaction Status: {status}")

        handle_switch_to_cash_flow(status)

        while status != "SUCCESSFUL":
            res, json_data = http_request(f"checkouts/{pos_checkout_id}", "GET")
            status = json_data["status"]
            if status == "CANCELED_BY_CUSTOMER":
                print_outcome("CANCELED_BY_CUSTOMER", res.status, json_data)
                exit(0)
            handle_switch_to_cash_flow(status)
            print_outcome("SUCCESS", res.status, json_data)
    else:
        print_outcome("FAILED", res.status, json_data)


@terminal_ping_decorator_3_attempts
def credit_transaction(total=0):
    json_data, discount = get_customers()

    pos_checkout_id, pos_order_id, customer_uid = generate_ids(json_data)

    checkout_data = {
        "checkout": {
            "pos_checkout_id": pos_checkout_id,
            "type": "CREDIT",
            "total": total,
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

        status = json_data["status"]

        if status == "SUCCESSFUL":
            print_outcome("SUCCESS", res.status, json_data)
            exit(0)

        print(f"Transaction Status: {status}")

        while status != "SUCCESSFUL":
            res, json_data = http_request(f"checkouts/{pos_checkout_id}", "GET")
            if status == "CANCELED_BY_CUSTOMER":
                print_outcome("CANCELED_BY_CUSTOMER", res.status, json_data)
                exit(0)
            print_outcome("SUCCESS", res.status, json_data)
    else:
        print_outcome("FAILED", res.status, json_data)


# *********************** #
# Credit Transaction Flow #
# *********************** #

@terminal_ping_decorator_3_attempts
def verify_cpay_1567():
    checkout_data = {
        "checkout": {
            "pos_checkout_id": uuid.uuid4().__str__(),
            "type": "CREDIT",
            "total": 800,
            "customer_account_uid": uuid.uuid4().__str__(),
            "discounts_applied": []
        },
        "order": {
            "currency": "USD",
            "pos_order_id": uuid.uuid4().__str__(),
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

    if res.status == 200:
        status = json_data["status"]

        if status == "PRIOR_TRANSACTION_ALREADY_IN_PROGRESS":
            print_outcome("FAILED, ISSUE CPAY-1567 STILL EXISTS", res.status, json_data)
            exit(0)

        print_outcome("SUCCESS", res.status)
    else:
        print_outcome("FAILED", res.status, json_data)
