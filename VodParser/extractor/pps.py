#!/usr/bin/env python
#_*_coding:utf-8_*_
import re
from common import get_content,r1,parser2dic
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

def get_pps_rate(i):
    if i == '0':
        rid = '标清'
    elif i =='1':
        rid = '高清'
    elif i =='2':
        rid = '超清'
    return rid

def get_pps_vid(html):
    if re.match(r'http://v.pps.tv/play_(.*).html',html):
        vid = r1(r'http://v.pps.tv/play_(.*).html',html)
    else:
        con = get_content(html)
        vid = r1(r'url_key: "(.*)",',con)
    return vid

def get_pps_urls_by_id(vid):
    urls = []
    for i in range(0,2):
        con = get_content('http://dp.ugc.pps.tv/get_play_url_cdn.php?sid={}&flash_type=1&type={}'.format(vid, i))
        if 'pfv' in con:
            template = {}
            con = r1(r'(.*)&all.*',con)
            template['rate'] = get_pps_rate(str(i))
            template['furls'] = [con]
            urls.append(template)
    return urls

def get_urls(html):
    try:
        vid = get_pps_vid(html) 
        urls = get_pps_urls_by_id(vid)
    except Exception,e:
        print e
        urls = []
    return parser2dic(urls)

#http://v.pps.tv/play_36C32J.html
if __name__ == "__main__":
    print get_urls('http://v.pps.tv/play_36C32J.html')
