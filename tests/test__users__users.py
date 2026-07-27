import pytest
import allure
from datetime import datetime

from utils.helpers import endpoint_schema, validate_schema, roll_password, get_pass_now
from utils.request_helper import Webitel
from utils.endpoints import USERS, USERS_PASSWORD
from utils.request_utils import do_login
from config import ADD_USER, USER_new_pass_DATA, USER_PASSWORD, TOKEN


@allure.feature("USERS")
@allure.story("Users")
@pytest.mark.smoke
@pytest.mark.nightly
def test__users__GET_200():
    """
    get users
    """
    request = Webitel(obf_endpoint=USERS)
    response = request.get(endpoint=USERS)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=USERS, method='GET', status_code=200))


@allure.feature("USERS")
@allure.story("Users")
@pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(2)
@pytest.mark.xdist_group(name="password")
def test__users__password__PUT_200():
    """
    change user password
    """
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
    password_request = Webitel(obf_endpoint=USERS_PASSWORD, custom_header={'X-Webitel-Access': user_data['access_token']})
    password_response = password_request.put(endpoint=USERS_PASSWORD, data=data)
    assert password_response.status_code == 200
    validate_schema(instance=password_response.json(), schema=endpoint_schema(endpoint=USERS_PASSWORD, method='PUT',
                                                                              status_code=200))
    ### try Login with old pass
    pass_now = get_pass_now()
    old_pass_response = do_login(pass_now['old_password'], data['username'], data['domain'])
    assert old_pass_response['code'] in [400, 401]
    assert old_pass_response['status'] in ["Bad Request", 'Unauthorized']
    ### try Login with new pass
    new_pass_response = do_login(pass_now['new_password'], data['username'], data['domain'])
    assert new_pass_response['code'] == 200
    assert isinstance(new_pass_response['access_token'], str)


@allure.feature("USERS")
@allure.story("Users")
@pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(3)
@pytest.mark.xdist_group(name="password")
def test__users_id__change_password__PUT_200():
    """
    change password in /users/id/general
    """
    user_data = USER_new_pass_DATA
    passwords = roll_password()
    data = {"password": passwords['new_password'], "username": user_data['new_pass']['username']}
    request = Webitel(obf_endpoint=USERS + "/{id}", custom_header={'X-Webitel-Access': user_data['access_token']})
    response = request.put(endpoint=f"{USERS}/{user_data['new_pass']['user_id']}", data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=USERS,
                                                                     method='PUT',
                                                                     status_code=200,
                                                                     additional='/{id}'))


@allure.feature("USERS")
@allure.story("Users")
@pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(4)
@pytest.mark.xdist_group(name="password")
def test__users_id__change_password__PATCH_200():
    """
    change password in /settings/general
    """
    user_data = USER_new_pass_DATA
    passwords = roll_password()
    data = {"password": passwords['new_password'], "username": user_data['new_pass']['username']}
    request = Webitel(obf_endpoint=USERS + "/{id}", custom_header={'X-Webitel-Access': user_data['access_token']})
    response = request.patch(endpoint=f"{USERS}/{user_data['new_pass']['user_id']}", data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=USERS,
                                                                     method='PATCH',
                                                                     status_code=200,
                                                                     additional='/{id}'))


@allure.feature("USERS")
@allure.story("Users")
@pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(999)
@pytest.mark.xdist_group(name="password")
@pytest.mark.skip(reason="NO LOGIN WINDOW WITH NEW PASSWORD FORM")
def test__users_id__force_change_password__PUT_200():
    """
    force_password_change": True
    """
    user_data = USER_new_pass_DATA
    data = {"force_password_change": True, "username": user_data['force_change']['username']}
    request = Webitel(obf_endpoint=f"{USERS}/id", custom_header={'X-Webitel-Access': user_data['access_token']})
    response = request.put(endpoint=f"{USERS}/{user_data['force_change']['user_id']}", data=data)

    ### try Login with old pass
    pass_now = get_pass_now()
    response = do_login(pass_now['old_password'], user_data['force_change']['username'], user_data['domain'])
    assert response['code'] in [400, 401]
    assert response['status'] == 'Unauthorized'
    ### TODO? How to login with new ???


@allure.feature("USERS")
@allure.story("Users")
@pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(3)
@pytest.mark.xdist_group(name="auth")
def test__users__add__POST_200():
    """
    add user
    """
    number = int(datetime.timestamp(datetime.now()))
    data = ADD_USER
    data['password'] = USER_PASSWORD
    data['email'] = data['email'].format(number=number)
    data['extension'] = data['extension'].format(number=number)
    data['name'] = data['name'].format(number=number)
    data['username'] = data['username'].format(number=number)
    request = Webitel(obf_endpoint=USERS, custom_header={'X-Webitel-Access': TOKEN})
    response = request.post(endpoint=USERS, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=USERS, method='POST', status_code=200,
                                                              _required_fields=['id', 'name', 'username', 'email',
                                                                                'extension']))
