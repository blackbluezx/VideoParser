#!/usr/bin/env python
#_*_coding:utf-8_*_

import re
import json
import random
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from common import get_content,match1,parser2dic
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

def get_rateid(nid):
    if nid == '350':
        rid = ['low','低清']
    elif nid =='1000':
        rid = ['high','标清']
    elif nid == '1300':
        rid = ['super','高清']
    elif nid == '720p':
        rid = ['720p','高清']
    elif nid == '1080p':
        rid = ['1080p','超清']
    return rid
    
def get_timestamp():
    tn = random.random()
    url = 'http://api.letv.com/time?tn={}'.format(tn)
    result = get_content(url)
    return json.loads(result)['stime']

def get_keyRor(value,key):
    i=0;
    while(i<key):
        value=(value>>1)+((value&1)<<31);
        i=i+1;
    return value;

def get_key(stime):
    key = 773625421;
    value = get_keyRor(stime, key%13);
    value ^= key;
    value = get_keyRor(value, key%17);
    return value;

def get_letv_vid(url):
    if re.match(r'http://www.letv.com/ptv/vplay/(\d+).html', url):
        vid = match1(url,r'http://www.letv.com/ptv/vplay/(\d+).html')
    else:
        html = get_content(url)
        vid = match1(html, r'vid="(\d+)"')
    return vid

def get_urls_by_vid(vid):
    urls = []
    tn = get_timestamp()
    key = get_key(tn)
    url = 'http://api.letv.com/mms/out/video/playJson?id={}&platid=1&splatid=101&format=1&tkey={}&domain=www.letv.com'.format(vid, key)
    info = get_content(url)
    playurl = json.loads(info)['playurl']
    domain = playurl['domain'][0]
    dispatch = playurl['dispatch']
    for k in dispatch.keys():
        template = {}
        url = dispatch[k][0]
        rate = get_rateid(k)
        template['rate'] = rate[1] 
        url = domain + url  + '&retry=1&tag=flash&sign=webdisk_19722818&termid=1&pay=0&ostype=windows&hwtype=un'
        url = url.replace('platid=1', 'platid=14')
        url = url.replace('splatid=101','splatid=1401')
        print rate[1]
        print url
        template['furls'] = [url]
        urls.append(template)
        if 'tss=ios' in url:
            ano = url.replace('tss=ios','tss=no')
        else:
            ano = url.replace('tss=no','tss=ios')
        print ano    
        urls.append({'rate':rate[1],'furls':[ano]})
    return urls

def get_urls(html):
    try:
        vid = get_letv_vid(html)
        print vid
        con = get_urls_by_vid(vid)
    except Exception,e:
        print e
        con = []
    return parser2dic(con)
#http://www.letv.com/ptv/vplay/2100756.html
#http://www.letv.com/ptv/vplay/2184096.html
if __name__ == "__main__":
    urls = get_urls('http://www.letv.com/ptv/vplay/21822487.html')
    print urls
