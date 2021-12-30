import time 
import frida
import requests
import json
import os


moduleid_list = []

def searchv2(param_str):
    headers = {
        'Source': 'source',
        'Date': 'Wed, 28 Jul 2021 11:02:48 GMT',
        'Authorization': 'hmac id="AKIDKpo6me25b14nzcNefQeoqR95syh2ayx97s0g", algorithm="hmac-sha1", headers="date source", signature="xUe79aim7V1Nur4J8DfN9KSDU0Q="',
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': '396',
        'Host': 'api.motuobang.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.14.9'
    }
    param_str = str(param_str).replace("\"","\\\"").replace("'", "\"")
    data = requests.post('http://api.motuobang.com/release/car/searchv2', data=param_str.encode(),
                     headers=headers).json()["data"]
    return json.loads(data)["serieslist"]

def seriesinfo(param_str):
    headers = {
        'Source': 'source',
        'Date': 'Mon, 26 Jul 2021 05:47:06 GMT',
        'Authorization': 'hmac id="AKIDKpo6me25b14nzcNefQeoqR95syh2ayx97s0g", algorithm="hmac-sha1", headers="date source", signature="jmwgtLvjj06A/M/TNcCqL72GRsk="',
        'Content-Type': 'application/json; charset=utf-8 ',
        'Content-Length': '403',
        'Host': 'api.motuobang.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.14.'
    }
    param_str = str(param_str).replace("\"","\\\"").replace("'", "\"")
    data = requests.post('http://api.motuobang.com/release/car/seriesinfo', data=param_str.encode(),
                     headers=headers).json()["data"]
    return json.loads(data)["seriesinfo"]


def my_message_handler(message, payload):
    if message["type"] == "send":  
        # print("payload如下:",message["payload"])
        payload = json.loads(message["payload"])
        if "searchcar" in payload:
            # searchv2
            print("searchv2")
            try:
                serials = searchv2(payload)
            except:
                print("error:",payload)  
                return  
            for s in serials:
                brandname = s['brandname']
                name = s['name']
                moduleid = s['modelid']
                print(moduleid)
                moduleid_list.append(str(moduleid))
        else:
            # seriesinfo
            print("seriesinfo")
            serialsinfo = seriesinfo(payload)
            pdfurl = serialsinfo["pdfurl"]
            name = serialsinfo["name"]
            brandname = serialsinfo["brandname"]
            if not pdfurl.isspace(): #and not os.path.exists(brandname+"_"+name+".pdf"):
                # down_res = requests.get(url=pdfurl)
                with open("url.txt","a+") as f:
                    print(brandname+"_"+name+".pdf"+pdfurl)
                    f.write(brandname+"_"+name+".pdf_"+pdfurl+"\n")
                # with open(brandname+"_"+name+".pdf","wb") as f:
                #     f.write(down_res.content)
            else:
                print("pdfurl:",pdfurl) 
            # input()


device = frida.get_usb_device()
# pid = device.spawn(["com.motoband"])
# device.resume(pid)
# time.sleep(10)
session = device.attach("com.motoband")
with open("motoband.js") as f:
    script = session.create_script(f.read())
script.on("message", my_message_handler) 
script.load()

# request for brandinfo 
headers = {
    'Source': 'source',
    'Date': 'Wed, 28 Jul 2021 10:42:37 GMT',
    'Authorization': 'hmac id="AKIDKpo6me25b14nzcNefQeoqR95syh2ayx97s0g", algorithm="hmac-sha1", headers="date source", signature="LueIYYQhihnHza8ZIzzH3X1J6xM="',
    'Content-Type': 'application/json;*/jg charset=utf-8',
    'Content-Length': '396',
    'Host': 'api.motuobang.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.14.9'
}
param_str = '{"jpushregistrationid":"18071adc03d4364a59f","ctype":"2","citycode":"0512","requestid":"10120210728184237309B6FABE44946F25C3","brandid":0,"sign":"Un9ld6EYErQmE2ab0CgGP4pbqGKz8taTYlT2d4vgJlR1e6N3vp2Ld/YHpZVHLAYQgdYxmHDPDmdPiapY/Irewg==","type":0,"cversion":"4.8.0.2021070601","userid":"53AEB07289854E91A74DA4718D86617F","token":"6A057F7AB0654DEBA3A9BAFE51A17D62","lonlat":"[120.670592,31.295319]"}'
data = requests.post('http://api.motuobang.com/release/car/brandinfo', data=param_str,headers=headers).json()["data"]
brandlist = json.loads(data)["brandlist"]


# 1.first
# for brand in brandlist:
#     brandname = brand["name"]
#     brandid = str(brand["brandid"])
#     # 1.创建文件夹
#     # 2.request for searchv2
#     script.exports.hooksearchv2(brandid)
#     # print(name_model_dict)
#     # 3.request for seriesinfo
#     # for (key,value) in name_model_dict.items():
#         # print(key+":"+str(value))
#         # script.exports.hookseriesinfo(str(value))
#     # 避免RuntimeError: dictionary changed size during iteration    
#     # for value in list(name_model_dict.values()):
#     #     script.exports.hookseriesinfo(str(value))
#     # input()    
# with open("moduleid.txt","a+") as f:
#     f.write(",".join(moduleid_list))


# 2.second
# with open("moduleid.txt","r") as f:
#     moduleid_list = f.read()
#     for module_id in moduleid_list.split(","):
#         print(module_id)
#         script.exports.hookseriesinfo(str(module_id))

# 3.third
def download_pics(url,n):
    r = requests.get(url)
    with open(r'./pdf/{}'.format(n),'wb') as f:
        f.write(r.content)
    thread_lock.release()

def main():
    for line in open("url.txt",encoding='UTF-8'):
        url = line.split("_")[2].strip()
        name = line.split("_")[:2]
        print(url)
        # 上锁 避免下载同一张
        thread_lock.acquire()
        t = threading.Thread(target=download_pics,args=(url,"".join(name).replace("/","")))
        t.start()
main()