import pytest
import allure
from datetime import datetime

from utils.helpers import endpoint_schema, validate_schema
from utils.request_helper import Webitel
from utils.endpoints import SETTINGS, SETTINGS_AVAILABLE
from config import SYSTEM_SETTINGS_PASSWORD


@allure.feature("SETTINGS")
@allure.story("System settings")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__settings__GET_200():
    """
    get system settings
    """
    params = {"size": 1000}
    request = Webitel(obf_endpoint=SETTINGS)
    response = request.get(endpoint=SETTINGS, _params=params)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=SETTINGS, method='GET',
                                                                     status_code=200))


@allure.feature("SETTINGS")
@allure.story("System settings")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__settings_available__GET_200():
    """
    get available system settings
    """
    params = {"size": 1000}
    request = Webitel(obf_endpoint=SETTINGS_AVAILABLE)
    response = request.get(endpoint=SETTINGS_AVAILABLE, _params=params)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=SETTINGS_AVAILABLE, method='GET',
                                                                     status_code=200))


@allure.feature("SETTINGS")
@allure.story("System settings")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__settings_id__GET_200():
    """
    get system settings by id
    """
    settings = SYSTEM_SETTINGS_PASSWORD
    sys_setting_id = settings[2]['id']
    params = {"size": 1000}
    request = Webitel(obf_endpoint=SETTINGS + '/{id}')
    response = request.get(endpoint=f'{SETTINGS}/{sys_setting_id}', _params=params)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=SETTINGS, method='GET',
                                                                     status_code=200,
                                                                     additional='/{id}'))

@allure.feature("SETTINGS")
@allure.story("System settings")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__settings_id__PUT_200():
    """
    set system settings
    """
    settings = SYSTEM_SETTINGS_PASSWORD
    sys_setting_id = settings[2]['id']
    sys_setting_value = settings[2]['value']
    data = {"value": sys_setting_value}
    request = Webitel(obf_endpoint=SETTINGS + '/{id}')
    response = request.put(endpoint=f'{SETTINGS}/{sys_setting_id}', data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=SETTINGS, method='PUT',
                                                                     status_code=200,
                                                                     additional='/{id}'))


@allure.feature("SETTINGS")
@allure.story("System settings")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__settings_id__PATCH_200():
    """
    set system settings
    """
    settings = SYSTEM_SETTINGS_PASSWORD
    sys_setting_id = settings[2]['id']
    sys_setting_value = settings[2]['value']
    sys_setting_name = settings[2]['name']
    data = {"fields": [sys_setting_name], "value": sys_setting_value}
    request = Webitel(obf_endpoint=SETTINGS + '/{id}')
    response = request.patch(endpoint=f'{SETTINGS}/{sys_setting_id}', data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=SETTINGS, method='PATCH',
                                                                     status_code=200,
                                                                     additional='/{id}'))



@allure.feature("SETTINGS")
@allure.story("System settings")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.skip(reason="need setting for tests")
def test__settings__POST_200():
    """
    add new system setting
    """
    number = int(datetime.timestamp(datetime.now()))
    data = {"name": f"aqa_delete_me_please_{number}", "value": "ghoti"}
    request = Webitel(obf_endpoint=SETTINGS)
    response = request.post(endpoint=SETTINGS, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=SETTINGS, method='POST',
                                                                     status_code=200))


@allure.feature("SETTINGS")
@allure.story("System settings")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.skip(reason="need setting for tests")
def test__settings_id__DELETE_200():
    """
    DELETE system setting by id
    """
    setting_id = 000
    request = Webitel(obf_endpoint=SETTINGS + '/{id}')
    response = request.delete(endpoint=f'{SETTINGS}/{setting_id}')
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=SETTINGS, method='DELETE',
                                                                     status_code=200,
                                                                     additional='/{id}'))