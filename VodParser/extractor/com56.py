#!/usr/bin/env python
#_*_coding:utf-8_*_

import urllib2
import json
from common import parser2dic
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

def get_clarity(eng):
    if eng == 'clear':
        rid = '低清'
    elif eng =='normal':
        rid = '标清'
    elif eng == 'super':
        rid = '高清'
    return rid

def get_vid(url):
    try:
        vid = url.split('_')[1].split('.')[0]
    except Exception,e:
        print e
        vid = None
    return vid

def get_urls(url):
    furls = []
    vid = get_vid(url)
    if vid!=None:
        try:
            jsonUrl = "http://vxml.56.com/json/%s/?src=site" % vid
            jsonContent = json.loads(urllib2.urlopen(jsonUrl).read(),'utf-8')
            rfiles = jsonContent['info']['rfiles']
            for rfile in rfiles:
                template ={}
                template['rate'] = get_clarity(rfile['type'])
                urls = []
                url = rfile['url']
                urls.append(url)
                template['furls'] = urls
                furls.append(template)
        except Exception,e:
            print e
            furls = []
    return parser2dic(furls)
        
if __name__ == '__main__':
    url = 'http://www.56.com/u56/v_ODQxNjcxMTc.htmll'
    print get_urls(url)
