import requests
import logging
from task.config import NBP_API_URL


def get_table_rate():
    try:
        response = requests.get(f"{NBP_API_URL}/exchangerates/tables/a")
        return response.json()
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection error: {e}")
        return None
