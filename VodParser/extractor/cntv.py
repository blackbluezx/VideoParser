#!/usr/bin/env python
#_*_coding:utf-8_*_

import re
import json
from common import get_content,r1,parser2dic
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

def get_clarity(eng):
    if eng == 'lowChapters':
        rid = '低清'
    elif eng =='chapters':
        rid = '标清'
    elif eng == 'chapters2':
        rid = '高清'
    return rid
def get_cntv_pid(html):
    if re.match(r'http://tv.cntv.cn/.*/(\w+)', html):
        pid = r1(r'http://tv.cntv.cn/.*/(\w+)', html)
    elif re.match(r'http://xiyou.cntv.cn/v-[\w-]+\.html', html):
        pid = r1(r'http://xiyou.cntv.cn/v-([\w-]+)\.html', html)
    else:
        raise NotImplementedError(html)
    return pid

def get_cntv_urls_by_id(pid):
    urls = []
    info = json.loads(get_content('http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=' + pid))
    hls_url = info['hls_url']
    if hls_url != '':
        template = {'rate':'标清','furls':[hls_url]}
        urls.append(template)
    video = info['video']
    for x in video.keys():
        if x in ["chapters2","lowChapters","chapters"]:
            templates = {}
            segs = video[x]
            templates['rate'] = get_clarity(x)
            furls = []
            for y in range(0,len(segs)):
                furls.append(segs[y]['url'])
            templates['furls'] = furls
            urls.append(templates)
    return urls

def get_urls(html): 
    try:   
        pid = get_cntv_pid(html)
        urls = get_cntv_urls_by_id(pid)
    except:
        urls =None
    return parser2dic(urls)
    
#http://tv.cntv.cn/video/C10406/84372ab2f9a24e5b90aa0a69309f7a31
if __name__ == '__main__':
    url = 'http://tv.cntv.cn/live/cctv2?date=2014-10-13&index=0'
    print get_urls(url)
