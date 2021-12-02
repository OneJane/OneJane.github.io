#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
# Python 2.x & 3.x compatible
# from distutils.log import warn as print

import sys
import requests
from requests import RequestException
import hashlib
import time
import json

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

def get_frida_rpc(url,msg):
    try:
        r = requests.post(url,data=msg.encode('utf-8'))
        # 这里可以做一些返回值的错误处理                          
        return r.text
    except RequestException as e:
        print(e)
                          
# 首页推荐内容解析
def dataAesEnc(msg):
    return get_frida_rpc('http://127.0.0.1:5000/aesenc',msg)

def dataAesDec(msg):
    return get_frida_rpc('http://127.0.0.1:5000/aesdec',msg)

def dataSign(msg):
    return get_frida_rpc('http://127.0.0.1:5000/sign',msg)

def dataGetKey():
    r  = requests.get('http://127.0.0.1:5000/getkey')
    return r.text

def dataSetKey(msg):
    return get_frida_rpc('http://127.0.0.1:5000/setkey',msg)
    

# 获取数据
def get_data(uri, msg):                          
    postData = dataAesEnc(msg)
    # print(postData)    
    sign = dataSign(postData)
    # print(sign)
    protocolKey = dataGetKey()
    # print(protocolKey)
    
    url = uri + str(sign)
    headers = { 'ZYP': 'mid=239631186',
                'X-Xc-Agent' : 'av=5.5.11,dt=0',
                'User-Agent': 'okhttp/3.12.2 Zuiyou/5.5.11 (Android/27)',
                'X-Xc-Proto-Req' : protocolKey,
                'Request-Type' : 'text/json',
                'Content-Type' : 'application/xcp',
                }
    # 将十六进制字符串转字节数组  b'/\x07\xc5\xf4\x143\xc2\xe1\x01...          
    byte_data = bytes.fromhex(postData) 
    # proxies = {'http': '127.0.0.1:8888',
    #  'https': '127.0.0.1:8888'
    #  }
    
    try:
        # ,proxies=proxies
        r = requests.post(url, headers=headers, data=byte_data, verify=False,stream=True,timeout=15)

        # print(r.headers['X-Xc-Proto-Res'])
        # key是 cat开头的就需要把返回包里面的duck key设置进去， 
        if protocolKey.find('cat') == 0:
            print(protocolKey)
            print(r.headers['X-Xc-Proto-Res'])
            dataSetKey(r.headers['X-Xc-Proto-Res'])
        # 这里要做一些错误处理        
        bufRc =  r.raw.read();
        rcStr = dataAesDec(bufRc.hex())
        rc = bytes.fromhex(rcStr).decode("utf-8")
        return rc

    except RequestException as e:
        print(e)
        
def main():
    # 手机端首页推荐地址
    uri = 'http://api.izuiyou.com/index/recommend?sign='
    msg = '{"filter":"all","auto":0,"tab":"推荐","direction":"down","c_types":[1,2,11,15,16,51,17,52,53,40,50,41,22,25,27],"sdk_ver":{"tt":"3.1.0.3","tx":"4.211.1081","bd":"5.86","mimo":"5.0.3","tt_aid":"5004095","tx_aid":"1106701465","bd_aid":"c8655095","mimo_aid":"2882303761518470184"},"ad_wakeup":1,"h_ua":"Mozilla\/5.0 (Linux; Android 8.1.0; Redmi 6A Build\/O11019; wv) AppleWebKit\/537.36 (KHTML, like Gecko) Version\/4.0 Chrome\/62.0.3202.84 Mobile Safari\/537.36","manufacturer":"Xiaomi","h_av":"5.5.11","h_dt":0,"h_os":27,"h_app":"zuiyou","h_model":"Redmi 6A","h_did":"866655030396869","h_nt":1,"h_m":239631186,"h_ch":"xiaomi","h_ts":1603179121590,"token":"T7K4Nnqg98_aFV9JwkfuiZtvPrRJ02EXxbnm7TXr3qiIWWaT1vjNNNCpcUu112TDw_VXu","android_id":"57b9b8465c2e440b","h_ids":{"imei2":"878739042239784","meid":"98001184062989","imei1":"878739042239776","imei":"98001184062989"},"h_os_type":"miui"}'
    
    items = get_data(uri, msg)
    print(items)
    
if __name__ == '__main__':
    j = 1
    while True:
        print("第{}次加载的段子\n".format(j))
        main()
        j += 1

        # 测试程序，加载3次
        if j >1 :
            break
        
    print("加载完毕")        
    
