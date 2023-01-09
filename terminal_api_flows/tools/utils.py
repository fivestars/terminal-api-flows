from terminal_api_flows.tools.logging import get_logger

LOGGER = get_logger()


def bad_response_message(func, response, json_data) -> None:
    if response.status in (404, 504, 400):
        print(json_data)
    else:
        LOGGER.error(
            f"{func.__name__} could not get success response. "
            f'http response status "{response.status}" last json {json_data}'
        )
