import os
import requests
from config import API_URL, SCHEMA_DIR, SCHEMA_NAME
from info_path_sys import path_to_project
from utils.file_helper import write_json_file
# from utils.decorators import calculate_time

SCHEMA_PATH = SCHEMA_DIR + SCHEMA_NAME

# @calculate_time
def save_spec():
    response = requests.get(API_URL)
    spec = response.json()
    os.makedirs(path_to_project + SCHEMA_DIR, exist_ok=True)
    write_json_file(SCHEMA_PATH, spec)


if __name__ == "__main__":
    save_spec()
