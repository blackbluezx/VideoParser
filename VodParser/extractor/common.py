#!/usr/bin/env python
#_*_coding:utf-8_*_

import urllib2
import random
import re
from xml.sax.saxutils import escape
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

proxy_list = ['116.236.216.116:8080',
              '183.131.144.204:443',
              '202.108.50.75:80',
              '122.96.59.106:82',
              '203.192.10.66:80']

def getContent(url):
    content = None
    for i in range(0,3):
        content = getHtml(url)
        if content!=None:
            print i
            break;
        else:
            print 'ee',i
    return content

def getHtml(url):
    proxy_support = urllib2.ProxyHandler({'http':random.choice(proxy_list)})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)  
    urllib2.install_opener(opener)  
    content = urllib2.urlopen(url,timeout =5 ).read()
    return content

def get_content(url):
    r=urllib2.Request(url)
    r.add_header("Accept-Language", "zh-cn")
    r.add_header("User-Agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53")
    try:
        content=urllib2.urlopen(r, timeout=5).read()
        return content
    except:
        return None
    
#def get_content(url):
#    response = urllib2.urlopen(url)
#    data = response.read()
#    return data  

def match1(text, *patterns):
    """Scans through a string for substrings matched some patterns (first-subgroups only).

    Args:
        text: A string to be scanned.
        patterns: Arbitrary number of regex patterns.

    Returns:
        When only one pattern is given, returns a string (None if no match found).
        When more than one pattern are given, returns a list of strings ([] if no match found).
    """

    if len(patterns) == 1:
        pattern = patterns[0]
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None
    else:
        ret = []
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                ret.append(match.group(1))
        return ret
# DEPRECATED in favor of match1()
def r1(pattern, text):
    if text!= None:
        m = re.search(pattern, text)
        if m:
            return m.group(1)
    else:
        return None

def r1_of(patterns, text):
    for p in patterns:
        x = r1(p, text)
        if x:
            return x

def getredirect(url):
    try:
        headers = {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"}
        r = requests.get(url, headers=headers)
        return r.url
    except:
        return url
  
def r2(pattern, text):
    m = re.compile(pattern)
    if text!=None:
        return m.findall(text)
    else:
        return []
    
def parser2dic(urls):
    nurls = []
    if urls!= None:
        for tem in urls:
            template = {}
            template['rate'] = tem['rate']
            furls = []
            for url in tem['furls']:
                furls.append(escape(url.decode('utf-8','ignore')))
            template['furls'] = furls
            nurls.append(template)
    else :
        nurls = None
    return nurls

if __name__ == '__main__':
    print getContent('http://www.woshisb.com/')