import logging

from flows.cash_txn import cash_transaction
from flows.credit_txn import credit_transaction, credit_to_cash_transaction, verify_cpay_1567
from flows.cancel_txn import cancel_transaction, cancel_transaction_404, cancel_transaction_105
from flows.other_txn import other_transaction
from flows.refund import refund
from terminal_api_flows import get_state, ping, get_customers, turn_on_screensaver, turn_off_screensaver

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


    # Get device state action
    # get_state()

    # TAPI v1.0.0.3 https://app.swaggerhub.com/apis/fs-integrations/Terminal-API/1.0.0.3
    # There are 3 options to skip screens and you can enable/disable some or all
    # SKIP_TIPS - SKIP_REWARD_NOTIFICATION - SKIP_SIGNIN
    # allow_discount parameter when set to False will override a discount/reward and replace it with the first
    # unselected one found. If there are no unselected ones it removes the reward/discount. You can of course
    # override this with any valid discount uid returned from the GET /customers call (look for the discounts field)

    # Cash Transaction (Reminder: tips are only on credit transactions so skip_tip has no effect here)
    # cash_transaction(
    #     total=850,
    #     skip_tip=False,
    #     skip_reward_notification=False,
    #     skip_signin=False,
    #     allow_discount=True
    # )

    # $0 Dollar Cash Transaction
    # cash_transaction(total=0, skip_tip=False, skip_reward_notification=False, skip_signin=False, allow_discount=True)

    # Credit Transaction
    # credit_transaction(
    #     1875,
    #     skip_tip=False,
    #     # You can skips these screens when you post the checkout
    #     skip_reward_notification=False,
    #     skip_signin=False,
    #     allow_discount=True,
    #     # You can skips these screens when they show up in real time
    #     # The notifications can happen very fast so you may not see them
    #     # prior to re-starting your long poll connection. A second call to
    #     # the actions endpoint to skip a screen might be required if you suspect
    #     # you are on a screen you want to skip.
    #     skip_tips_screen=True,
    #     # Approval screen happens very fast after the POST checkouts and
    #     # is very difficult to catch in real time. If you want to test this you can
    #     # wait for the 2 minute timeout and it will move you along to the next screen.
    #     # Note: The approval screen only shows when early checkin with a credit card is used
    #     # and a card checkout is started.
    #     skip_approval_screen=False,
    #     skip_reward_notification_screen=True)

    # Credit to Cash Transaction
    # Note to partners: cash switching will be triggered if cPay returns any card decline, swipe read errors, etc.
    # Note: you cannot sign in with a credit card to trigger this - sign in with a phone number
    # Note: skip_signin is not available in this kind of flow
    # credit_to_cash_transaction(1550, skip_tip=False, skip_reward_notification=False, allow_discount=True)

    # $0 Dollar Credit Transaction
    # Note to partners: If you are running a $0 transaction you should run
    # it as a $0 CASH transaction unless you know they will be adding a tip
    # to the $0 amount.
    # credit_transaction(total=0)

    # Other Transaction
    # other_transaction(skip_tip=False, skip_reward_notification=False, skip_signin=False, allow_discount=True)

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

    # Screensaver
    # turn_on_screensaver()
    # turn_off_screensaver()
