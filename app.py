#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os.path
import tornado.ioloop
import tornado.web
import tornado.wsgi
import requests
import logging


class SlackHandler(tornado.web.RequestHandler):

    def post(self):
        print(self.request.body)
        logging.error(self.request.body)
        self.write("ok")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "public"),
    "template_path": os.path.join(os.path.dirname(__file__), "views"),
    "gzip": True,
    "debug": True
}

application = tornado.web.Application([
    (r"/slack", SlackHandler),
], **settings)

app = tornado.wsgi.WSGIAdapter(application)


def main():
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
