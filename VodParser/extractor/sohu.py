#!/usr/bin/env python
#_*_coding:utf-8_*_

import urllib2
import json
import re
from common import get_content,r1,parser2dic
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

def getPram(streamType_id):
    url = "http://hot.vrs.sohu.com/vrs_flash.action?vid=" + str(streamType_id)
    jsonContent = json.loads(urllib2.urlopen(url).read())
    allot = jsonContent['allot']
    prot = jsonContent['prot']
    clipsURL = jsonContent['data']["clipsURL"]
    su = jsonContent['data']["su"]
    return allot, prot, clipsURL, su

def getKey(allot_url):
    content = urllib2.urlopen(allot_url).read()
    listTmp = content.split('|')
    prefix = listTmp[0]
    key = listTmp[3]
    return prefix, key
  
def get_vid(url):
    html = get_content(url)
    try:
        pattern = re.compile("share.vrs.sohu.com/(.*?)/")
        match = pattern.search(html)
        vid = match.group(1)
    except :
        vid = r1(r'vid="(.*)";',html)
    return vid

def get_urls_by_vid(vid): 
    urls = []
    streamTypes_ch = ['低清','标清','高清','超清']
    streamTypes = ["norVid", "highVid", "superVid", "oriVid"]
    streamType_url = "http://hot.vrs.sohu.com/vrs_flash.action?vid=" + vid
    jsonContent = json.loads(urllib2.urlopen(streamType_url).read())['data']
    for i in range(0,len(streamTypes)):
        try:
            template = {}
            template['rate'] = streamTypes_ch[i]
            streamType_id = jsonContent[streamTypes[i]]
            allot, prot, clipsURL, su = getPram(streamType_id)
            if(len(clipsURL)!=len(su)):
                continue
            else:
                furls = []
                for i in range(len(clipsURL)):
                    allot_url = "http://%s/?prot=%s&file=%s&new=%s"%(allot, prot, clipsURL[i], su[i])
                    prefix, key = getKey(allot_url)
                    realUrl = "%s%s?key=%s"%(prefix[0:-1], su[i], key)
                    furls.append(realUrl)
                template['furls'] = furls
                urls.append(template)  
        except Exception,e:
            print e
            pass
    return urls
 
def get_urls(url):
    urls = []
    vid = get_vid(url)
    if vid!= None:
        urls = get_urls_by_vid(vid)
    return parser2dic(urls)
    
if __name__ == '__main__':
    url = 'http://tv.sohu.com/20131020/n388515766.shtml'
    urls = get_urls(url)
    print len(urls)
    for i in urls[0]['furls']:
        print i
                
    
