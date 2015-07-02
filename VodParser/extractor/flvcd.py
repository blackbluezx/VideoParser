#!/usr/bin/env python
#_*_coding:utf-8_*_

from urllib import quote
from common import get_content,r2,r1,parser2dic

rate = ['标清','高清','超清']
form = ['','high','super']

def get_urls(url):
    urls = []
    for i in range(0,3):
        template = {}
        flvcdurl = "http://www.flvcd.com/parse.php?format={}&kw={}".format(form[i], quote(url))
        content = get_content(flvcdurl)
        furls = r2('<BR><a href=\"(.*?)\" target=',content)
        if furls!= []:
            print 'flvcd multi'
            template['rate'] = rate[i]
            template['furls'] = furls
            urls.append(template)
        else:
            print 'flvcd single'
            sfurls = r1('<br>.*?<a href=\"(.*?)\" target',content)
            print 'sfurls',sfurls
            if(sfurls!=None):
                template['rate'] = rate[i]
                template['furls'] = [sfurls]
                urls.append(template)

    return parser2dic(urls)
    

if __name__ == '__main__':
    print get_urls("http://www.hunantv.com/v/3/50877/f/1002068.html#")
#    print get_urls("http://v.youku.com/v_show/id_XNzc5NzMwMDQ4.html?from=y1.3-movie-grid-1095-9921.86994-86993.4-1")   