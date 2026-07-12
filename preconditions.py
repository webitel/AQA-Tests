from config import DEFAULT_USER_DATA_FILE, DEFAULT_USER_LOGIN_SESSION_DATA_FILE, FILES
from utils.file_helper import write_json_file
from utils.get_json_schemas_files import save_spec
from utils.request_utils import set_password_to_normal, set_system_settings

# from utils.decorators import calculate_time


# @calculate_time
def clear_user_data_file():
    write_json_file(DEFAULT_USER_DATA_FILE, {})


def clear_user_session_data_file():
    write_json_file(DEFAULT_USER_LOGIN_SESSION_DATA_FILE, {})

def clear_all_tmp_files():
    files = FILES
    for k, filename in files.items():
        write_json_file(filename, {})


if __name__ == "__main__":
    ""
    # save_spec()
    # clear_user_data_file()
    # clear_user_session_data_file()
    # clear_all_tmp_files()