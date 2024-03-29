import json
import time
import uuid

from terminal_api_flows import print_outcome, generate_ids, http_request, get_customers
from terminal_api_flows.tools.decorators import terminal_ping_decorator_3_attempts
from terminal_api_flows import skip_screen


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


# *********************** #
# Credit Transaction Flow #
# *********************** #

@terminal_ping_decorator_3_attempts
def credit_to_cash_transaction(total=0, skip_tip=False, skip_reward_notification=False, allow_discount=True):
    json_data, discount = get_customers(allow_discount=allow_discount)

    pos_checkout_id, pos_order_id, customer_uid = generate_ids(json_data)

    checkout_data = {
        "checkout": {
            "pos_checkout_id": pos_checkout_id,
            "type": "CREDIT",
            "total": total,
            "customer_account_uid": customer_uid,
            "discounts_applied": discount,
            "skip_tip": skip_tip,
            "skip_reward_notification": skip_reward_notification,
            "skip_signin": False

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
def credit_transaction(
        total=0,
        skip_tip=False,
        skip_reward_notification=False,
        skip_signin=False,
        allow_discount=True,
        # Skip screens in real time if they come up
        skip_tips_screen=False,
        skip_reward_notification_screen=False,
        skip_approval_screen=False
    ):
    json_data, discount = get_customers(skip_signin=skip_signin, allow_discount=allow_discount)

    pos_checkout_id, pos_order_id, customer_uid = generate_ids(json_data)

    checkout_data = {
        "checkout": {
            "pos_checkout_id": pos_checkout_id,
            "type": "CREDIT",
            "total": total,
            "customer_account_uid": customer_uid,
            "discounts_applied": discount,
            "skip_tip": skip_tip,
            "skip_reward_notification": skip_reward_notification,
            "skip_signin": skip_signin
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

        # Potential here to skip the current screen
        # This has to be checked here and in the following loop as the screens can show up right away
        # once the transaction has kicked off and depending on the customer termainal's settings.
        if skip_tips_screen and status == "SCREEN_TIPS" or \
            skip_approval_screen and status == "SCREEN_APPROVAL" or \
            skip_reward_notification_screen and status == "SCREEN_REWARD_NOTIFICATION":
            skip_screen()

        while status != "SUCCESSFUL":
            res, json_data = http_request(f"checkouts/{pos_checkout_id}", "GET")
            status = json_data["status"]
            print(f"Transaction Status: {status}")

            if status == "CANCELED_BY_CUSTOMER":
                print_outcome("CANCELED_BY_CUSTOMER", res.status, json_data)
                exit(0)
            if status in CARD_DECLINE_STATUSES:
                print(f"Problem with payment: {status}")
                # Backoff a bit, wait for the customer to try another card
                time.sleep(3)
            # Potential here to skip the current screen
            # This has to be checked here and in the following loop as the screens can show up right away
            # once the transaction has kicked off and depending on the customer termainal's settings.
            if skip_tips_screen and status == "SCREEN_TIPS" or \
                skip_approval_screen and status == "SCREEN_APPROVAL" or \
                skip_reward_notification_screen and status == "SCREEN_REWARD_NOTIFICATION":
                skip_screen()

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
