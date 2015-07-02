#!/usr/bin/env python
#_*_coding:utf-8_*_

import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from common import get_content,r1,parser2dic
import base64
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

def get_m1905_vid(html):
    if re.match(r'http://www.1905.com/vod/play/(.*).shtml.*',html):
        vid = r1(r'http://www.1905.com/vod/play/(.*).shtml.*',html)
    else:
        con = get_content(html)
        vid = r1(r'vid : "(.*)",',con)
    return vid

def get_clarity(eng):
    if eng == 'sdurl':
        rid = '低清'
    elif eng =='url':
        rid = '标清'
    elif eng == 'hdurl':
        rid = '高清'
    elif eng == 'bkurl':
        rid = '超清'
    return rid

def get_m1905_m3u8(vid):
    try:
        url = 'http://www.1905.com/api/video/getmediainfo.php?id={}&type=0&source_key=m3u8ipad'.format(vid)
        con = get_content(url)
        m3url = r1(r'"iosurl":"(.*?)",',con)
        m3u8 = base64.decodestring(m3url)
    except Exception,e:
        print e
        m3u8 = None
    return m3u8
    
def get_m1905_urls(vid):
    urls = []
    m3u8url = get_m1905_m3u8(vid)
    if m3u8url != None:
        urls.append({'rate':'标清','furls':[m3u8url]})
    fir = r1(r'(\d).*',vid)
    sec = r1(r'\d(\d).*',vid)
    info = get_content('http://static.m1905.cn/profile/vod/{}/{}/{}_1.xml'.format(fir,sec,vid))
    root = ET.fromstring(info)
    links = root.find('playlist/item').attrib
    for i in links:
        if i in ['url','sdurl','bkurl','hdurl']:
            template = {}
            template['rate'] = get_clarity(i)
            template['furls'] = [links[i]] 
            urls.append(template)     
    return urls

def get_urls(html):
    try:
        vid = get_m1905_vid(html)
        con = get_m1905_urls(vid)
    except Exception,e:
        print e
        con = None
    return parser2dic(con)
#http://www.1905.com/vod/play/597853.shtml   
if __name__ == "__main__":
    print get_urls('http://www.1905.com/vod/play/597853.shtml') 
