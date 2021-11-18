import execjs
import re
import requests
import json

from m3u8 import M3u8Download

with open("ckey_blog.js", "r",encoding="utf-8") as f:
    js_code = f.read()

# target_url = "http://v.qq.com/txp/iframe/player.html?origin=https%3A%2F%2Fmp.weixin.qq.com&chid=17&vid=s3306hychob&autoplay=false&full=true&show1080p=false&isDebugIframe=false"
target_url = "https://v.qq.com/x/cover/bzfkv5se8qaqel2/j002024w2wg.html"
vinfoparam = "spsrt=1&charge=0&defaultfmt=auto&otype=ojson&guid={}&flowid={}&platform={}&sdtfrom={}&defnpayver=0&appVer={}&host=v.qq.com&sphttps=0&tm=1637237951&spwm=4&vid={}&defn=&fhdswitch=0&show1080p=0&isHLS=1&dtype=3&sphls=1&spgzip=&dlver=&hdcp=0&spau=1&spaudio=15&defsrc=1&encryptVer=9.1&cKey={}"
data = {}
data["buid"] = "vinfoad"
guid = execjs.compile(js_code).call('createGUID')
if "mp.weixin.qq.com" in target_url:
    vid = re.compile(r"&vid=(.*?)&").findall(target_url)[0] # ?非贪婪
    plateform = "70201"
    flowid = execjs.compile(js_code).call('createGUID') + "_" + plateform
    sdtfrom = "v1104"
    appVer = "3.4.40"
    ckey = execjs.compile(js_code).call('getCKey',plateform,appVer,vid)
else:
    vid = target_url.split("/")[-1].split(".")[0]
    plateform = "10201"
    flowid = execjs.compile(js_code).call('createGUID') + "_" + plateform
    sdtfrom = "v1010"
    appVer = "3.5.57"
    ckey = execjs.compile(js_code).call('getCKey', plateform, appVer, vid)

data["vinfoparam"] = vinfoparam.format(guid,flowid,plateform,sdtfrom,appVer,vid,ckey)
result = requests.post('http://vd.l.qq.com/proxyhttp', data=json.dumps(data)).json()
# print(result)
if result.get("errCode") == 0:
    url_data = json.loads(result.get("vinfo"))["vl"]["vi"][0]["ul"]["ui"][0]
    url = url_data["url"]+url_data["hls"]["pt"]
    print("m3u8地址",url)
    M3u8Download(url,
                 "test",
                 max_workers=64,
                 num_retries=10,
                 )
