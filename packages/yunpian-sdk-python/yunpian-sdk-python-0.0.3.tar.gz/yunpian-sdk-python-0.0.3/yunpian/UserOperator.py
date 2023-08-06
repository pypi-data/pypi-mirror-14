# -*- coding:utf-8 -*-
# filename:FlowOperator
# 16/1/20 下午5:10

__author__ = 'bingone'
from lib.Config import yunpian_config
from lib.HttpUtil import request_post


class UserOperator(object):
    def __init__(self, apikey=None, api_secret=None):
        if apikey == None:
            self.apikey = yunpian_config['APIKEY']
        if api_secret == None:
            self.api_secret = yunpian_config['API_SECRET']

    def get(self, data={}):

        data['apikey'] = self.apikey;

        return request_post(yunpian_config['URI_GET_USER_INFO'], data)

    def set(self, data={}):

        data['apikey'] = self.apikey;

        return request_post(yunpian_config['URI_SET_USER_INFO'], data)
