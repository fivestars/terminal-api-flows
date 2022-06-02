from flows.cash_txn import cash_transaction
from flows.credit_txn import credit_transaction, verify_cpay_1567
from flows.cancel_txn import cancel_transaction, cancel_transaction_404, cancel_transaction_105
from terminal_api_flows import ping, get_customers


if __name__ == "__main__":
    # To install: pip install -e .
    # Ensure urllib3 is installed if it is not already: pip install urllib3
    # You can then run this file as you wish. I did not put in an
    # entry_points for it in setup.py since most likely it will
    # be run with a debugger inside VSCode or PyCharm.
    #
    # Run these one at a time - uncomment the one you wish to run.

    # Ping
    # ping()

    # Cash Transaction
    # cash_transaction()

    # Credit Transaction
    # credit_transaction()

    # Cancel Transaction
    # cancel_transaction()

    # cancel_transaction_404()
    # cancel_transaction_105()

    # Cancel check-in, start txn
    # Verify https://sumupteam.atlassian.net/browse/CPAY-1567
    # Just press the "Check in" button on cPay and the script will do the rest
    get_customers(thenCancel=True)
    verify_cpay_1567()
