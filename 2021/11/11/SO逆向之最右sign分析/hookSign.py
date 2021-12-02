#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
# Python 2.x & 3.x compatible
# from distutils.log import warn as print

import sys
import frida
import codecs
import threading
import time
import re
import base64
import json

from flask import Flask, jsonify, request

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


global gScript

HOOK_JS = './agent/zuiyouSign.js'

ZY_NAME = u'最右'
ZY_FRONTBOARD = 'cn.xiaochuankeji.tieba'
    
def bytesToHexString(bs):
    return ''.join(['%02X ' % b for b in bs])

#系统标准输出，支持grep
def outWrite(text):
    sys.stdout.write((text.encode('utf8') + b'\n' ).decode());

#带颜色打印输出
def colorPrint(color, s):
    return "%s[31;%dm%s%s[0m" % (chr(27), color, s , chr(27))

#获取第一个USB连接的设备
def get_usb_iphone():
    Type = 'usb'
    if int(frida.__version__.split('.')[0]) < 12:
        Type = 'tether'
        
    device_manager = frida.get_device_manager()
    changed = threading.Event()

    def on_changed():
        changed.set()

    device_manager.on('changed', on_changed)

    device = None
    while device is None:
        devices = [dev for dev in device_manager.enumerate_devices() if dev.type == Type]
        if len(devices) == 0:
            print ('Waiting for USB device...')
            changed.wait()
        else:
            device = devices[0]

    device_manager.off('changed', on_changed)

    return device

#枚举运行进程信息
def listRunningProcess():
    device = get_usb_iphone();
    processes = device.enumerate_processes();
    processes.sort(key = lambda item : item.pid)
    outWrite('%-10s\t%s' % ('pid', 'name'))
    for process in processes:
        outWrite('%-10s\t%s' % (str(process.pid),process.name))

#枚举某个进程的所有模块信息
def listModulesoOfProcess(session):
    moduels = session.enumerate_modules()
    moduels.sort(key = lambda item : item.base_address)
    for module in moduels:
        outWrite('%-40s\t%-10s\t%-10s\t%s' % (module.name, hex(module.base_address), hex(module.size), module.path))
    session.detach()

#从JS接受信息
def on_message(message, data):
    print(message)
    if message.has_key('payload'):
        payload = message['payload']
        if isinstance(payload, dict):
            deal_message(payload)
        else:
            print (payload)

#加载JS文件脚本
def loadJsFile(session, filename):
    source = ''
    with codecs.open(filename, 'r', 'utf-8') as f:
        source = source + f.read()
    script = session.create_script(source)
    script.on('message', on_message)
    #接收js脚本的消息
    script.load()
    return script


app = Flask(__name__)

@app.route('/aesenc', methods=['POST']) # 数据加密
def zy_aesenc():
    global gScript
    data = request.get_data()    
    res = gScript.exports.callencaes(data.decode("utf-8"))
    return res

@app.route('/aesdec', methods=['POST']) # 数据解密
def zy_aesdec():
    global gScript

    data = request.get_data()
    res = gScript.exports.calldecaes(data.decode("utf-8"))
    return res

@app.route('/sign', methods=['POST']) # 数据签名
def zy_sign():
    global gScript

    data = request.get_data()
    print(data.decode("utf-8"))        

    res = gScript.exports.callsignfun('http://api.izuiyou.com/',data.decode("utf-8"))
    return res

@app.route('/setkey', methods=['POST']) # 设置key
def zy_setKey():
    global gScript

    data = request.get_data()
    res = gScript.exports.callsetkey(data);
    return res

@app.route('/getkey')   # 获取当前key
def zy_getKey():
    global gScript

    res = gScript.exports.callgetkey()
    return res

def main():
    global session
    global appname
    global gScript
    
    # 1. 获取USB设备
    device = get_usb_iphone()
    if len(sys.argv)>2:
        appname = sys.argv[2]
    else:
        appname = ZY_NAME

    print('设备信息:' + str(device))
    if sys.argv[1]=='ps':
        # 枚举运行进程信息
        print ('ps')
        listRunningProcess()
    elif sys.argv[1]=='hook':
        # 动态Hook
        print ('zyhook')

        pid = device.spawn(ZY_FRONTBOARD)
        session = device.attach(pid)
        print("[*] Attach Application id:",pid)

        device.resume(pid)
        print("[*] Application onResume")

        gScript = loadJsFile(session, HOOK_JS)
        # sys.stdin.read()

    # 启动web服务
    app.run()        

    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if session:
            session.detach()
        sys.exit()
    else:
        pass
    finally:
        pass
