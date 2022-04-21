from flows.cash_txn import cash_transaction
from flows.credit_txn import credit_transaction
from flows.cancel_txn import cancel_transaction
from terminal_api_flows import ping


if __name__ == "__main__":
    # To install: pip install -e .
    # Ensure urllib3 is installed if it is not already: pip install urllib3
    # You can then run this file as you wish. I did not put in an
    # entry_points for it in setup.py since most likely it will
    # be run with a debugger inside VSCode or PyCharm.
    #
    # Run these one at a time - uncomment the one you wish to run.

    # Ping
    ping()

    # Cash Transaction
    # cash_transaction()

    # Credit Transaction
    # credit_transaction()

    # Cancel Transaction
    # cancel_transaction()
