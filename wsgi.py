#!/usr/bin/env python
# -*- coding: utf-8 -*-

import leancloud
import tornado.ioloop
import tornado.web
import tornado.wsgi
import wsgiref.handlers
from app import app
from cloud import engine
from configs import config
configParser = config.configParser
lcConfig = dict(configParser.items('LC_Config'))
import wsgiref.simple_server

APP_ID = lcConfig['lc_app_id']
MASTER_KEY = lcConfig['lc_app_master_key']
PORT = int(lcConfig['lc_app_port'])
leancloud.init(APP_ID, master_key=MASTER_KEY)


application = engine


if __name__ == '__main__':
    server = wsgiref.simple_server.make_server('', 3000, application)
    sa = server.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    server.serve_forever()
