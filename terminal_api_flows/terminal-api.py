import logging

from flows.cash_txn import cash_transaction
from flows.credit_txn import credit_transaction, credit_to_cash_transaction, verify_cpay_1567
from flows.cancel_txn import cancel_transaction, cancel_transaction_404, cancel_transaction_105
from flows.other_txn import other_transaction
from flows.refund import refund
from terminal_api_flows import ping, get_customers


if __name__ == "__main__":
    # To install: pip install -e .
    # Ensure urllib3 is installed if it is not already: pip install urllib3
    # You can then run this file as you wish. I did not put in an
    # entry_points for it in setup.py since most likely it will
    # be run with a debugger inside VSCode or PyCharm.
    # Setup logging for debug info
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    #
    # Run these one at a time - uncomment the one you wish to run.

    # Ping
    ping()

    # TAPI v1.0.0.3 https://app.swaggerhub.com/apis/fs-integrations/Terminal-API/1.0.0.3
    # There are 3 options to skip screens and you can enable/disable some or all
    # SKIP_TIPS - SKIP_REWARD_NOTIFICATION - SKIP_SIGNIN

    # Cash Transaction
    # cash_transaction(total=850, skip_tip=False, skip_reward_notification=False, skip_signin=False)

    # $0 Dollar Cash Transaction
    # cash_transaction(total=0, skip_tip=False, skip_reward_notification=False, skip_signin=False)

    # Credit Transaction
    # credit_transaction(1550, skip_tip=False, skip_reward_notification=False, skip_signin=False)

    # Credit to Cash Transaction
    # Note to partners: cash switching will be triggered if cPay returns any card decline, swipe read errors, etc.
    # Note: you cannot sign in with a credit card to trigger this - sign in with a phone number
    # Note: skip_signin is not available in this kind of flow
    # credit_to_cash_transaction(1550, skip_tip=False, skip_reward_notification=False)

    # $0 Dollar Credit Transaction
    # Note to partners: If you are running a $0 transaction you should run
    # it as a $0 CASH transaction unless you know they will be adding a tip
    # to the $0 amount.
    # credit_transaction(total=0)

    # Other Transaction
    # other_transaction(skip_tip=False, skip_reward_notification=False, skip_signin=False)

    # Cancel Transaction
    # cancel_transaction()

    # Refund - run a credit transaction and capture the checkout reference id
    # Use the checkout reference id and amount in the params below
    # refund("91ca9ce791c64ce18b420310b2a15fab", 800)

    # Partial Refund - run a credit transaction and capture the checkout reference id
    # Use the checkout reference id and amount in the params below
    # refund("86ba9ce791c64ca58b420321a2a15c56", 400)

    # Refunds - Things to test
    # - use an amount too high from the original amount
    # - use an amount of $0
    # - use the same checkout reference that has already been refunded
    # - use and invalid checkout reference

    # cancel_transaction_404()
    # cancel_transaction_105()

    # Cancel check-in, start txn
    # Verify https://sumupteam.atlassian.net/browse/CPAY-1567
    # Just press the "Check in" button on cPay and the script will do the rest
    # get_customers(then_cancel=True)
    # verify_cpay_1567()
