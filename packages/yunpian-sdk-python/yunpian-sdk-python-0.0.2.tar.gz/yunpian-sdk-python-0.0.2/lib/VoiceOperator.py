# -*- coding:utf-8 -*-
# filename:FlowOperator
# 16/1/20 下午5:11

__author__ = 'bingone'
from lib.Config import yunpian_config
from lib.model.Result import Result
from lib.HttpUtil import request_post


class VoiceOperator(object):
    def __init__(self, apikey=None, api_secret=None):
        if apikey == None:
            self.apikey = yunpian_config['APIKEY']
        if api_secret == None:
            self.api_secret = yunpian_config['API_SECRET']

    def pull_status(self, data={}):

        data['apikey'] = self.apikey;

        return request_post(yunpian_config['URI_PULL_VOICE_STATUS'], data)

    def send(self, data={}):
        if 'mobile' not in data:
            return Result(None, 'mobile 为空')
        if 'code' not in data:
            return Result(None, 'code 为空')
        data['apikey'] = self.apikey;

        return request_post(yunpian_config['URI_SEND_VOICE_SMS'], data)
