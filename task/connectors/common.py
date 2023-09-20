import json
import logging


def read_json_file(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return {}
