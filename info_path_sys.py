import os
import platform
from os.path import expanduser

os_name = platform.system().lower()
current_user = expanduser("~")
path_to_project = os.path.dirname(os.path.abspath(__file__))

pytest_config = None


def get_option(option_name):
    """
    :param option_name: matched option
    :return: value of option or Exception()
    """
    if pytest_config is None:
        raise RuntimeError("pytest not initialised.")
    full_name = option_name if option_name.startswith("--") else f"--{option_name}"
    try:
        return pytest_config.getoption(full_name)
    except ValueError:
        raise Exception(f"No option '{option_name}'")
