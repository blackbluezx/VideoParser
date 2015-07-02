#!/usr/bin/env python
#_*_coding:utf-8_*_

import urllib2
import json
from common import r1_of,parser2dic,getredirect
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

# http://v.ku6.com/fetchwebm/_AVbqIR88LRyg15KcnQvIw...m3u8
# rate =1500 rate=799 rate=450 rate=299
def get_vid(url):
    patterns = [r'http://v.ku6.com/.*/show_\d+/(.*)html',
            r'.*show/(.*?)html']
    vid = r1_of(patterns, url)
    if vid == None:
        rurl = getredirect(url)
        patterns = [r'http://v.ku6.com/special/show_\d+/(.*)html',
            r'.*show/(.*?)html']
        vid = r1_of(patterns, url)
    return vid

def get_urls_by_vid(vid):
    urls = []
    url = "http://v.ku6.com/fetchVideo4Player/%shtml"%vid
    jsonContent = json.loads(urllib2.urlopen(url).read())['data']['f']
    rurls = []
    for realurl in jsonContent.split(','):
        rurls.append(realurl)
    rates = ['高清','标清','低清']
    erates = ['?rate=1500','?rate=799','?rate=450']
    for i in range(0,len(rates)):
        template = {}
        template['rate'] = rates[i]
        furls = []
        for u in rurls:
            furls.append(u+erates[i])
        template['furls'] = furls
        urls.append(template)
    return urls
        

def get_urls(url):
    try:
        vid = get_vid(url)
        urls = get_urls_by_vid(vid)
    except:
        urls = []
    return parser2dic(urls)

if __name__ == '__main__':   
    url = 'http://v.ku6.com/show/wD0sX0FCMGbo9-GmZ2SdRA...html?csrc=4_77_1'
    print get_vid(url)
    print get_urls(url)
