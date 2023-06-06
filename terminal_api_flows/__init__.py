from  base64 import b64encode
import json
from typing import Tuple
import uuid
import urllib3


HTTP = urllib3.PoolManager(timeout=160)
# Adjust these as needed
TERMINAL_ID = " --> TERMINAL ID HERE <--- "
KEY_SECRET = " --> KEY-SECRET-HERE <--" # Format is your KEY:SECRET
FIVESTARS_SOFTWARE_ID = " --> FIVESTARS-SOFTWARE-ID <--"
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


def http_request(endpoint, action, json_body="") -> Tuple[urllib3.HTTPResponse, dict]:
    request = HTTP.request(
        action,
        f"{BASE_URL}{endpoint}",
        headers={
            "pos-id": f"{POS_ID}",
            "fivestars-software-id": f"{FIVESTARS_SOFTWARE_ID}",
            "User-agent": "TapiPythonSampleClient",
            "authorization": f"Basic {b64encode(bytes(f'{KEY_SECRET}', encoding='utf-8')).decode('utf-8')}",
            "content-type": "application/json",
            "accept": "application/json",
        },
        body=json_body
    )
    # Uncomment for debugging assistance
    # try:
    #     print("---------------------------")
    #     print(http_request.data)
    #     print("---------------------------")
    # except:
    #     pass
    # Add a sleep if you want to slow the calls down
    # time.sleep(2)
    return request, json.loads(request.data.decode("utf-8"))


def skip_screen():
    print("Skipping current screen")
    res, json_data = http_request(f"actions", "POST", json.dumps({"action": "pay_skip_user_action"}).encode("utf-8"))
    print(f"Actions endpoint response: {res.status}")
    print(f"    `-------------payload: {json_data['status']}")


def ping():
    res, json_data = http_request("ping", "GET")

    if res.status == 200 and json_data["connected"]:
        print_outcome("SUCCESS", res.status, json_data)
    else:
        print_outcome("FAILED", res.status, json_data)
        exit(1)


def get_customers(then_cancel=False, skip_signin=False, allow_discount=True):
    if skip_signin:
        json_data = {
            "customer": {
                "uid": ''
            }
        }
        return json_data, []

    res, json_data = http_request("customers", "GET")

    # Possible status values that will be returned:
    # IDLE | CHECKING_IN | SELECTING_DISCOUNT | AWAITING_PAYMENT | AWAITING_CHECKOUT
    if res.status == 200:
        while json_data["customer"] is None:
            device_state = json_data["device"]["device_state_title"]
            print(f"Device State: {device_state}")

            if device_state == "CHECKING_IN" and then_cancel:
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

    while json_data["device"]["device_state_title"] in ["SELECTING_DISCOUNT", "CHECKING_IN"]:
        device_state = json_data["device"]["device_state_title"]
        print(f"Device State: {device_state}")

        if device_state in ["AWAITING_CHECKOUT", "AWAITING_PAYMENT"]:
            break
        res, json_data = http_request("customers", "GET")

    # If there is a reward passed in, apply it if allow_discount=True
    # otherwise if allow_discount=False then pick the first unselected
    # reward or if there are none remove the discount/reward completely
    discount_uids = []
    discounts = list(filter(lambda x: x["selected"]==allow_discount, json_data["customer"]["discounts"]))

    if len(discounts) > 0:
        # Even if its an override we just grab the first discount id
        # In a point of sale you can set this to whatever discount ids are available
        discount_uids = [discounts[0]["uid"]]

    print('--------------- Customer Data ---------------')
    print(json_data)

    return json_data, discount_uids




def get_state():
    print("Getting state")
    res, json_data = http_request("actions", "POST", json.dumps({"action": "get_state"}).encode("utf-8"))
    print(f"Action endpoint response: {res.status}")
    print(f"    `--------------state: \n\t{json_data}")
