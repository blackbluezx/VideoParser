#_*_coding:utf-8_*_
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpclient
from tornado.options import define, options
import sys
import os
from urllib import quote
import urlhandler
import extractor.flvcd as FLVCD
from extractor.common import parser2dic
from extractor.common import r2,r1
sys.path.append(r'..')

define ("port", default=8527, help="run on the given port", type=int)

from tornado.web import RequestHandler
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

class TemplateRendering:
    """
    A simple class to hold methods for rendering templates.
    """
    def render_template(self, template_name, **kwargs):
        template_dirs = [r'../templates']
        if self.settings.get('template_path', ''):
            template_dirs.append(
                self.settings["template_path"]
            )
        env = Environment(loader=FileSystemLoader(template_dirs))

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


class BaseHandler(RequestHandler, TemplateRendering):
    """
    RequestHandler already has a `render()` method. I'm writing another
    method `render2()` and keeping the API almost same.
    """
    def render2(self, template_name, **kwargs):
        """
        This is for making some extra context variables available to
        the template
        """
        kwargs.update({
            'settings': self.settings,
            'STATIC_URL': self.settings.get('static_url_prefix', '/static/'),
            'request': self.request,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
        })
        content = self.render_template(template_name, **kwargs)
        self.write(content)


class MainHandler(BaseHandler):
    """ 主要处理句柄，负责接收客户端请求，并返回相应的urls"""
    def get(self,website):
        burl = self.get_argument('url', '')
        print self.request.remote_ip,'SiteUrl:',burl
        source = self.getsources(burl)
        if source == []:
            print source
        print 'len:',len(source)
        self.set_header('Content-Type', 'application/xml')
        self.render2('template.xml',source=source)
        self.finish()
        
    def getsources(self, url):
        return urlhandler.GetUrlsFromSites(url)
        
class JustNowHandler(BaseHandler):
    def get(self,website):
        self.write("i hope just now see you")

rate = ['标清','高清','超清']
form = ['','high','super']

class AsyncHandler(BaseHandler):
#    def prepare_curl_socks5(self,curl):
#        curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self,website):
        burl = self.get_argument('url', '')   
        print self.request.remote_ip,'SiteUrlAsync:',burl
        urls = []
        ##FLVCD
        for i in range(0,3):
            template = {}
            furl = "http://www.flvcd.com/parse.php?format={}&kw={}".format(form[i],quote(burl))
            tornado.httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
            client = tornado.httpclient.AsyncHTTPClient()
#            client.set_proxy("61.150.12.10","8118")
#            request = tornado.httpclient.HTTPRequest(
#                                             url = furl,
#                                             proxy_host='202.107.233.85',
#                                             proxy_port=8080
#                                            )                                            
            response = yield tornado.gen.Task(client.fetch,furl)
            content = response.body
            furls = r2('<BR><a href=\"(.*?)\" target=',content)
            if furls!= []:
                print 'flvcd multi'
                template['rate'] = rate[i]
                template['furls'] = furls
                urls.append(template)
            else:
                sfurls = r1('<br>.*?<a href=\"(.*?)\" target',content)
                if(sfurls!=None):
                    print 'flvcd single'
                    template['rate'] = rate[i]
                    template['furls'] = [sfurls]
                    urls.append(template)
        source = parser2dic(urls)
        self.set_header('Content-Type', 'application/xml')
        self.render2('template.xml',source=source)
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
    "static_path": os.path.join(os.path.dirname(os.getcwd()), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "xsrf_cookies": True,
    }
    app = tornado.web.Application(handlers=[(r"/(\w+)/video", MainHandler) ,\
                                            (r"/(\w+)/now",JustNowHandler) ,\
                                            (r"/(\w+)/video1",AsyncHandler) ,\
                                            (r"/(favicon\.ico|\w+\.py)", tornado.web.StaticFileHandler, dict(path=settings['static_path']))], **settings)
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
