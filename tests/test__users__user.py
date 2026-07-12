import pytest
import allure
from utils.helpers import endpoint_schema, validate_schema
from utils.request_helper import Webitel
from utils.endpoints import USER
from config import USER_ID


@allure.feature("USERS")
@allure.story("User")
@pytest.mark.smoke
@pytest.mark.nightly
def test__user__GET_200():
    """
    get user data
    """
    request = Webitel(obf_endpoint=USER)
    response = request.get(endpoint=USER)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=USER, method='GET', status_code=200))


@allure.feature("USERS")
@allure.story("User")
@pytest.mark.smoke
@pytest.mark.nightly
def test__user_by_id__GET_200():
    """
    get user data by user id
    """
    request = Webitel(obf_endpoint=USER)
    response = request.get(endpoint=USER, _params={'id': USER_ID})
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=USER, method='GET', status_code=200))
