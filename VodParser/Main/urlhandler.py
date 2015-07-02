#!/usr/bin/env python
#_*_coding:utf-8_*_

import sys
sys.path.append(r'..')
import extractor.cntv as CNTV
import extractor.com56 as COM56
import extractor.funshion as FUNS
import extractor.kankan as KANKAN
import extractor.ku6 as KU6
import extractor.letv as LETV
import extractor.m1905 as M1905
import extractor.pps as PPS
import extractor.qq as QQ
import extractor.sina as SINA
import extractor.sohu as SOHU
import extractor.tudou as TUDOU
import extractor.wasu as WASU
import extractor.youku as YOUKU
import extractor.iqiyi as IQIYI
import extractor.flvcd as FLVCD
import base64
reload(sys) 
sys.setdefaultencoding('utf8') 

def getUrlsSites(url):
    urls = []
    if 'wasu' in url:
        urls = WASU.get_urls(url)
    elif 'cntv' in url:
        urls = CNTV.get_urls(url)
    elif '56.com' in url:
        urls = COM56.get_urls(url)  
    elif 'ku6.com' in url:
        urls = KU6.get_urls(url)  
    elif 'letv.com' in url:
        urls = LETV.get_urls(url)
    elif '1905.com' in url:
        urls = M1905.get_urls(url)
    elif 'pps.tv' in url:
        urls = PPS.get_urls(url)
    elif 'qq.com' in url:
        urls = QQ.get_urls(url)
    elif 'sina.com' in url:
        urls = SINA.get_urls(url)
    elif 'sohu.com' in url:
        urls = SOHU.get_urls(url)
    elif 'kankan.com' in url:
        urls = KANKAN.get_urls(url)
    elif 'youku.com' in url:
        urls = YOUKU.get_urls(url)
    elif 'tudou.com' in url:
        urls = TUDOU.get_urls(url)
    elif 'iqiyi' in url:
        urls = IQIYI.get_urls(url)
    elif 'fun.tv' in url or 'funshion.com' in url:
        urls = FUNS.get_urls(url)
    return urls
    
def GetUrlsFromSites(url):
    urls = []
#    try:
#        url = base64.b64decode(burl)
#        print 'URL',url
#    except Exception,e:
#        print e
#        url = 'error'
    urls1 = getUrlsSites(url)
    urls2 = FLVCD.get_urls(url)
    for tem in urls1:
        template = {}
        template['rate'] = tem['rate']
        template['furls'] = tem['furls']
        template['source'] = 'site'
        urls.append(template)
    for tem in urls2:
        template = {}
        template['rate'] = tem['rate']
        template['furls'] = tem['furls']
        template['source'] = 'flvcd'
        urls.append(template)  
    return urls

if __name__ == '__main__':
    print GetUrlsFromSites('http://v.youku.com/v_show/id_XNzc5NzMwMDQ4.html?from=y1.3-movie-grid-1095-9921.86994-86993.4-1')
    