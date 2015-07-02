#!/usr/bin/env python
#_*_coding:utf-8_*_

from uuid import uuid4
from common import r1,get_content,parser2dic
from random import random,randint
import json
from math import floor
import hashlib
import threading
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 
 
class getUrls(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, num, param):  
        threading.Thread.__init__(self)  
        self.thread_num = num
        self.template = {}  
        self.video_link = param[0]
        self.gen_uid = param[1]
        self.info = param[2]
        self.bid = param[3]
        self.thread_stop = False  
   
    def run(self): #Overwrite run() method, put what you want the thread do here  
        self.template['rate'] = get_rate(self.bid)
        self.template['furls']  = get_real_urls(self.video_link,self.gen_uid,self.info)


stream_types = [
        {'bid': '5', 'video_profile': '超清'},
        {'bid': '4', 'video_profile': '高清'},
        {'bid': '3', 'video_profile': '标清'},
        {'bid': '2', 'video_profile': '标清'},
        {'bid': '1', 'video_profile': '低清'},
        {'bid': '96', 'video_profile': '流畅'},
        {'bid': '10', 'video_profile': '超清'},]

def get_rate(bid):
    rate = None
    for stream_type in stream_types:
        if bid == stream_type['bid']:
            rate = stream_type['video_profile']
            break
    if rate == None:
        rate = '标清'
    return rate

def getVRSXORCode(arg1,arg2):
    loc3=arg2 %3
    if loc3 == 1:
        return arg1^121
    if loc3 == 2:
        return arg1^72
    return arg1^103


def getVrsEncodeCode(vlink):
    loc6=0
    loc2=''
    loc3=vlink.split("-")
    loc4=len(loc3)
    # loc5=loc4-1
    for i in range(loc4-1,-1,-1):
        loc6=getVRSXORCode(int(loc3[loc4-i-1],16),i)
        loc2+=chr(loc6)
    return loc2[::-1]

def getVMS(tvid,vid,uid):
    tm=randint(1000,2000)
    vmsreq='http://cache.video.qiyi.com/vms?key=fvip&src=p'+"&tvId="+tvid+"&vid="+vid+"&vinfo=1&tm="+str(tm)+"&enc="+hashlib.new('md5',bytes('ts56gh'+str(tm)+tvid)).hexdigest()+"&qyid="+uid+"&tn="+str(random())
    return json.loads(get_content(vmsreq))

def getDispathKey(rid):
    tp=")(*&^flash@#$%a"  #magic from swf
    time=json.loads(get_content("http://data.video.qiyi.com/t?tn="+str(random())))["t"]
    t=str(int(floor(int(time)/(10*60.0))))
    return hashlib.new("md5",bytes(t+tp+rid)).hexdigest()

def get_real_urls(video_links,gen_uid,info):
    urls = []
    for i in video_links:
        vlink=i["l"]
        # print(vlink)
        if not vlink.startswith("/"):
            #vlink is encode
            vlink=getVrsEncodeCode(vlink)
        assert vlink.endswith(".f4v")
        key=getDispathKey(vlink.split("/")[-1].split(".")[0])
        baseurl=info["data"]["vp"]["du"].split("/")
        baseurl.insert(-1,key)
        url="/".join(baseurl)+vlink+'?su='+gen_uid+'&client=&z=&bt=&ct=&tn='+str(randint(10000,20000))
        urls.append(json.loads(get_content(url))["l"])
    return urls
    
def get_iqiyi_urls(url):
    allurls = []
    threads = []
    gen_uid = uuid4().hex
    html = get_content(url)
    tvid = r1(r'data-player-tvid="([^"]+)"', html)
    videoid = r1(r'data-player-videoid="([^"]+)"', html)
    assert tvid
    assert videoid
    info = getVMS(tvid,videoid,gen_uid)      
    bids = []
    videos = []
    try:
        for i in info["data"]["vp"]["tkl"][0]["vs"]:
            bid=int(i["bid"])
            bids.append(bid)
            video_links=i["fs"]
            videos.append(video_links)
        for i in range(0,len(videos)):
            thread1 = getUrls(i,[videos[i], gen_uid, info,str(bids[i])])
            threads.append(thread1)
            thread1.start()
    except Exception,e:
        print e
    for i in range(0,len(threads)):
        threads[i].join()
        if threads[i].template != {} :
            allurls.append(threads[i].template)
    return allurls
 
def get_urls(url):
    urls = []
    try:
        urls = get_iqiyi_urls(url)
    except Exception,e:
        print e
        urls = []
    return parser2dic(urls)
 
       
if __name__ == "__main__":
    url = 'http://www.iqiyi.com/v_19rrmuibj8.html#vfrm=2-4-0-1'
    print get_urls(url)
