from utils.request_helper import Webitel
from utils.endpoints import (CALL_CENTER, PRESET_QUERY_SERVICE, USERINFO, LOGIN, LOGOUT, USERS, SETTINGS, DEVICES,
                             SKILLS, AGENTS)
from utils.file_helper import write_json_file, read_json_file
from config import (PRESET_QUERY_SERVICE_ID, USER_new_pass_DATA, P, C_FILE, SYSTEM_SETTINGS_PASSWORD,
                    SYSTEM_SETTINGS_2FA, USER_ID, SKILLS_PARAMS, AGENTS_PARAMS)


def get_id_call_center__preset_query_DELETE():
    request = Webitel(obf_endpoint=CALL_CENTER+PRESET_QUERY_SERVICE)
    response = request.get(endpoint=CALL_CENTER+PRESET_QUERY_SERVICE, _params={'size': 5000}, attachments=False)
    data = response.json()
    items = data['items']
    for item in items:
        if item['id'] != PRESET_QUERY_SERVICE_ID:
            return item['id']
        else:
            continue


def get_user_id_by_access_token(access_token):
    params = {'access_token': access_token}
    request = Webitel(obf_endpoint=USERINFO, custom_header={'X-Webitel-Access': access_token})
    response = request.get(endpoint=USERINFO, _params=params, attachments=False)
    data = response.json()
    user_id = data['user_id']
    return user_id


def do_login(password, username, domain):
    data = {"password": password, "username": f"{username}@{domain}"}
    request_login = Webitel(obf_endpoint=LOGIN, custom_header="clear")
    response_login = request_login.post(endpoint=LOGIN, data=data, allow_redirects=True, attachments=False)
    resp_code = response_login.status_code
    response = response_login.json()
    response['code'] = resp_code
    return response


def do_logout(user_id = None):
    _user_id = USER_ID if user_id is None else user_id
    data = {"id": str(_user_id)}
    request_logout = Webitel(obf_endpoint=LOGOUT, custom_header="clear")
    request_logout.post(endpoint=LOGOUT, data=data, allow_redirects=True, attachments=False)


def set_password_to_normal():
    user_data = USER_new_pass_DATA
    passwords_list = list(P.values())*2
    for p in passwords_list:
        data = {"password": p, "username": user_data['new_pass']['username'],
                "license": [{"id": f"{user_data['new_pass']['license_id']}"}],}
        request_set_password_to_normal = Webitel(obf_endpoint=USERS + "/{id}", custom_header={'X-Webitel-Access': user_data['access_token']})
        request_set_password_to_normal.put(endpoint=f"{USERS}/{user_data['new_pass']['user_id']}", data=data, attachments=False)
    counter_data = read_json_file(C_FILE)
    counter_data["p_o"] = "7"
    counter_data["p_n"] = "8"
    write_json_file(C_FILE, counter_data)
    do_logout()


def set_system_settings():
    settings = SYSTEM_SETTINGS_PASSWORD
    for setting in settings:
        request_set_system_settings = Webitel(obf_endpoint=SETTINGS + '{id}')
        request_set_system_settings.put(endpoint=f'{SETTINGS}/{setting['id']}', data={"value": setting['value']}, attachments=False)
    do_logout()


def set_2fa(c):
    settings = SYSTEM_SETTINGS_2FA
    request = Webitel(obf_endpoint=SETTINGS + '{id}')
    request.put(endpoint=f'{SETTINGS}/{settings['id']}', data={"value": c}, attachments=False)
    do_logout()


def get_devices(**kwargs):
    params = kwargs
    request = Webitel(obf_endpoint=DEVICES)
    response_devices = request.get(endpoint=DEVICES, _params=params, attachments=False)
    return response_devices.json()


def get_device_for_delete():
    name = f"aqa_delete*"
    params = {"size":1000, "name":name}
    devices = get_devices(**params)
    try:
        device_id = [i['id'] for i in devices['items']][0]
        return device_id
    except Exception as e:
        raise e


def get_skills(**kwargs):
    params = kwargs
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS)
    response = request.get(endpoint=CALL_CENTER+SKILLS, _params=params, attachments=False)
    return response.json()


def get_skill_id_for_delete():
    name = f"aqa_delete*"
    params = {"size":1000, "q":name}
    skills = get_skills(**params)
    try:
        skill_id = [i['id'] for i in skills['items']][0]
        return skill_id
    except Exception as e:
        raise e


def get_agents_for_skill_id(skill_id=None):
    s_id = skill_id if skill_id is not None else f'{SKILLS_PARAMS['id']}'
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS+'/{skill_id}'+AGENTS)
    response = request.get(endpoint=CALL_CENTER+SKILLS+f'/{s_id}'+AGENTS, attachments=False)
    return response.json()


def get_agent_skill_row_for_skill_id(skill_id=None, agent_id=None):
    a_id = agent_id if agent_id is not None else f'{SKILLS_PARAMS['agent']['id']}'
    r = get_agents_for_skill_id(skill_id=skill_id)
    if 'items' in r:
        for i in r['items']:
            if i['agent']['id'] == str(a_id):
                s_id = i['id']
        return s_id
    else:
        raise Exception("No Agents added for this skill")


def delete_skill_for_agent(skill_id, s_id, agent_id):
    data = {"agent_id": [f"{agent_id}"], "id": [f"{s_id}"]}
    request = Webitel(obf_endpoint=CALL_CENTER+SKILLS+'/{skill_id}'+AGENTS)
    request.delete(endpoint=CALL_CENTER+SKILLS+f'/{skill_id}'+AGENTS, data=data, attachments=False)


def clear_agent_skill():
    r = get_agents_for_skill_id()
    if 'items' in r:
        s_id = r['items'][0]['id']
        delete_skill_for_agent(skill_id=SKILLS_PARAMS['id'], s_id=s_id, agent_id=SKILLS_PARAMS['agent']['id'])

def add_skill_for_agent():
    data = {"capacity": 7, "skill": {"id": SKILLS_PARAMS['id'],"name": SKILLS_PARAMS['name']}}
    request = Webitel(obf_endpoint=CALL_CENTER+AGENTS+'/{agent_id}'+SKILLS)
    response = request.post(endpoint=CALL_CENTER+AGENTS+f'/{AGENTS_PARAMS['id']}'+SKILLS, data=data, attachments=False)
    return response.json()