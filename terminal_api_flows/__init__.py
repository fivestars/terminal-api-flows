import json
import uuid
import urllib3


HTTP = urllib3.PoolManager()
# Adjust these as needed
BASE_URL = "https://ws.chad-dev-test-v1.kdev.awesomestartup.com/api/v1/terminals/222222222222/"
BEARER_TOKEN = "7e5c8c2797e547fa8794715ceabe6efb"
SOFTWARE_ID = "TEST1"
POS_ID = "111"


def print_outcome(failed, status_code, json_data=None):
    print("--------------------------------------")
    print(f"Flow Outcome: {failed}")
    print(f"Status Code: {status_code}")
    print("--------------------------------------")
    if(json_data):
        print(json_data)


def generate_ids(json_data):
    pos_checkout_id = uuid.uuid4().__str__()
    pos_order_id = uuid.uuid4().__str__()
    customer_uid = json_data["customer"]["uid"]

    return pos_checkout_id, pos_order_id, customer_uid


def http_request(endpoint, action, json_body=""):
    http_request = HTTP.request(
        action,
        f"{BASE_URL}/{endpoint}",
        headers={
            "software-id": f"{SOFTWARE_ID}",
            "pos-id": f"{POS_ID}",
            "authorization": f"Bearer {BEARER_TOKEN}",
            "content-type": "application/json",
        },
        body=json_body
    )
    return http_request, json.loads(http_request.data.decode("utf-8"))


def ping():
    json_data = {}

    res, json_data = http_request("ping", "GET")

    if res.status == 200 and json_data["connected"] == True:
        print_outcome("SUCCESS", res.status, json_data)
    else:
        print_outcome("FAILED", res.status, json_data)
        exit(1)


def get_customers():
    json_data = {}
    discount = []

    res, json_data = http_request("customers", "GET")

    # Call the customers endpoint again on every one of
    # these until the customer object is no longer null
    # Possible status values that will be returned:
    # IDLE | CHECKING_IN | SELECTING_DISCOUNT | AWAITING_PAYMENT | AWAITING_CHECKOUT
    if res.status == 200:
        while json_data["customer"] == None:
            device_state = json_data["device"]["device_state_title"]
            print(f"Device State: {device_state}")
            res, json_data = http_request("customers", "GET")
    else:
        print_outcome("FAILED", res.status, json_data)
        exit(1)

    res, json_data = http_request("customers", "GET")

    while json_data["device"]["device_state_title"] == "SELECTING_DISCOUNT" or "CHECKING_IN":
        device_state = json_data["device"]["device_state_title"]
        print(f"Device State: {device_state}")
        if json_data["device"]["device_state_title"] == "AWAITING_CHECKOUT" or "AWAITING_PAYMENT":
            break
        res, json_data = http_request("customers", "GET")

    # If there is a reward passed in, apply it
    if len(json_data["customer"]["discounts"]) > 0:
            discount = [ json_data["customer"]["discounts"][0]["uid"] ]

    return json_data, discount

