#!/usr/bin/env python
#_*_coding:utf-8_*_

import urllib2
import json
from common import get_content,parser2dic
import extractor.youku as YOUKU
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

def get_video_urls(tudou_url):
    html = urllib2.urlopen(tudou_url).read()
    index = html.find('vcode') + len('vcode')
    vid = html[index+3:index+16]    
    jsonUrl = "http://v.youku.com/player/getPlayList/VideoIDS/" + vid
    jsonContent = json.loads(urllib2.urlopen(jsonUrl).read())
    streamType = jsonContent['data'][0]['streamsizes']
    print streamType
    videoTypes = ['mp4', 'hd3', 'hd2', 'flv'] 
    for videoType in videoTypes:
        try:
            streamType_id = streamType[videoType]
            m3u8_url = "http://v.youku.com/player/getM3U8/vid/%s/type/%s/video.m3u8"%(id, streamType_id)
            print videoType
            print m3u8_url
        except:
            print videoType + 'do not exist'

def get_vid_by_url(url):
    html = get_content(url)
    index = html.find('vcode') + len('vcode')
    vid = html[index+3:index+16]
    return vid

def get_urls(url):
    urls = []
    try:
        vid = get_vid_by_url(url)
        urls = YOUKU.get_urls_by_vid(vid)
    except Exception,e:
        print e
        urls = []
    return parser2dic(urls)   
  
if __name__ == '__main__': 
    tudou_url = "http://www.tudou.com/albumplay/9SPemnFjdUE.html"
    print get_urls(tudou_url)   
