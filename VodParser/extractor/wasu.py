#!/usr/bin/env python
#_*_coding:utf-8_*_

import re
from common import get_content,r1,parser2dic
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 
    
def get_wasu_id(url):
    if re.match(r'http://www.wasu.cn/Play/show/id/(.*)', url):
        vid = r1(r'http://www.wasu.cn/Play/show/id/(.*)', url)
    return vid

def get_suffix_by_html(html):
    con = get_content(html)
    playUrl = r1(r'_playUrl = \'(.*?)\',',con)
    playKey = r1(r'_playKey = \'(.*?)\',',con)
    suffix = '/url/'+playUrl+'/key/'+playKey
    return suffix

def get_urls(html):
    try:
        vid = get_wasu_id(html)
        print vid
        suffix = get_suffix_by_html(html)
        url = 'http://www.wasu.cn/Api/getVideoUrl/id/'+vid+suffix
        info = get_content(url)
        root = ET.fromstring(info)
        url = root.find('video').text
        print url
    except:
        url = 'Error'
    return parser2dic([{'rate':'标清','furls':[url]}])

if __name__ == "__main__":
    url = get_urls('http://www.wasu.cn/Play/show/id/2134923')
    print url
