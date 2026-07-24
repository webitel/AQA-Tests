import json
import pyotp
import time

from itertools import cycle
from urllib3.util.url import parse_url

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from info_path_sys import path_to_project, get_option
from utils.file_helper import write_json_file, append_to_json_file, load_json_schema, read_json_file
from config import (SCHEMA_DIR, SCHEMA_NAME, DEFAULT_SCHEMA_NAME, DEFAULT_USER_DATA_FILE, TOTP_SECRET,
                    DEFAULT_USER_LOGIN_SESSION_DATA_FILE,DEFAULT_USER_NAME__1, DEFAULT_PASSWORD__1q_6y, C_FILE, P)

SCHEMA_PATH = path_to_project + SCHEMA_DIR + SCHEMA_NAME
default_schema_path = path_to_project + SCHEMA_DIR + DEFAULT_SCHEMA_NAME


def validate_schema(instance, schema):
    class SchemaValidationError(Exception):
        pass
    try:
        validate(instance=instance, schema=schema)
    except ValidationError as e:
        safe_message = (
            f"JSON Schema Validation Failed!\n"
            f"Missing required property: {e.validator_value}\n"
            f"Schema path: {list(e.schema_path)}"
        )
        i = show_instance()
        instance = i if i is not None else instance
        raise SchemaValidationError(safe_message) from None
        # raise AssertionError(safe_message) from None


def show_instance():
    if get_option("--IN_FO") not in [True, "True"]:
        return "[CONFIDENTIAL_DATA_HIDDEN]"
    else:
        return None


def _json_serializable(text):
    try:
        json.dumps(text)
        return True
    except TypeError:
        return False
    except Exception as e:
        raise e


def apply_required(schema, _required_fields=[], _exclude=[]):
    _exclude_list = ["items", "next", "page", "size"] + (_exclude)

    if not isinstance(schema, dict):
        return

    if schema.get("type") == "object" or "properties" in schema:
        props = schema.get("properties", {})
        if props and _required_fields != []:
            needed = [k for k in props.keys() if k in _required_fields]
            schema["required"] = needed
        elif props and _required_fields == []:
            needed = [k for k in props.keys() if k not in _exclude_list]
            schema["required"] = needed

        for prop_schema in props.values():
            apply_required(prop_schema, _required_fields, _exclude_list)

    if schema.get("type") == "array" or "items" in schema:
        items_schema = schema.get("items")
        if isinstance(items_schema, dict):
            apply_required(items_schema, _required_fields, _exclude_list)
        elif isinstance(items_schema, list):
            for item in items_schema:
                apply_required(item, _required_fields, _exclude_list)


def endpoint_schema(endpoint, method, status_code, _required_fields=[], _exclude=[], additional=''):
    full_spec = load_json_schema(schema_path=SCHEMA_PATH)
    _endpoint_schema = full_spec['paths'][endpoint+additional][method.lower()]['responses'][str(status_code)]['schema']
    apply_required(_endpoint_schema, _required_fields, _exclude)
    return _endpoint_schema


def default_endpoint_schema(method, status_code, _required_fields=[], _exclude=[]):
    full_spec = load_json_schema(schema_path=default_schema_path)
    _endpoint_schema = full_spec['paths']['/default'][method.lower()]['responses'][str(status_code)]['schema']
    apply_required(_endpoint_schema, _required_fields, _exclude)
    return _endpoint_schema


def save_data_created_domain(response, domain_name):
    """
    get response after SIGNUP
    """
    d = response.json()
    access_token = d['access_token']
    data = {'domain': domain_name, 'access_token': access_token, 'username': DEFAULT_USER_NAME__1, 'password': DEFAULT_PASSWORD__1q_6y}
    write_json_file(DEFAULT_USER_DATA_FILE, data)


def save_session_token(response):
    """
    get response after LOGIN
    save session token to file => {session_token: session_token}
    """
    d = response.json()
    session_token = d['access_token']
    data = {'session_token': session_token}
    write_json_file(DEFAULT_USER_LOGIN_SESSION_DATA_FILE, data)


def save_user_id(user_id):
    data = {'user_id': user_id}
    append_to_json_file(DEFAULT_USER_DATA_FILE, data)


def save_new_user_data(data:dict, filename, *args, **kwargs):
    """
        data = {
            "email": ""
            "extension": "",
            "name": "",
            "profile": {},
            "username": ""}
    """
    file_data = read_json_file(filename)
    file_data.update(data)
    write_json_file(filename, file_data)


def anonymize_dict(data, word, k=''):
    if isinstance(data, dict):
        return {k: anonymize_dict(v, word, k) for k, v in data.items()}
    elif isinstance(data, list):
        return [anonymize_dict(item, word) for item in data]
    else:
        return f"{word} for _{k}_"


def obfuscate_control(obf, r, endpoint):
    if r is not None:
        try:
            resp_body = r.json()
        except:
            resp_body = str(r.text)
    else:
        resp_body = {}
    if r.request.body is not None:
        try:
            req_body = json.loads(r.request.body)
        except:
            req_body = str(r.request.body.text)
    else:
        req_body = {}
    if obf:
        obf_url = parse_url(r.url)
        url = str(f'{obf_url.scheme}://{obf_url.host}{endpoint}')
        if isinstance(req_body, dict):
            req_body = anonymize_dict(data=req_body, word='request')
        elif isinstance(req_body, str):
            req_body = f"string request"
        if isinstance(resp_body, (dict, list)):
            resp_body = anonymize_dict(data=resp_body, word='response')
        elif isinstance(resp_body, str):
            resp_body = f"string response"
    else:
        url = str(r.url)
    return {"url":url, "response_body": resp_body, "request_body": req_body}


def roll_password():
    actual_p_i = read_json_file(C_FILE)["p_n"]
    iter = list(P.keys())
    idx = iter.index(actual_p_i)
    shifted_list = iter[idx:] + iter[:idx]
    iterator = cycle(shifted_list)
    old_i = next(iterator)
    new_i = next(iterator)
    old_password = P[old_i]
    new_password = P[new_i]
    counter_data = read_json_file(C_FILE)
    counter_data["p_o"] = old_i
    counter_data["p_n"] = new_i
    write_json_file(C_FILE, counter_data)
    return {"old_password": old_password, "new_password": new_password}

def get_pass_now():
    """
    return:: {"old_password": old_password, "new_password": new_password}
    """
    counter_data = read_json_file(C_FILE)
    old_i = counter_data["p_o"]
    new_i = counter_data["p_n"]
    old_password = P[old_i]
    new_password = P[new_i]
    return {"old_password": old_password, "new_password": new_password}


def get_totp_now():
    totp = pyotp.TOTP(TOTP_SECRET)
    return totp.now()