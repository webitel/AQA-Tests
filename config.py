# from pygments.styles import default

from info_path_sys import get_option, path_to_project, current_user
from dynaconf import Dynaconf

"""

root dir for configs --> dynaconf
files with configs:
    .settings.yaml
    .secrets.yaml

"""

# settings = Dynaconf(root_path=current_user + '/dynaconf', includes=["*.yaml"])
settings = Dynaconf(root_path=path_to_project, includes=["*.yaml"])

def __env():
    try:
        get_env = get_option("--env")
        return get_env
    except Exception:
        return "test"


_env = __env()

DYNA_ROOT = settings.root_path_for_dynaconf

# get by env
API_URL = settings.secret[_env].api_json
TOKEN = settings.secret[_env].token
BASE_URL = settings.secret[_env].api_base_url
DOMAIN = settings.secret[_env].domain
USER_ID = settings.secret[_env].user_id
USER_PASSWORD = settings.secret[_env].password
PRESET_QUERY_SERVICE_ID = settings.secret[_env].preset_query_id
TOTP_SECRET = settings.secret[_env].totp_secret
LICENSE_KEY = settings.secret[_env].license_key

HEADERS = settings[_env].headers.to_dict()

SCHEMA_DIR = settings.secret[_env].schema_dir
SCHEMA_NAME = settings.secret[_env].schema_name

DEFAULT_SCHEMA_NAME = settings.secret[_env].default_schema_name_file
FILES = settings.secret[_env].files.to_dict()
DEFAULT_USER_DATA_FILE = settings.secret[_env].files.data_new_domain_file
DEFAULT_USER_LOGIN_SESSION_DATA_FILE = settings.secret[_env].files.login_session_file
DEFAULT_new_USER_DATA_FILE = settings.secret[_env].files.new_user_data_file
USER_new_pass_DATA = settings.secret[_env].user_new_pass_data.to_dict()
C_FILE = settings.secret[_env].c_file
P = settings.secret[_env].p.to_dict()
SYSTEM_SETTINGS_PASSWORD = settings.secret[_env].system_settings_password.to_list()
SYSTEM_SETTINGS_2FA = settings.secret[_env].system_settings_2fa

DEFAULT_USER_NAME__1 = settings.secret[_env].default_user
DEFAULT_PASSWORD__1q_6y = settings.secret[_env].default_password
DEFAULT_PASSWORD_NEW__1q_4r = settings.secret[_env].new_password
DEFAULT_DOMAIN_NAME_1 = settings.secret[_env].default_domain_name
DEFAULT_add_USER_EMAIL = settings.secret[_env].default_user_email
DEFAULT_USER_LOGIN_NAME = settings.secret[_env].user_login_name
DEFAULT_USER_LOGIN_TOKEN = settings.secret[_env].user_login_token

DEVICE_ID = settings.secret[_env].device.id
DEVICE_NAME = settings.secret[_env].device.name

ADD_USER = {
    "email": DEFAULT_add_USER_EMAIL,
    "extension": "0{number}",
    "name": "aqa_user_delete_me__{number}",
    "profile": {},
    "username": "user{number}"
}

SKILLS_PARAMS = settings.secret[_env].skills.to_dict()