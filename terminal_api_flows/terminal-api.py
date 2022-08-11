import logging

from flows.cash_txn import cash_transaction
from flows.credit_txn import credit_transaction, verify_cpay_1567
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
    # ping()

    # Cash Transaction
    # cash_transaction()

    # Credit Transaction
    # credit_transaction()

    # Other Transaction
    # other_transaction()

    # Cancel Transaction
    # cancel_transaction()

    # Refund - run a credit transaction and capture the checkout reference id
    # Use the checkout reference id and amount in the params below
    refund("91ca9ce791c64ce18b420310b2a15fab", 800)

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
    # get_customers(thenCancel=True)
    # verify_cpay_1567()
