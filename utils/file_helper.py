import json
import jsonref
from typing import Union
from yaml import load, dump, Loader
from info_path_sys import path_to_project


def read_data_from_file(file_path: str) -> str:
    """
    file_path: только путь к файлу относительно корня проекта
    example: '/file_path.abc'
    """
    with open(path_to_project + file_path, 'rt') as file:
        file_data = file.read()
    return file_data


def append_data_to_file(updated_file: str, data: str):
    """
    updated_file: только путь к файлу относительно корня проекта
    example: '/updated_file.abc'
    """
    with open(path_to_project + updated_file, 'a') as updf:
        updf.write(data)


def write_data_to_file(updated_file: str, data: str):
    """
    updated_file: только путь к файлу относительно корня проекта
    example: '/updated_file.abc'
    """
    with open(path_to_project + updated_file, 'wt') as updf:
        updf.write(data)


def read_json_file(json_file_path: str) -> Union[dict, list]:
    """
    json_file_path: только путь к файлу относительно корня проекта
    example: '/json_file_path.json'

    """
    with open(path_to_project + json_file_path) as jf:
        data = json.load(jf)
    return data


def load_json_schema(schema_path):
    with open(schema_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonref.replace_refs(data)


def append_to_json_file(json_file_path: str, data: Union[dict, list]):
    """
    json_file_path: только путь к файлу относительно корня проекта
    example: '/json_file_path.json'
    """
    try:
        file_data = read_json_file(json_file_path)
        if isinstance(file_data, dict):
            file_data.update(data)
        elif isinstance(file_data, list):
            file_data.append(data)
    except:
        file_data = list()
        file_data.append(data)
    with open(path_to_project + json_file_path, 'w') as jf:
        json.dump(file_data, jf, indent=4)


def write_json_file(json_file_path: str, data: Union[dict, list]):
    """
    json_file_path: только путь к файлу относительно корня проекта
    example: '/json_file_path.json'
    """
    with open(path_to_project + json_file_path, 'wt') as f:
        json.dump(data, f, indent=4)


def read_from_yml_file(yml_file_path: str) -> Union[dict, list]:
    """
    yml_file_path: только путь к файлу относительно корня проекта
    example: '/yml_file_path.yml'

    """
    with open(path_to_project + yml_file_path, 'r') as spec:
        yml_data = load(spec.read(), Loader)
    return yml_data


def write_to_yml_file(yml_file_path: str, data: Union[dict, list]):
    """
    yml_file_path: только путь к файлу относительно корня проекта
    example: '/yml_file_path.yml'
    """
    with open(path_to_project + yml_file_path, 'w+') as file:
        file.write(dump(data))
