import pytest
import allure
from datetime import datetime
from utils.helpers import endpoint_schema, validate_schema
from utils.request_helper import Webitel
from utils.request_utils import get_skill_id_for_delete, get_agent_skill_row_for_skill_id
from utils.endpoints import CALL_CENTER, SKILLS, AGENTS
from config import SKILLS_PARAMS, AGENTS_PARAMS


@allure.feature("CALL CENTER")
@allure.story("Skills Service")
@pytest.mark.nightly
@pytest.mark.order()
def test__call_center__skills__GET_200():
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS)
    response = request.get(endpoint=CALL_CENTER+SKILLS, _params={'size': 5000})
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+SKILLS,
                                                              method='GET',
                                                              status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Skills Service")
@pytest.mark.nightly
@pytest.mark.order(1)
@pytest.mark.xdist_group(name="skills service")
def test__call_center__skills__POST_200():
    number = int(datetime.timestamp(datetime.now()))
    data = {"name": f"aqa_delete_this_{number}","description":"delete_this"}
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS)
    response = request.post(endpoint=CALL_CENTER+SKILLS, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+SKILLS,
                                                              method='POST',
                                                              status_code=200))


@allure.feature("CALL CENTER")
@allure.story("Skills Service")
@pytest.mark.nightly
@pytest.mark.order()
def test__call_center__skills_by_id__GET_200():
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS+'/{id}')
    response = request.get(endpoint=CALL_CENTER+SKILLS+f'/{SKILLS_PARAMS['id']}')
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+SKILLS,
                                                              method='GET',
                                                              status_code=200,
                                                              additional='/{id}'))


@allure.feature("CALL CENTER")
@allure.story("Skills Service")
@pytest.mark.nightly
@pytest.mark.order()
def test__call_center__skills_by_id__PUT_200():
    number = int(datetime.timestamp(datetime.now()))
    data = {"name": SKILLS_PARAMS['name'], "description": f"this skill for a-tests __changed_at__ {number}"}
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS+'/{id}')
    response = request.put(endpoint=CALL_CENTER+SKILLS+f'/{SKILLS_PARAMS['id']}', data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+SKILLS,
                                                              method='PUT',
                                                              status_code=200,
                                                              additional='/{id}'))


@allure.feature("CALL CENTER")
@allure.story("Skills Service")
@pytest.mark.nightly
@pytest.mark.order(2)
@pytest.mark.xdist_group(name="skills service")
def test__call_center__skills__delete_by_id__DELETE_200():
    try:
        delete_id = get_skill_id_for_delete()
    except Exception as e:
        raise Exception("Need create skill for deleting") from None
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS+'/{id}')
    response = request.delete(endpoint=CALL_CENTER+SKILLS+f'/{delete_id}')
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+SKILLS,
                                                              method='DELETE',
                                                              status_code=200,
                                                              additional='/{id}'))


@allure.feature("CALL CENTER")
@allure.story("Skills Service")
@pytest.mark.nightly
@pytest.mark.order()
def test__call_center__skills_by_id_agents__GET_200():
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS+'/{skill_id}'+AGENTS)
    response = request.get(endpoint=CALL_CENTER+SKILLS+f'/{SKILLS_PARAMS['id']}'+AGENTS)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+SKILLS,
                                                              method='GET',
                                                              status_code=200,
                                                              additional='/{skill_id}'+AGENTS))


@allure.feature("CALL CENTER")
@allure.story("Skills Service")
@pytest.mark.nightly
@pytest.mark.order(3)
@pytest.mark.xdist_group(name="skills service agents")
def test__call_center__skills_by_id_agents__POST_200():
    data = {"agent": [{"id": f"{AGENTS_PARAMS['id']}", "name": f"{AGENTS_PARAMS['name']}"}],
            "capacity": 2,
            "enabled": False}
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS+'/{skill_id}'+AGENTS)
    response = request.post(endpoint=CALL_CENTER+SKILLS+f"/{SKILLS_PARAMS['id']}"+AGENTS, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+SKILLS,
                                                              method='POST',
                                                              status_code=200,
                                                              additional='/{skill_id}'+AGENTS))


@allure.feature("CALL CENTER")
@allure.story("Skills Service")
@pytest.mark.nightly
@pytest.mark.order(4)
@pytest.mark.xdist_group(name="skills service agents")
def test__call_center__skills_by_id_agents__PATCH_200():
    data = {"enabled": True}
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS+'/{skill_id}'+AGENTS)
    response = request.patch(endpoint=CALL_CENTER+SKILLS+f"/{SKILLS_PARAMS['id']}"+AGENTS, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+SKILLS,
                                                              method='PATCH',
                                                              status_code=200,
                                                              additional='/{skill_id}'+AGENTS))


@allure.feature("CALL CENTER")
@allure.story("Skills Service")
@pytest.mark.nightly
@pytest.mark.order(5)
@pytest.mark.xdist_group(name="skills service agents")
def test__call_center__skills_by_id_agents__DELETE_200():
    agent_skill_row = get_agent_skill_row_for_skill_id()
    data = {"agent_id": [f"{AGENTS_PARAMS['id']}"],"id": [f"{agent_skill_row}"]}
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS+'/{skill_id}'+AGENTS)
    response = request.delete(endpoint=CALL_CENTER+SKILLS+f"/{SKILLS_PARAMS['id']}"+AGENTS, data=data)
    assert response.status_code == 200
    validate_schema(instance=response.json(), schema=endpoint_schema(endpoint=CALL_CENTER+SKILLS,
                                                              method='DELETE',
                                                              status_code=200,
                                                              additional='/{skill_id}'+AGENTS))
