#!/usr/bin/env python
#_*_coding:utf-8_*_

from common import r1,r2,get_content,parser2dic
import urllib2
from random import randint
from time import time
import md5
import json
from xml.etree import ElementTree
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

#http://v.iask.com/v_play_ipad.php?vid=134765323&tags=wap_dp
rate = ['低清','标清','高清','超清']
def get_hdvid(html):
    hdvid = r1(r'hd_vid:\'(.*?)\',',html)
    return hdvid

def get_ipadvid(html):
    ipadvid = r1(r'ipad_vid:\'(.*?)\',',html)
    return ipadvid

def get_segvids(html):
    try:
        vids = r2(r"vid:'(\d+)\|(\d+)\|(\d+)'",html)
        vid = vids[0]
    except:
        vid = None
    return vid

def get_newsvid(url):
    newsvid = r1(r'.*#(.*)',url)
    return newsvid

def get_news_url_by_vid(vid):
    try:
        url = 'http://video.sina.com.cn/interface/video_ids/video_ids.php?v={}'.format(vid)
        html = json.loads(get_content(url))
        newsvid = html['ipad_vid']
        url = 'http://v.iask.com/v_play_ipad.php?vid={}&tags=newsList_web'.format(newsvid)
    except Exception,e:
        print e
        url = None
    return url
   
def get_urls_by_vid(vid):
    try:
        furls = []
        ran = "0.{0}{1}".format(randint(10000, 10000000), randint(10000, 10000000))
        t = str(int('{0:b}'.format(int(time()))[:-6], 2))
        k = md5.new((vid+'Z6prk18aWxP278cVAH'+t+ran).encode('utf-8')).hexdigest()[:16]+t
        realUrl = "http://v.iask.com/v_play.php?vid=%s&ran=%s&p=i&k=%s"%(vid, ran, k)
        xmlStr = urllib2.urlopen(realUrl).read()
        root = ElementTree.fromstring(xmlStr) 
        node_urls = root.findall('durl')
        for node_url in node_urls:
#        print int(node_url.find('length').text)/1000
            furls.append(node_url.find('url').text)
    except Exception,e:
        print e
        furls = None
    return furls 
   
def get_urls(url): 
    urls = []
    newsvid = get_newsvid(url)
    if newsvid != None:
        newsurl = get_news_url_by_vid(newsvid)
        if newsurl!=None:
            urls.append({'rate':'标清','furls':[newsurl]})
    html = get_content(url)
    ipadvid = get_ipadvid(html)
    if ipadvid !=None:
        ipadurl = get_urls_by_vid(ipadvid)
        if ipadurl != None:
            urls.append({'rate':'标清','furls':ipadurl})
    segvids = get_segvids(html)
    if segvids!= None:
        for i in range(0,len(segvids)):
            url = get_urls_by_vid(segvids[i])
            if url != None:
                urls.append({'rate':rate[i],'furls':url})
        
    return parser2dic(urls)
    
if __name__ == '__main__':
    url = 'http://video.sina.com.cn/m/201406190445582_64048689.html'
    print get_urls(url)
        
    
