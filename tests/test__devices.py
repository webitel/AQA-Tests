import pytest
import allure
from datetime import datetime

from utils.helpers import endpoint_schema, validate_schema
from utils.request_helper import Webitel
from utils.request_utils import get_device_for_delete
from utils.endpoints import DEVICES, DEVICES_ID_USERS_AUDIT
from config import DEVICE_ID, DEVICE_NAME, DEFAULT_PASSWORD__1q_6y


@allure.feature("DEVICES")
@allure.story("Devices")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__devices__GET_200():
    """
    get devices
    """
    params = {"size": 1000}
    request = Webitel(obf_endpoint=DEVICES)
    response = request.get(endpoint=DEVICES, _params=params)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=DEVICES, method='GET', status_code=200))


@allure.feature("DEVICES")
@allure.story("Devices")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__devices_by_id__GET_200():
    """
    get device by id
    """
    request = Webitel(obf_endpoint=DEVICES + '/{id}')
    response = request.get(endpoint=f'{DEVICES}/{DEVICE_ID}')
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=DEVICES, method='GET',
                                                                     status_code=200, additional='/{id}'))


@allure.feature("DEVICES")
@allure.story("Devices")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__devices_id_users_audit__GET_200():
    """
    get device by id
    """
    params = {"size": 1000}
    request = Webitel(obf_endpoint=DEVICES_ID_USERS_AUDIT)
    response = request.get(endpoint=DEVICES_ID_USERS_AUDIT.format(id=DEVICE_ID), _params=params)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=DEVICES_ID_USERS_AUDIT.format(id="{device.id}"),
                                                                     method='GET', status_code=200))


@allure.feature("DEVICES")
@allure.story("Devices")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(1)
@pytest.mark.xdist_group(name="devices")
def test__devices__POST_200():
    """
    Create new device
    """
    number = int(datetime.timestamp(datetime.now()))
    data = {
        "name": f"aqa_delete_this_device_{number}",
        "account": f"aqa_delete_this_device_{number}",
        "password": DEFAULT_PASSWORD__1q_6y
        }
    request = Webitel(obf_endpoint=DEVICES)
    response = request.post(endpoint=DEVICES, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=DEVICES, method='POST', status_code=200))


@allure.feature("DEVICES")
@allure.story("Devices")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(2)
@pytest.mark.xdist_group(name="devices")
def test__devices_by_id__PUT_200():
    """
    Change device name by id
    """
    number = int(datetime.timestamp(datetime.now()))
    data = {"name": f"{DEVICE_NAME}_{number}", "account": f"{DEVICE_NAME}_{number}"}
    request = Webitel(obf_endpoint=DEVICES + '/{devce.id}')
    response = request.put(endpoint=f'{DEVICES}/{DEVICE_ID}', data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=DEVICES, method='PUT', status_code=200,
                                                                     additional='/{device.id}'))


@allure.feature("DEVICES")
@allure.story("Devices")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(3)
@pytest.mark.xdist_group(name="devices")
def test__devices_by_id__PATCH_200():
    """
    Change device params by id
    """
    number = int(datetime.timestamp(datetime.now()))
    data = {"name": f"{DEVICE_NAME}_{number}", "account": f"{DEVICE_NAME}_{number}", "brand": f"PythonPhone{number}"}
    request = Webitel(obf_endpoint=DEVICES + '/{devce.id}')
    response = request.patch(endpoint=f'{DEVICES}/{DEVICE_ID}', data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=DEVICES, method='PATCH', status_code=200,
                                                                     additional='/{device.id}'))


@allure.feature("DEVICES")
@allure.story("Devices")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(4)
@pytest.mark.xdist_group(name="devices")
def test__devices_by_id__DELETE_200():
    """
    delete devices
    """
    try:
        device_id = get_device_for_delete()
    except Exception as e:
        raise Exception("Need devices for deleting") from None
    request = Webitel(obf_endpoint=DEVICES + '/{id}')
    response = request.delete(endpoint=f'{DEVICES}/{device_id}')
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=DEVICES, method='DELETE',
                                                                     status_code=200, additional='/{id}'))


# @allure.feature("DEVICES")
# @allure.story("Devices")
# # @pytest.mark.smoke
# @pytest.mark.nightly
# @pytest.mark.skip(reason="need dev")
# def test__devices__DELETE_200():
#     """
#     delete devices
#     """
#     d_devices = get_devices()
#     device_id = [i['id'] for i in d_devices['items']][0]
#     data = {"ids": [device_id]}
#     request = Webitel(obf_endpoint=DEVICES)
#     response = request.delete(endpoint=DEVICES, data=data)
#     assert response.status_code == 200
#     validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=DEVICES, method='DELETE', status_code=200))