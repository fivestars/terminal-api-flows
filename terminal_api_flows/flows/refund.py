import json

from terminal_api_flows import print_outcome, http_request

# ********************** #
#      Refund Flow       #
# ********************** #
def refund(checkout_reference, amount):

    refund_data = {
        "amount": amount
    }

    # POST to refunds
    res, json_data = http_request(f"refunds/{checkout_reference}", "POST", json.dumps(refund_data).encode("utf-8"))

    if res.status == 200:
        status =  json_data["status"]

        if status == "REFUND_SUCCESS":
            print_outcome("SUCCESS", res.status, json_data)
            exit(0)
        else:
            print_outcome("FAILED", res.status, json_data)

        print(f"Refund Status: {status}")
    else:
        print_outcome("FAILED", res.status, json_data)
