import pytest
import allure
from datetime import datetime, timezone
from utils.helpers import endpoint_schema, validate_schema
from utils.request_helper import Webitel
from utils.request_utils import get_id_call_center__preset_query_DELETE
from utils.endpoints import PRESET_QUERY_SERVICE
from config import PRESET_QUERY_SERVICE_ID

now = datetime.now(timezone.utc)
timestamp = now.timestamp()


@allure.feature("CALL CENTER")
@allure.story("Preset query service")
@pytest.mark.nightly
@pytest.mark.order()
@pytest.mark.xdist_group(name="preset query service")
def test__call_center__preset_query__GET_200():
    request = Webitel(obf_endpoint=PRESET_QUERY_SERVICE)
    response = request.get(endpoint=PRESET_QUERY_SERVICE, _params={'size': 5000})
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=PRESET_QUERY_SERVICE,
                                                              method='GET',
                                                              status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Preset query service")
@pytest.mark.nightly
@pytest.mark.order()
@pytest.mark.xdist_group(name="preset query service")
def test__call_center__preset_query_by_id__GET_200():
    request = Webitel(obf_endpoint=PRESET_QUERY_SERVICE)
    response = request.get(endpoint=PRESET_QUERY_SERVICE, _params={'id': PRESET_QUERY_SERVICE_ID})
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=PRESET_QUERY_SERVICE,
                                                              method='GET',
                                                              status_code=200,
                                                              additional='/{id}'))


@allure.feature("CALL CENTER")
@allure.story("Preset query service")
@pytest.mark.nightly
@pytest.mark.order(1)
@pytest.mark.xdist_group(name="preset query service")
def test__call_center__preset_query__POST_200():
    data = {
        "description": f"qaa tests ({timestamp}) - delete it",
        "name": f"qaa tests ({timestamp}) - delete it",
        "preset": {
            "filters_manager.to_string": '{"createdAt_val":{"from":1767218400000,"to":1798754340000},"createdAt_lbl":"QAA tests"}',
            "namespace": "modules/registry"
            },
        "section": "modules/registry"
    }

    required_fields = ['created_at', 'description', 'id', 'name', 'preset', 'section', 'updated_at']
    request = Webitel(obf_endpoint=PRESET_QUERY_SERVICE)
    response = request.post(endpoint=PRESET_QUERY_SERVICE, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=PRESET_QUERY_SERVICE,
                                                              method='POST',
                                                              status_code=200,
                                                              _required_fields=required_fields))


@allure.feature("CALL CENTER")
@allure.story("Preset query service")
@pytest.mark.nightly
@pytest.mark.order(2)
@pytest.mark.xdist_group(name="preset query service")
def test__call_center__preset_query_by_id__PUT_200():
    data = {
        "name": f"AQA_TESTS_DO_NOT_DELETE",
        "description": f"DO NOT DELETE PLEASE ({timestamp})",
        "preset": {
            "filters_manager.to_string": '{"createdAt_val":{"from":1767218400000,"to":1798754340000},"createdAt_lbl":"QAA tests"}',
            "namespace": "modules/registry"
            },
        "section": "modules/registry"
    }

    required_fields = ['created_at', 'description', 'id', 'name', 'preset', 'section', 'updated_at']
    request = Webitel(obf_endpoint=PRESET_QUERY_SERVICE+'/{id}')
    response = request.put(endpoint=PRESET_QUERY_SERVICE+f'/{PRESET_QUERY_SERVICE_ID}', data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=PRESET_QUERY_SERVICE,
                                                              method='PUT',
                                                              status_code=200,
                                                              _required_fields=required_fields,
                                                              additional='/{id}'))


@allure.feature("CALL CENTER")
@allure.story("Preset query service")
@pytest.mark.nightly
@pytest.mark.order(3)
@pytest.mark.xdist_group(name="preset query service")
def test__call_center__preset_query_by_id__PATCH_200():
    data = {
        "description": f"DO NOT DELETE PLEASE ({timestamp})",
    }

    required_fields = ['created_at', 'description', 'id', 'name', 'preset', 'section', 'updated_at']
    request = Webitel(obf_endpoint=PRESET_QUERY_SERVICE+'/{id}')
    response = request.patch(endpoint=PRESET_QUERY_SERVICE+f'/{PRESET_QUERY_SERVICE_ID}', data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=PRESET_QUERY_SERVICE,
                                                              method='PATCH',
                                                              status_code=200,
                                                              _required_fields=required_fields,
                                                              additional='/{id}'))


@allure.feature("CALL CENTER")
@allure.story("Preset query service")
@pytest.mark.nightly
@pytest.mark.order(4)
@pytest.mark.xdist_group(name="preset query service")
def test__call_center__preset_query_by_id__DELETE_200():
    DELETE_ID = get_id_call_center__preset_query_DELETE()
    request = Webitel(obf_endpoint=PRESET_QUERY_SERVICE+'/{id}')
    response = request.delete(endpoint=PRESET_QUERY_SERVICE+f'/{DELETE_ID}')
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=PRESET_QUERY_SERVICE,
                                                              method='DELETE',
                                                              status_code=200,
                                                              additional='/{id}'))