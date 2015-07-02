#!/usr/bin/env python
#_*_coding:utf-8_*_
import re
import requests
import json
from common import get_content,r1,r2,parser2dic
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

def getredirect(url):
    try:
        headers = {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"}
        r = requests.get(url, headers=headers)
        return r.url
    except:
        return url


def get_funshion_vid(rurl):
    if re.match(r'http://www.fun.tv/vplay/.*m-(\d+)',rurl):
            vid = r1(r'http://www.fun.tv/vplay/.*m-(\d+)',rurl)
    else:
        html = get_content(url)
        vid = r1(r'\"mediaid\":(\d+)',html)
    return vid

def get_funshion_playnum(rurl):
    playNum = r1('http://www.fun.tv/vplay/.*m-\d+.e-(\d+)',rurl)
    print 'playNum',playNum
    if playNum == None:
        html = get_content(rurl)
        playNum = r1("minfo.playNumber = \'(\d+)\';",html)
    if playNum == None:
        playNum = 1
        print 'playNum2',playNum
    return playNum
            
def get_clarity(eng):
    if eng == 'tv':
        rid = '低清'
    elif eng =='dvd':
        rid = '标清'
    elif eng == 'highdvd':
        rid = '高清'
    return rid

def get_fun_allurls(vid,playnum):
    urls = []
    pos = 0
    info = get_content('http://jsonfe.funshion.com/media/?cli=ipad&ver=2.0.0.1&ta=0&mid={}'.format(vid))
    number = r2(r'"number":"(\d*)",',info)
    print len(number),number
#    mpurls = r2(r'"mpurls":(\{.*?\{.*?\}.*?\{.*?\}.*?\{.*?\}\})',info)
    tvurl = r2('\"tv\":{\"url\":\"(.*?)\"',info)
    dvdurl = r2('\"dvd\":{\"url\":\"(.*?)\"',info)
    highdvd = r2('\"highdvd\":{\"url\":\"(.*?)\"',info)
    print len(tvurl),tvurl
    print len(dvdurl),dvdurl
    print len(highdvd),highdvd
    
#    print len(number),number,len(mpurls),mpurls
    if len(number) == 0:
        urls = []
    elif len(number) == len(tvurl):
        for i in range(0,len(number)):
            if number[i] == playnum:
                pos = i
                break
        if pos < len(tvurl):
            template = {}
            template['rate'] = get_clarity('tv')
            furls = [tvurl[pos].replace('\\','')]
            template['furls'] = furls
            urls.append(template)
        if pos < len(dvdurl):
            template = {}
            template['rate'] = get_clarity('dvd')
            furls = [dvdurl[pos].replace('\\','')]
            template['furls'] = furls
            urls.append(template)
        if pos < len(highdvd):
            template = {}
            template['rate'] = get_clarity('highdvd')
            furls = [highdvd[pos].replace('\\','')]
            template['furls'] = furls
            urls.append(template)
    else:
        if 0 < len(tvurl):
            template = {}
            template['rate'] = get_clarity('tv')
            furls = [tvurl[0].replace('\\','')]
            template['furls'] = furls
            urls.append(template)
        if 0 < len(dvdurl):
            template = {}
            template['rate'] = get_clarity('dvd')
            furls = [dvdurl[0].replace('\\','')]
            template['furls'] = furls
            urls.append(template)
        if 0 < len(highdvd):
            template = {}
            template['rate'] = get_clarity('highdvd')
            furls = [highdvd[0].replace('\\','')]
            template['furls'] = furls
            urls.append(template)
    return urls

def get_urls(url):
    urls = []
    try:
        rurl = getredirect(url)
        print rurl
        vid = get_funshion_vid(rurl)
        playnum = get_funshion_playnum(rurl)
        print vid,playnum
        urls = get_fun_allurls(vid,playnum)
    except Exception,e:
        print e
        urls = []
    return parser2dic(urls)
#http://www.fun.tv/vplay/m-109104/   movie
#http://www.fun.tv/vplay/m-111738.e-25/    tv
#http://www.fun.tv/vplay/m-112230.e-20140902/    variety
#http://www.fun.tv/vplay/v-2330862.m-102486/   cartoon 
#http://www.funshion.com/subject/play/111154/6  
if __name__ == "__main__":
    url = 'http://www.fun.tv/vplay/g-117867/'
    print get_urls(url)
