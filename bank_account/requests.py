#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests
from django.conf import settings


def get_user_bank_account_info(session_id, user_id=None):
    try:
        response = requests.post(settings.PASSPORT_USER_CREDENTIALS_URI, data={'session_id': session_id,
                                                                               'user_id': user_id,
                                                                               'secret': settings.PASSPORT_SECRET_KEY,})
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            if not data['error']:
                if 'account_info' in data['data']:
                    return response.status_code, data['data']['account_info']
        else:
            return response.status_code, response.json()
    except Exception as ex:
        logging.error(ex)
        return 500, None


def post_credit_requests(data):
    try:
        url = '{url}{urn}'.format(url=settings.PASSPORT_URL, urn=settings.CREDIT_REDIRECT_URN)
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except Exception as ex:
        logging.error(ex)
        return 500, None


def post_unlink_redirect_request(data):
    try:
        url = '{url}{urn}'.format(url=settings.PASSPORT_URL, urn=settings.UNLINK_REDIRECT_URN)
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except Exception as ex:
        logging.error(ex)
        return 500, None