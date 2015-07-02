#!/usr/bin/env python
#_*_coding:utf-8_*_

from common import get_content,r1,r2,parser2dic
import hashlib
from xml.sax.saxutils import escape
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

rate = ['低清','标清','高清','超清','超清']
def get_kankan_param(gcid,param):
    info = get_content('http://p2s.cl.kankan.com/getCdnresource_flv?gcid={}'.format(gcid))
    ip = r1(r'ip:"(.*?)"',info)
    path = r1(r'path:"(.*?)"',info)
    url = 'http://' + ip +'/'+ path
    param1 = r1(r'param1:(.*),',info)
    param2 = r1(r'param2:(.*)}',info)
    if param == 'url':
        return url
    elif param == 'param1':
        return param1
    elif param == 'param2':
        return param2
    else:
        return url
    
def get_kankan_mparam(gcid,param):
    info = get_content('http://mp4.cl.kankan.com/getCdnresource_flv?gcid={}'.format(gcid))
    ip = r1(r'ip:"(.*?)"',info)
    path = r1(r'path:"(.*?)"',info)
    url = 'http://' + ip +'/'+ path
    param1 = r1(r'param1:(.*),',info)
    param2 = r1(r'param2:(.*)}',info)
    if param == 'url':
        return url
    elif param == 'param1':
        return param1
    elif param == 'param2':
        return param2
    else:
        return url

def get_gcids(html):
    con = get_content(html)
    gcid = r2(r'http://pubnet.sandai.net:8080/\d+/(.*?)/.*?.flv',con)
    return gcid

def get_gcid(html):
    con = get_content(html)
    gcid = r1(r'http://pubnet.sandai.net:8080/\d+/(.*?)/.*?.mp4',con)
    return gcid

def get_url(html):
    rurls = []
    try:
        gcids = get_gcids(html)
        if (len(gcids)!= 0):
            for gcid in gcids:
                param1 = get_kankan_param(gcid,'param1')
                param2 = get_kankan_param(gcid,'param2')
                url = get_kankan_param(gcid,'url')
                param1_md5 = hashlib.new('md5', param1).hexdigest()  
                rurl = url+'?key='+param1_md5+'&key1='+param2
                rurls.append(rurl)
    except Exception,e:
        print e
    return rurls

def get_murl(html):
    rurl = None
    try:
        gcid = get_gcid(html.replace('vod','m' ))
        param1 = get_kankan_mparam(gcid,'param1')
        param2 = get_kankan_mparam(gcid,'param2')
        url = get_kankan_mparam(gcid,'url')
        param1_md5 = hashlib.new('md5', param1).hexdigest()  
        rurl = url+'?key='+param1_md5+'&key1='+param2
    except Exception,e:
        print e
    return rurl

def get_urls(html):
    urls = []
    try:
        furl = get_murl(html)
        if furl!=None:
            urls.append({'rate':'低清','furls':[furl]})
        furls = get_url(html)
        if len(furls)!=0:
            for i in range(0,len(furls)):
                urls.append({'rate':rate[i],'furls':[furls[i]]})
        for i in urls:
            print i
    except Exception,e:
        print e
        urls = None
    return parser2dic(urls)
#http://vod.kankan.com/v/12/12801.shtml
if __name__ == "__main__":
    print get_urls('http://vod.kankan.com/v/68/68873.shtml?id=731057')
