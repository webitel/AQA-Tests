import json
import allure
import requests

from config import BASE_URL, TOKEN, HEADERS
from utils.helpers import _json_serializable, obfuscate_control


class Attachments:
    def __init__(self, obfuscate=True, obf_endpoint=''):
        self.obfuscate = obfuscate
        self.obf_endpoint = obf_endpoint

    def get_attachments(self, r,):
        data = obfuscate_control(self.obfuscate, r, self.obf_endpoint)
        req_headers_dict = dict(r.request.headers)
        req_headers_dict.update({'X-Webitel-Access': 'X-Webitel-Access'})

        allure.attach(data["url"], 'URL', allure.attachment_type.TEXT)
        allure.attach('GET', 'Method', allure.attachment_type.TEXT)
        allure.attach(json.dumps(req_headers_dict, indent=4), 'Request headers', allure.attachment_type.JSON)
        allure.attach(json.dumps(dict(r.headers), indent=4), 'Response headers', allure.attachment_type.JSON)
        self._allure_attach__response_body(data)

    def post_attachments(self, r):
        data = obfuscate_control(self.obfuscate, r, self.obf_endpoint)
        req_headers_dict = dict(r.request.headers)
        req_headers_dict.update({'X-Webitel-Access': 'X-Webitel-Access'})

        allure.attach(data["url"], 'URL', allure.attachment_type.TEXT)
        allure.attach('POST', 'Method', allure.attachment_type.TEXT)
        allure.attach(json.dumps(req_headers_dict, indent=4), 'Request headers', allure.attachment_type.JSON)
        self._allure_attach__request_body(data)
        allure.attach(json.dumps(dict(r.headers), indent=4), 'Response headers', allure.attachment_type.JSON)
        self._allure_attach__response_body(data)


    def put_attachments(self, r):
        data = obfuscate_control(self.obfuscate, r, self.obf_endpoint)
        req_headers_dict = dict(r.request.headers)
        req_headers_dict.update({'X-Webitel-Access': 'X-Webitel-Access'})

        allure.attach(data["url"], 'URL', allure.attachment_type.TEXT)
        allure.attach('PUT', 'Method', allure.attachment_type.TEXT)
        allure.attach(json.dumps(req_headers_dict, indent=4), 'Request headers', allure.attachment_type.JSON)
        self._allure_attach__request_body(data)
        allure.attach(json.dumps(dict(r.headers), indent=4), 'Response headers', allure.attachment_type.JSON)
        self._allure_attach__response_body(data)


    def patch_attachments(self, r):
        data = obfuscate_control(self.obfuscate, r, self.obf_endpoint)
        req_headers_dict = dict(r.request.headers)
        req_headers_dict.update({'X-Webitel-Access': 'X-Webitel-Access'})

        allure.attach(data["url"], 'URL', allure.attachment_type.TEXT)
        allure.attach('PATCH', 'Method', allure.attachment_type.TEXT)
        allure.attach(json.dumps(req_headers_dict, indent=4), 'Request headers', allure.attachment_type.JSON)
        self._allure_attach__request_body(data)
        allure.attach(json.dumps(dict(r.headers), indent=4), 'Response headers', allure.attachment_type.JSON)
        self._allure_attach__response_body(data)


    def delete_attachments(self, r):
        data = obfuscate_control(self.obfuscate, r, self.obf_endpoint)
        req_headers_dict = dict(r.request.headers)
        req_headers_dict.update({'X-Webitel-Access': 'X-Webitel-Access'})

        allure.attach(data["url"], 'URL', allure.attachment_type.TEXT)
        allure.attach('DELETE', 'Method', allure.attachment_type.TEXT)
        allure.attach(json.dumps(req_headers_dict, indent=4), 'Request headers', allure.attachment_type.JSON)
        self._allure_attach__request_body(data)
        allure.attach(json.dumps(dict(r.headers), indent=4), 'Response headers', allure.attachment_type.JSON)
        self._allure_attach__response_body(data)

    @staticmethod
    def _allure_attach__request_body(data):
        try:
            allure.attach(json.dumps(data["request_body"], indent=4), 'Request body', allure.attachment_type.JSON)
        except:
            allure.attach(data["request_body"], 'Request body', allure.attachment_type.TEXT)

    @staticmethod
    def _allure_attach__response_body(data):
        try:
            allure.attach(json.dumps(data["response_body"], indent=4), 'Response body', allure.attachment_type.JSON)
        except:
            allure.attach(data["response_body"], 'Response body', allure.attachment_type.TEXT)


class Webitel(Attachments):
    def __init__(self, custom_header=None, obfuscate=True, obf_endpoint=False, *args, **kwargs):
        super(Webitel, self).__init__(obfuscate=obfuscate, obf_endpoint=obf_endpoint)
        self.args = args
        self.kwargs = kwargs
        self.custom_header = custom_header

    def get(self, endpoint='', _params = None, attachments=True):
        response = requests.get(url=BASE_URL + endpoint, headers=self._get_headers(), params=_params)
        if attachments:
            self.get_attachments(response)
        self._check_json_serializable(response)
        return response

    def post(self, endpoint, data: dict = {}, _params = None, attachments=True, *args, **kwargs):
        response = requests.post(url=BASE_URL + endpoint, data=json.dumps(data), headers=self._get_headers(), params=_params)
        if attachments:
            self.post_attachments(response)
        self._check_json_serializable(response)
        return response

    def put(self, endpoint, data: dict = {}, _params = None, attachments=True):
        response = requests.put(url=BASE_URL + endpoint, data=json.dumps(data), headers=self._get_headers(), params=_params)
        if attachments:
            self.put_attachments(response)
        self._check_json_serializable(response)
        return response

    def patch(self, endpoint, data: dict = {}, _params = None, attachments=True):
        response = requests.patch(url=BASE_URL + endpoint, data=json.dumps(data), headers=self._get_headers(), params=_params)
        if attachments:
            self.patch_attachments(response)
        self._check_json_serializable(response)
        return response

    def delete(self, endpoint, data: dict = {}, attachments=True, **kwargs):
        response = requests.delete(url=BASE_URL + endpoint, headers=self._get_headers())
        if attachments:
            self.delete_attachments(response)
        self._check_json_serializable(response)
        return response

    def _get_headers(self):
        if self.custom_header is None:
            headers = HEADERS.copy()
            headers['X-Webitel-Access'] = TOKEN
            return headers
        elif self.custom_header in ["clear", "CLEAR", "Clear"]:
            return HEADERS
        else:
            headers = HEADERS.copy()
            for k,v in self.custom_header.items():
                headers[k] = v
            return headers

    @staticmethod
    def _check_json_serializable(response):
        if not _json_serializable(response.text):
            raise AssertionError("Unable to serialize response to json\n" + response.text)
