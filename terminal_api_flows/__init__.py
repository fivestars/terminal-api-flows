import json
import uuid
import urllib3


HTTP = urllib3.PoolManager(timeout=160)
# Adjust these as needed
TERMINAL_ID = " --> TERMINAL ID HERE <--- "
BEARER_TOKEN = " --> BEARER-TOKEN-HERE <--"
SOFTWARE_ID = " --> SOFTWARE-ID <--"
BASE_URL = f"https://edge.nerfstars.com/terminal-api/v1/terminals/{TERMINAL_ID}/"
# This is your unique POS ID
POS_ID = "123"


def print_outcome(failed, status_code, json_data=None):
    print("--------------------------------------")
    print(f"Flow Outcome: {failed}")
    print(f"Status Code: {status_code}")
    print("--------------------------------------")
    if json_data:
        print(json_data)


def generate_ids(json_data):
    pos_checkout_id = uuid.uuid4().__str__()
    pos_order_id = uuid.uuid4().__str__()
    customer_uid = json_data["customer"]["uid"]

    return pos_checkout_id, pos_order_id, customer_uid


def http_request(endpoint, action, json_body="") -> (urllib3.HTTPResponse, dict):
    http_request = HTTP.request(
        action,
        f"{BASE_URL}{endpoint}",
        headers={
            "pos-id": f"{POS_ID}",
            "software-id": f"{SOFTWARE_ID}",
            "authorization": f"Bearer {BEARER_TOKEN}",
            "content-type": "application/json",
            "accept": "application/json",
        },
        body=json_body
    )
    # print("---------------------------")
    # print(http_request.data)
    # print("---------------------------")
    # time.sleep(2)
    return http_request, json.loads(http_request.data.decode("utf-8"))


def ping():
    res, json_data = http_request("ping", "GET")

    if res.status == 200 and json_data["connected"]:
        print_outcome("SUCCESS", res.status, json_data)
    else:
        print_outcome("FAILED", res.status, json_data)
        exit(1)


def get_customers(thenCancel=False):
    discount = []

    res, json_data = http_request("customers", "GET")

    # Possible status values that will be returned:
    # IDLE | CHECKING_IN | SELECTING_DISCOUNT | AWAITING_PAYMENT | AWAITING_CHECKOUT
    if res.status == 200:
        while json_data["customer"] is None:
            device_state = json_data["device"]["device_state_title"]
            print(f"Device State: {device_state}")

            if device_state == "CHECKING_IN" and thenCancel:
                res, json_data = http_request(f"checkouts/cancel", "POST")
                print_outcome("CANCEL DATA:", res.status, json_data)
                if res.status == 200 and device_state == "TRANSACTION_CANCELLED":
                    print_outcome("SUCCESS", res.status, json_data)
                else:
                    print_outcome("FAILED", res.status, json_data)
                return

            res, json_data = http_request("customers", "GET")
    else:
        print_outcome("FAILED", res.status, json_data)
        exit(1)

    res, json_data = http_request("customers", "GET")

    while json_data["device"]["device_state_title"] == "SELECTING_DISCOUNT" or "CHECKING_IN":
        device_state = json_data["device"]["device_state_title"]
        print(f"Device State: {device_state}")

        if device_state == "AWAITING_CHECKOUT" or "AWAITING_PAYMENT":
            break
        res, json_data = http_request("customers", "GET")

    # If there is a reward passed in, apply it
    if len(json_data["customer"]["discounts"]) > 0:
        discount = [json_data["customer"]["discounts"][0]["uid"]]

    return json_data, discount

