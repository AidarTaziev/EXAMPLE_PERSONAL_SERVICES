import requests
import logging
from django.conf import settings
from json import JSONDecodeError

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, filename=u'erp.log')


class ERPWrapper:
    status_code_error_encode = {
        500: "В данный момент на сервере 1С ведутся технические работы. Повтороите попытку позже.",
        401: "Ошибка авторизации",
    }

    def __init__(self, url, method, user=None, data=None, user_dict=None):
        self.method = method
        self.data = data if data else {}
        self.response_status_code = None
        self.url = url.encode('utf-8')
        self.username = None
        self.password = None
        if user:
            self.username = user.username.encode('utf-8')
            self.password = user.erp_password.encode('utf-8')

        if user_dict:
            self.username = user_dict.get('username').encode('utf-8')
            self.password = user_dict.get('password').encode('utf-8')

    def make_erp_request(self):
        try:
            logging.debug('---------------------------REQUEST----------------------------')
            logging.debug("Request to 1C: url - {url}, data - {data}".format(url=self.url.decode('utf-8'), data=self.data))

            if self.username and self.password:
                if self.method == "GET":
                    response = requests.request(self.method, url=self.url, params=self.data,
                                                auth=(self.username, self.password), timeout=15, verify=False)
                else:
                    response = requests.request(self.method, url=self.url, json=self.data,
                                                auth=(self.username, self.password),  verify=False)
            else:
                if self.method == "GET":
                    response = requests.request(self.method, url=self.url, params=self.data, timeout=15, verify=False)
                else:
                    response = requests.request(self.method, url=self.url, json=self.data, timeout=15, verify=False)

            logging.debug("1C received content  - {content} \n ... \n ".format(content=str(response.text)[:80]))
            logging.debug("1C received headers  - {headers}".format(headers=response.headers))

        except requests.RequestException as ex:
            logging.debug('1C request exception - {ex}'.format(ex=ex))

            self.response_status_code = 500

            return {'error': True, 'report': 'Ошибка подключения к серверу 1C ERP'}, {}

        self.response_status_code = response.status_code

        data, headers = self.get_response_data(response)

        return data, headers

    def get_response_data(self, response):
        if response.status_code == 401:
            return {'error': True, 'report': 'Ошибка авторизации'}, response.headers

        if response.status_code == 500:
            return {
                       'error': True,
                       'report': 'В данный момент на сервере 1С ведутся технические работы. Повторите попытку позже.'

                   }, response.headers

        if response.status_code == 200 and not 'application/json' in response.headers['Content-Type']:
            return response.content, response.headers

        try:
            data = response.json()
        except:
            data = {'error': True,
                    'report': 'В данный момент на сервере 1С ведутся технические работы. Повторите попытку позже.',
                    'details': response.content.decode('utf-8')
                    }

        return data, response.headers


def make_request_personal(path, data):
    data['token'] = settings.TRACKING_TOKEN

    url = settings.TRACKING_DOMAIN + path
    print(data)
    response = requests.request(method="POST", url=url, data=data)
    print(url, response.text)
    try:
        data = response.json()

    except JSONDecodeError as error:
        return True, "Ошибка сервера отслеживания"

    if response.status_code != 200:
        return True, data.get("error", "Ошибка сервера")

    return False, data or []
