# coding: utf-8
from decimal import Decimal
from hashlib import md5

import requests


PROXY_DETECTION_URL = 'https://minfraud.maxmind.com/app/ipauth_http'
FRAUD_DETECTION_URL = 'https://minfraud.maxmind.com/app/ccv2r'


def parse_response(response):
    return dict(f.split('=') for f in response.text.split(';'))


class MaxMindAPI(object):

    def __init__(self, license_key):
        self.license_key = license_key

    def detect_fraud(self, ip_address, city=None, region=None, postal=None, country=None, email=None, phone=None,
                     user_agent=None):
        params = {'i': ip_address, 'license_key': self.license_key}
        if city:
            params['city'] = city
        if region:
            params['region'] = region
        if postal:
            params['postal'] = postal
        if country:
            params['country'] = country
        if email:
            params['domain'] = email.split('@')[1]
            params['emailMD5'] = md5(email).hexdigest()
        if phone:
            params['custPhone'] = phone
        if user_agent:
            params['user_agent'] = user_agent
        response = requests.get(FRAUD_DETECTION_URL, params=params)
        return Decimal(parse_response(response)['riskScore'])
