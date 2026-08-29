import time
import pytest
import allure
from datetime import datetime

from config import (DOMAIN, LICENSE_KEY, DEFAULT_USER_NAME__1, DEFAULT_PASSWORD__1q_6y,
                    DEFAULT_DOMAIN_NAME_1, DEFAULT_USER_DATA_FILE, DEFAULT_USER_LOGIN_NAME, USER_new_pass_DATA)
from utils.helpers import (endpoint_schema, default_endpoint_schema, validate_schema, roll_password, get_totp_now,
                           save_data_created_domain)

from utils.request_helper import Webitel
from utils.request_utils import do_login, set_2fa
from utils.endpoints import SIGNUP, LOGIN, LOGIN_2FA
from utils.file_helper import read_json_file

name_number = int(datetime.timestamp(datetime.now()))
domain_name = f"{DEFAULT_DOMAIN_NAME_1}{name_number}"


@allure.feature("AUTH")
@allure.story("Signup")
@pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(1)
@pytest.mark.xdist_group(name="auth")
def test__auth__signup__POST_200():
    """
    create new domain + first user
    check response

    response:
    {'access_token': 'access_token', 'token_type': 'Bearer'}
    """
    params = {"generate_device": "true"}
    data = {
        "domain": domain_name,
        "username": DEFAULT_USER_NAME__1,
        "password": DEFAULT_PASSWORD__1q_6y,
        "certificate": LICENSE_KEY
    }
    request = Webitel(obf_endpoint=SIGNUP, custom_header="clear")
    response = request.post(endpoint=SIGNUP, data=data, _params=params)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=SIGNUP,
                                                              method='POST',
                                                              status_code=200,
                                                              _required_fields=['access_token']
                                                              ))
    save_data_created_domain(response, domain_name)


@allure.feature("AUTH")
@allure.story("Signup")
@pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(2)
@pytest.mark.xdist_group(name="auth")
def test__auth__signin_with_new__POST_200():
    """
    login with new user on new domain
    """
    data = read_json_file(DEFAULT_USER_DATA_FILE)
    if not data:
        raise Exception("No data for new user on new domain")
    params = {'username': data['username'], 'password': data['password'], 'domain': data['domain']}
    request_login = Webitel(obf_endpoint=LOGIN)
    response_login = request_login.post(endpoint=LOGIN, data=params)
    assert response_login.status_code == 200
    validate_schema(instance=response_login.json(), schema=default_endpoint_schema(method='POST', status_code=200,
                                                                            _required_fields=['access_token']))


@allure.feature("AUTH")
@allure.story("Login")
@pytest.mark.smoke
@pytest.mark.nightly
def test__auth__login_mobile__POST_200():
    """
    login with mobile mark
    """
    data = {
        "domain": DOMAIN,
        "password": DEFAULT_PASSWORD__1q_6y,
        "username": DEFAULT_USER_LOGIN_NAME,
        "mobile": True
    }
    request_login = Webitel(obf_endpoint=LOGIN, custom_header="clear")
    response_login = request_login.post(endpoint=LOGIN, data=data)
    assert response_login.status_code in [200, 300]
    validate_schema(instance=response_login.json(), schema=default_endpoint_schema(method='POST', status_code=200,
                                                                            _required_fields=['access_token']))


@allure.feature("AUTH")
@allure.story("Login")
@pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.parametrize("data", [{"domain": DOMAIN,
                                   "password": DEFAULT_PASSWORD__1q_6y,
                                   "username": DEFAULT_USER_LOGIN_NAME},
                                  {"password": DEFAULT_PASSWORD__1q_6y,
                                   "username": f"{DEFAULT_USER_LOGIN_NAME}@{DOMAIN}"}],
                                    ids=["with domain", "without domain"])
def test__auth__login__POST_200(data):
    """
    login without mobile mark
    """
    request_login = Webitel(obf_endpoint=LOGIN, custom_header="clear")
    response_login = request_login.post(endpoint=LOGIN, data=data, allow_redirects=True)
    assert response_login.status_code in [200, 300]
    validate_schema(instance=response_login.json(), schema=default_endpoint_schema(method='POST', status_code=200,
                                                                            _required_fields=['access_token']))

@allure.feature("AUTH")
@allure.story("Login")
@pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(6)
@pytest.mark.xdist_group(name="password")
@pytest.mark.skip(reason="NO LOGIN WINDOW WITH NEW PASSWORD FORM")
def test__auth__login_password__POST_200():
    user_data = USER_new_pass_DATA
    passwords = roll_password()
    data = {
        "domain": user_data['domain'],
        "id": user_data['new_pass']['user_id'],
        "old_password": passwords['old_password'],
        "user_password": passwords['new_password'],
        "confirm_password": passwords['new_password'],
        "username": user_data['new_pass']['username']
        }
    login_request = Webitel(obf_endpoint=LOGIN, custom_header={'X-Webitel-Access': user_data['access_token']})
    login_response = login_request.post(endpoint=LOGIN, data=data)
    assert login_response.status_code == 200
    validate_schema(instance=login_response.json(), schema=default_endpoint_schema(method='POST', status_code=200,
                                                                            _required_fields=['access_token']))


# TODO fix it
@allure.feature("AUTH")
@allure.story("Login")
@pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(4)
@pytest.mark.xdist_group(name="auth")
@pytest.mark.skip(reason="401,416")
def test__auth__2fa__POST_200():
    """
    {"id":"login_id","totp":"your_totp"}
    """
    set_2fa(True)
    try:
        login_response = do_login(password=DEFAULT_PASSWORD__1q_6y,
                                  username=DEFAULT_USER_LOGIN_NAME,
                                  domain=DOMAIN)
        login_id = login_response['id']
        login_request = Webitel(obf_endpoint=LOGIN_2FA)
        time.sleep(1)
        data = {"id": login_id, "totp": get_totp_now()}
        login_2fa_response = login_request.post(endpoint=LOGIN_2FA, data=data)
        assert login_2fa_response.status_code == 200
        validate_schema(instance=login_2fa_response.json(),
                        schema=default_endpoint_schema(method='POST',
                                                       status_code=200,
                                                       _required_fields='access_token'))
    finally:
        set_2fa(False)