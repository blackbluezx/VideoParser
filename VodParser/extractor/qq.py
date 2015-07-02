#!/usr/bin/env python
#_*_coding:utf-8_*_

import re
import threading
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from common import get_content,r1,parser2dic
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

fmts = ['sd','sd','sd','hd','shd','fhd']
types = ['mp4','flv','segs','segs','segs','segs',]

def get_clarity(eng):
    if eng == 'sd':
        rid = '低清'
    elif eng =='hd':
        rid = '标清'
    elif eng == 'shd':
        rid = '高清'
    elif eng == 'fhd':
        rid = '超清'
    return rid

def get_video_sections_by_id(vid, fmt):
    try:
        xml = get_content('http://vv.video.qq.com/getinfo?vids=%s' % vid +'&defaultfmt=%s' % fmt)
        root = ET.fromstring(xml)
        num = root.find('vl/vi/cl/fc').text
        ui = root.find('vl/vi/ul/ui/url').text
        urls = []
        for i in range(1,int(num)+1):
            suffix = get_vkey_by_id(vid, i, fmt)
            url = ui+suffix
            urls.append(url)
    except Exception,e:
        print e
        urls = None
    return urls 

def get_vkey_by_id(vid,idx,fmt):
    xml = get_content('http://vv.video.qq.com/getclip?vid={}&idx={}&fmt={}'.format(vid,idx,fmt))
    root = ET.fromstring(xml)
    fn = root.find('vi/fn').text
    vkey = root.find('vi/key').text
    suffix = fn+'?vkey='+vkey
    return suffix 

class getSegUrls(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self,vtype,param):  
        threading.Thread.__init__(self)  
        self.template = {}  
        self.vtype = vtype
        self.vid = param[0]
        self.fmt = param[1]
        self.thread_stop = False  
   
    def run(self): #Overwrite run() method, put what you want the thread do here
        if self.vtype == 'mp4':
            furls = get_video_mp4_complete_by_id(self.vid) 
            if furls != None:
                self.template['rate'] = '标清'
                self.template['furls'] = [furls]
        elif self.vtype == 'flv':
            furls = get_video_flv_complete_by_id(self.vid) 
            if furls != None:
                self.template['rate'] = '标清'
                self.template['furls'] = [furls]
        else:
            furls = get_video_sections_by_id(self.vid,self.fmt)
            if furls!= None:
                self.template['rate'] = get_clarity(self.fmt)
                self.template['furls']  = furls
        
def get_video_mp4_complete_by_id(vid):
    try:
        info = get_content('http://vv.video.qq.com/getinfo?vids={}&otype=xml&defaultfmt=mp4'.format(vid))
        root = ET.fromstring(info)
        fn = root.find('vl/vi/fn').text
        fvkey = root.find('vl/vi/fvkey').text
        ui = root.find('vl/vi/ul/ui/url').text
        url = ui+fn+'?vkey='+fvkey
    except Exception,e:
        print e
        url = None
    return url

def get_video_flv_complete_by_id(vid):
    try:
        info = get_content('http://vv.video.qq.com/getinfo?vids={}&otype=xml&defaultfmt=flv'.format(vid))
        root = ET.fromstring(info)
        fn = root.find('vl/vi/fn').text
        fvkey = root.find('vl/vi/fvkey').text
        ui = root.find('vl/vi/ul/ui/url').text
        url = ui+fn+'?vkey='+fvkey
    except Exception,e:
        print e
        url = None
    return url 

def get_qq_vid(url):
    if re.match(r'http://v.qq.com/([^\?]+)\?vid', url):
        vid = r1(r'http://v.qq.com/[^\?]+\?vid=(\w+)', url)
    else:
        html = get_content(url)
        vid = r1(r'vid:"(.*)"', html)  
    return vid

def get_urls(html):
    allurls = []
    threads = []
    vid = get_qq_vid(html) 
    for i in range(0,len(types)):
        thread1 = getSegUrls(types[i],[vid,fmts[i]])
        threads.append(thread1) 
        thread1.start()
    for i in range(0,len(threads)):
        threads[i].join()
        if threads[i].template != {} :
            allurls.append(threads[i].template)
    return parser2dic(allurls)
 
#http://v.qq.com/cover/e/ea49fskavlwolbp.html
if __name__ == "__main__":
#    print get_urls('http://v.qq.com/cover/1/1vhtklm1izph8k3.html?vid=f0015dry88q')
    urls = get_urls('http://v.qq.com/cover/1/1vhtklm1izph8k3.html?vid=f0015dry88q')
    for i in urls[4]['furls']:
        print i
