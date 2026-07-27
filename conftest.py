import os
import json
import pytest
import info_path_sys
from preconditions import clear_all_tmp_files, save_spec, set_password_to_normal, set_system_settings, clear_agent_skill


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test", help="(YES | NO)")
    parser.addoption("--IN_FO", action="store", default=False)


def pytest_configure(config):
    info_path_sys.pytest_config = config


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    results_dir = os.path.join(session.config.rootdir, "allure-results")
    if os.path.exists(results_dir):
        for filename in os.listdir(results_dir):
            if filename.endswith("-result.json"):
                filepath = os.path.join(results_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if "parameters" in data:
                        data["parameters"] = []
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                except Exception:
                    pass


@pytest.fixture(scope="session", autouse=True)
def conditions():
    clear_all_tmp_files()
    save_spec()
    set_password_to_normal()
    set_system_settings()
    clear_agent_skill()
    yield
    clear_all_tmp_files()
    set_password_to_normal()
    clear_agent_skill()
