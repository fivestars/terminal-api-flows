import time
from functools import partial

from terminal_api_flows import http_request
from terminal_api_flows.tools.logging import get_logger
from terminal_api_flows.tools import utils

LOGGER = get_logger()


def _terminal_ping_decorator(function: callable, attempts: int, sleep_delay: int) -> callable:
    """
    Decorator to check if the cPay terminal is active before executing the function

    :param function: python function
    :param attempts: amount of http requests before exit the code
    :return: function
    """
    def ret_function(*args, **kwargs):
        response, json_data = http_request("ping", "GET")
        made_attempts = 1
        while made_attempts <= attempts:
            LOGGER.info(f"Connect to terminal attempt: {made_attempts}")
            if response.status == 200 and json_data.get("connected"):
                LOGGER.info(" === Connected to terminal ===")
                return function(*args, **kwargs)
            else:
                utils.bad_response_message(
                    func=_terminal_ping_decorator,
                    http_status=response.status,
                    json_data=json_data
                )
            response, json_data = http_request("ping", "GET")
            made_attempts += 1
            time.sleep(sleep_delay)
        else:
            LOGGER.error("Terminal does not respond")
            exit(1)
    return ret_function


terminal_ping_decorator_3_attempts = partial(_terminal_ping_decorator, attempts=3, sleep_delay=30)
