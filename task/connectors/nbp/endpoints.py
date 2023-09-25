import requests

from task.config import NBP_API_URL
from task.logger import LOGGER


def get_table_rate():
    try:
        response = requests.get(f"{NBP_API_URL}/exchangerates/tables/a")
        if not response.status_code == 200:
            LOGGER.error(f"Invalid status code: {response.status_code}")
            return None
        return response.json()
    except requests.exceptions.ConnectionError as e:
        LOGGER.error(f"Connection error: {e}")
