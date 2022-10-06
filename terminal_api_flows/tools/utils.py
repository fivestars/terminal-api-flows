from terminal_api_flows.tools.logging import get_logger

LOGGER = get_logger()


def bad_response_message(func, http_status, json_data) -> None:
    LOGGER.error(
        f"{func.__name__} could not get success response. "
        f'last http response status "{http_status}" last json {json_data}'
    )
