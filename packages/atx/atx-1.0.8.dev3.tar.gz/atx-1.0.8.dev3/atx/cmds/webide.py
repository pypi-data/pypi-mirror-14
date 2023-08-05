# coding: utf-8

import os
import logging
import webbrowser
import socket

import tornado.ioloop
import tornado.web
import tornado.websocket

from atx import logutils
from atx import base


__dir__ = os.path.dirname(os.path.abspath(__file__))

log = logutils.getLogger("webide")
log.setLevel(logging.DEBUG)


IMAGE_PATH = ['.', 'imgs', 'images']
workdir = '.'

def read_file(filename, default=''):
    if not os.path.isfile(filename):
        return default
    with open(filename, 'rb') as f:
        return f.read()

def write_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def get_valid_port():
    for port in range(10010, 10100):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        if result != 0:
            return port

    raise SystemError("Can not find a unused port, amazing!")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        imgs = base.list_images(path=IMAGE_PATH)
        imgs = [(os.path.basename(name), name) for name in imgs]
        self.render('index.html', images=imgs)

    def post(self):
        print self.get_argument('xml_text')
        self.write("Good")


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket connected")
        # imgs = base.list_images(path=IMAGE_PATH)
        # imgs = [dict(
        #     path=name.replace('\\', '/'), name=os.path.basename(name)) for name in imgs]
        # self.write_message({'images': list(imgs)})

    def on_message(self, message):
        if message == 'refresh':
            imgs = base.list_images(path=IMAGE_PATH)
            imgs = [dict(
                path=name.replace('\\', '/'), name=os.path.basename(name)) for name in imgs]
            self.write_message({'images': list(imgs)})
        else:
            self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
    
    def check_origin(self, origin):
        return True


class WorkspaceHandler(tornado.web.RequestHandler):
    def get(self):
        ret = {}
        ret['xml_text'] = read_file('blockly.xml', '<xml xmlns="http://www.w3.org/1999/xhtml"></xml>')
        ret['python_text'] = read_file('blockly.py')
        self.write(ret)

    def post(self):
        log.debug("Save workspace")
        xml_text = self.get_argument('xml_text')
        python_text = self.get_argument('python_text')
        write_file('blockly.xml', xml_text)
        write_file('blockly.py', python_text)


class StaticFileHandler(tornado.web.StaticFileHandler):
    def get(self, path=None, include_body=True):
        path = path.encode(base.SYSTEM_ENCODING) # fix for windows
        super(StaticFileHandler, self).get(path, include_body)


def make_app(settings={}):
    static_path = os.getcwd()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/workspace", WorkspaceHandler),
        (r'/static_imgs/(.*)', StaticFileHandler, {'path': static_path}),
        (r'/ws', EchoWebSocket),
    ], **settings)
    return application


def main(**kws):
    application = make_app({
        'static_path': os.path.join(__dir__, 'static'),
        'template_path': os.path.join(__dir__, 'static'),
        'debug': True,
    })
    port = kws.get('port', None)
    if not port:
        port = get_valid_port()

    global workdir
    workdir = kws.get('workdir', '.')

    open_browser = kws.get('open_browser', True)
    if open_browser:
        url = 'http://127.0.0.1:{}'.format(port)
        webbrowser.open(url, new=2) # 2: open new tab if possible

    application.listen(port)
    log.info("Listening port on 127.0.0.1:{}".format(port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
