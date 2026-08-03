import pytest
import allure

from config import AGENTS_PARAMS
from utils.helpers import endpoint_schema, validate_schema
from utils.request_helper import Webitel
from utils.endpoints import CALL_CENTER, AGENTS, SKILLS, LOOKUPS


@allure.feature("CALL CENTER")
@allure.story("Lookups")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__call_center__lookups__agent__skills__GET_200():
    request = Webitel(obf_endpoint=CALL_CENTER+LOOKUPS+AGENTS+SKILLS+'/{agent_id}')
    response = request.get(endpoint=CALL_CENTER+LOOKUPS+AGENTS+SKILLS+f'/{AGENTS_PARAMS['id']}', _params={'size': 5000})
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+LOOKUPS+AGENTS+SKILLS+'/{agent_id}',
                                                              method='GET',
                                                              status_code=200))