#!/usr/bin/env python
#_*_coding:utf-8_*_

import base64
import json
from random import randint
import time
import urllib 
from common import get_content,match1,parser2dic
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

def get_video(vid,stream_type = None):
    url = "http://v.youku.com/player/getPlayList/VideoIDS/{}/Pf/4/ctype/12/ev/1".format(vid)
    vvid = vid
    info = json.loads(get_content(url))
    #key = '%s%x' % (info['data'][0]['key2'], int(info['data'][0]['key1'], 16) ^ 0xA55AA5A5)
    data = info['data'][0]
    segs = data['segs']
    types = segs.keys()
    if not stream_type:
        for x in ['hd3', 'hd2', 'mp4', 'flv']:
            if x in types:
                stream_type = x
                break
        else:
            raise NotImplementedError()
    assert stream_type in ('hd3', 'hd2', 'mp4', 'flv')
    print 'stream_type',stream_type
    file_type = {'hd3':'flv', 'hd2':'flv', 'mp4':'mp4', 'flv':'flv'}[stream_type]

    seed = info['data'][0]['seed']
    source = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890")
    mixed = ''
    while source:
        seed = (seed * 211 + 30031) & 0xFFFF
        index = seed * len(source) >> 16
        c = source.pop(index)
        mixed += c

    ids = info['data'][0]['streamfileids'][stream_type].split('*')[:-1]
    vid = ''.join(mixed[int(i)] for i in ids)

    sid = '%s%s%s' % (int(time.time()*1000), randint(1000, 1999), randint(1000, 9999))
    
    ep = data['ep']
    ip = data['ip']
    query = get_segurls_param(ep,ip)
    print query
    urls = []
    for s in segs[stream_type]:
        no = '%02x' % int(s['no'])
        url = 'http://k.youku.com/player/getFlvPath/sid/%s_%s/st/%s/fileid/%s%s%s?K=%s&ts=%s' % (sid, no, file_type, vid[:8], no.upper(), vid[10:], s['k'], s['seconds'])
        print url+'&'+query
        urls.append((url, int(s['size'])))
    return urls

stream_types = [
        {'id': 'hd3', 'container': 'flv', 'video_profile': '超清'},
        {'id': 'hd2', 'container': 'flv', 'video_profile': '高清'},
        {'id': 'mp4', 'container': 'mp4', 'video_profile': '标清'},
        {'id': 'flvhd', 'container': 'flv', 'video_profile': '标清'},
        {'id': 'flv', 'container': 'flv', 'video_profile': '低清'},
        {'id': '3gphd', 'container': '3gp', 'video_profile': '低清'},]

def get_rate(tid):
    rate = None
    for stream_type in stream_types:
        if tid == stream_type['id']:
            rate = stream_type['video_profile']
            break
    if rate == None:
        rate = '标清'
    return rate
        

def getVideoId(url):
    vid =  match1(url, r'youku\.com/v_show/id_([\w=]+)') or \
          match1(url, r'player\.youku\.com/player\.php/sid/([\w=]+)/v\.swf') or \
          match1(url, r'loader\.swf\?VideoIDS=([\w=]+)')
    return vid

def generate_ep(vid, ep):
    f_code_1 = 'becaf9be'
    f_code_2 = 'bf7e5f01'

    def trans_e(a, c):
        f = h = 0
        b = list(range(256))
        result = ''
        while h < 256:
            f = (f + b[h] + ord(a[h % len(a)])) % 256
            b[h], b[f] = b[f], b[h]
            h += 1
        q = f = h = 0
        while q < len(c):
            h = (h + 1) % 256
            f = (f + b[h]) % 256
            b[h], b[f] = b[f], b[h]
            if isinstance(c[q], int):
                result += chr(c[q] ^ b[(b[h] + b[f]) % 256])
            else:
                result += chr(ord(c[q]) ^ b[(b[h] + b[f]) % 256])
            q += 1

        return result

    e_code = trans_e(f_code_1, base64.b64decode(bytes(ep)))
    sid, token = e_code.split('_')
    new_ep = trans_e(f_code_2, '%s_%s_%s' % (sid, vid, token))
    return base64.b64encode(bytes(new_ep)), sid, token

def get_segurls_param(ep,ip):
    new_ep, sid, token = generate_ep(vid, ep)
    m3u8_query = urllib.urlencode(dict(
        ctype=12,
        ep=new_ep,
        ev=1,
        oip=ip,
        token=token
    ))
    return m3u8_query

def get_m3u8url_by_param(vid,ep,ip,stream_id):   
    new_ep, sid, token = generate_ep(vid, ep)
    m3u8_query = urllib.urlencode(dict(
        ctype=12,
        ep=new_ep,
        ev=1,
        keyframe=1,
        oip=ip,
        sid=sid,
        token=token,
        ts=int(time.time()),
        type=stream_id,
        vid=vid
    ))
    m3u8_url =  m3u8_query
    return m3u8_url

def get_urls_by_vid(vid):
    urls = []
    print 'http://v.youku.com/player/getPlayList/VideoIDS/{}/Pf/4/ctype/12/ev/1'.format(vid)
    try:
        meta = json.loads(get_content('http://v.youku.com/player/getPlayList/VideoIDS/{}/Pf/4/ctype/12/ev/1'.format(vid)))
        metadata0 = meta['data'][0]
        stream_ids = metadata0['streamtypes_o']
        ep = metadata0['ep']
        ip = metadata0['ip']
        for stream_id in stream_ids:
            template = {}
            template['rate'] = get_rate(stream_id)
            furls = 'http://pl.youku.com/playlist/m3u8?' + get_m3u8url_by_param(vid,ep,ip,stream_id)
            template['furls'] = [furls]
            urls.append(template)
    except Exception,e:
        print e
        urls = []
    return urls

def get_urls(url):
    urls = []
    try:
        vid = getVideoId(url)
        urls = get_urls_by_vid(vid)
    except Exception,e:
        print e
        urls = []
    return parser2dic(urls)   


if __name__ == '__main__':     
    url = "http://v.youku.com/v_show/id_XODgzOTYwMjI4.html"
#    print get_urls(url)
    vid = getVideoId(url)
    urls = get_urls_by_vid(vid)
    for i in urls:
        print i['furls'][0]      
    print 'Video'
    print get_video(vid, None)
    
