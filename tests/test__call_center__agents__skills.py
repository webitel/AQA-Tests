import pytest
import allure

from config import AGENTS_PARAMS, SKILLS_PARAMS
from utils.helpers import endpoint_schema, validate_schema
from utils.request_utils import get_agent_skill_row_for_skill_id
from utils.request_helper import Webitel
from utils.endpoints import CALL_CENTER, AGENTS, SKILLS, BULK


@allure.feature("CALL CENTER")
@allure.story("Agents")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__call_center__agents_by_id__skills__GET_200():
    request = Webitel(obf_endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS)
    response = request.get(endpoint=CALL_CENTER+AGENTS+f'/{AGENTS_PARAMS['id']}'+SKILLS, _params={'size': 5000})
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS,
                                                              method='GET',
                                                              status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Agents")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(1)
@pytest.mark.xdist_group(name="agents service skills")
def test__call_center__agents_by_id__skills__POST_200():
    data = {"capacity": 7, "skill": {"id": SKILLS_PARAMS['id'],"name": SKILLS_PARAMS['name']}}
    request = Webitel(obf_endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS)
    response = request.post(endpoint=CALL_CENTER+AGENTS+f'/{AGENTS_PARAMS['id']}'+SKILLS, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(),
                    schema=endpoint_schema(endpoint=CALL_CENTER + AGENTS + '/{agent_id}' + SKILLS,
                                           method='POST',
                                           status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Agents")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(2)
@pytest.mark.xdist_group(name="agents service skills")
def test__call_center__agents_by_id__skills__PATCH_200():
    data = {"capacity": 4, "enabled": False, "skill_id": [f"{SKILLS_PARAMS['id']}"]}
    request = Webitel(obf_endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS)
    response = request.patch(endpoint=CALL_CENTER+AGENTS+f'/{AGENTS_PARAMS['id']}'+SKILLS, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(),
                    schema=endpoint_schema(endpoint=CALL_CENTER + AGENTS + '/{agent_id}' + SKILLS,
                                           method='PATCH',
                                           status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Agents")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(3)
@pytest.mark.xdist_group(name="agents service skills")
def test__call_center__agents_by_id__skills__DELETE_200():
    request = Webitel(obf_endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS)
    response = request.delete(endpoint=CALL_CENTER+AGENTS+f'/{SKILLS_PARAMS['agent']['id']}'+SKILLS)
    assert response.status_code == 200
    validate_schema(instance=response.json(),
                    schema=endpoint_schema(endpoint=CALL_CENTER + AGENTS + '/{agent_id}' + SKILLS,
                                           method='DELETE',
                                           status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Agents")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(4)
@pytest.mark.xdist_group(name="agents service skills")
def test__call_center__agents_by_id__skills__bulk__POST_200():
    data = {"items": [{"capacity": 3,
                       "skill": {"id": f'{SKILLS_PARAMS['id']}',
                                 "name": f"{SKILLS_PARAMS['name']}"}}]}
    request = Webitel(obf_endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS+BULK)
    response = request.post(endpoint=CALL_CENTER+AGENTS+f'/{SKILLS_PARAMS['agent']['id']}'+SKILLS+BULK, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(),
                    schema=endpoint_schema(endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS+BULK,
                                           method='POST',
                                           status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Agents")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__call_center__agents_by_id__skills_by_id__GET_200():
    request = Webitel(obf_endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS+'/{id}')
    response = request.get(endpoint=CALL_CENTER+AGENTS+f'/{AGENTS_PARAMS['id']}'+SKILLS+f'/{AGENTS_PARAMS['skill']['row_id']}',
                           _params={'size': 5000})
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS+'/{id}',
                                                              method='GET',
                                                              status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Agents")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__call_center__agents_by_id__skills_by_id__PUT_200():
    data = {"capacity": 6,
            "enabled": True,
            "skill": {"id": f"{AGENTS_PARAMS['skill']['id']}",
                      "name": f"{AGENTS_PARAMS['skill']['name']}"}}
    request = Webitel(obf_endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS+'/{id}')
    response = request.put(endpoint=CALL_CENTER+AGENTS+f'/{AGENTS_PARAMS['id']}'+SKILLS+f'/{AGENTS_PARAMS['skill']['row_id']}', data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(),
                    schema=endpoint_schema(endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS+'/{id}',
                                           method='PUT',
                                           status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Agents")
# @pytest.mark.smoke
@pytest.mark.nightly
def test__call_center__agents_by_id__skills_by_id__PATCH_200():
    data = {"capacity": 7,
            "enabled": True,
            "skill": {"id": f"{AGENTS_PARAMS['skill']['id']}",
                      "name": f"{AGENTS_PARAMS['skill']['name']}"}}
    request = Webitel(obf_endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS+'/{id}')
    response = request.patch(endpoint=CALL_CENTER+AGENTS+f'/{AGENTS_PARAMS['id']}'+SKILLS+f'/{AGENTS_PARAMS['skill']['row_id']}', data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(),
                    schema=endpoint_schema(endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS+'/{id}',
                                           method='PATCH',
                                           status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Agents")
# @pytest.mark.smoke
@pytest.mark.nightly
@pytest.mark.order(5)
@pytest.mark.xdist_group(name="agents service skills")
def test__call_center__agents_by_id__skills_by_id__DELETE_200():
    row_id = get_agent_skill_row_for_skill_id(skill_id=SKILLS_PARAMS['id'], agent_id=SKILLS_PARAMS['agent']['id'])
    request = Webitel(obf_endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS+'/{id}')
    response = request.delete(endpoint=CALL_CENTER+AGENTS+f'/{SKILLS_PARAMS['agent']['id']}'+SKILLS+f'/{row_id}')
    assert response.status_code == 200
    validate_schema(instance=response.json(),
                    schema=endpoint_schema(endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS+'/{id}',
                                           method='DELETE',
                                           status_code=200))