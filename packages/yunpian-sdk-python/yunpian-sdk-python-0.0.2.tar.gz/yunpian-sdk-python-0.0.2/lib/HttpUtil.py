# -*- coding:utf-8 -*-
# filename:HttpUtil
# 16/1/20 下午3:25
from lib.Config import yunpian_config
from lib.Sign import Sign

__author__ = 'bingone'

import platform

import requests
from lib.model.Result import Result

_sys_info = '{0}; {1}'.format(platform.system(), platform.machine())
_python_ver = platform.python_version()

_session = None
_headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}


def _init():
    pass


def request_post(url, data=None):
    pass
    if not data:
        return Result(data, None, '参数为空')
    if data.has_key('encrypt'):
        data[Sign.singName] = Sign.getSign(data, yunpian_config['API_SECRET'])
    return real_post(url, data)


def real_post(url, data=None, retry=3):
    if _session is None:
        _init()
    try:
        r = requests.post(
            url, data=data, headers=_headers, timeout=5)
    except Exception as e:
        if retry > 0:
            return real_post(url, data, retry - 1)
        else:
            return Result(data, None, e)
    return Result(data, r)


if __name__ == '__main__':
    pass

    filetxt = open('/Users/bingone/develop/tools/reissue.txt', 'r')
    for txt in filetxt.readlines():
        pass
        text = txt.split('\t')[1]
        mobile = txt.split('\t')[0]
        # print 'mobile=',mobile,'txt=',text
        # result = real_post('https://sms.yunpian.com/v1/sms/send.json',
        #                    data={'apikey': '592662792b81f6a87f62d7a2059005b5', 'mobile': mobile, 'text': text})
        # import sys,json
        # reload(sys)
        # sys.setdefaultencoding('utf-8')
        # print json.dumps(result.content, ensure_ascii=False)
