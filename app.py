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

    def response_success(self, pgyer):
        title_url = "https://www.pgyer.com/" + pgyer
        image_url = "https://o1wjx1evz.qnssl.com/app/qrcode/" + pgyer
        payload = {
            "icon_url": "https://s3-us-west-2.amazonaws.com/buddybuild-public/assets/slack-lolo-icon.png",
            "parse": "none",
            "username": "buddybuild",
            "attachments": [
                {
                    "fallback": "湾视 iOS 新版发布",
                    "color": "good",
                    "title": "湾视 iOS 新版发布，点击或扫描二维码安装",
                    "title_link": title_url,
                    "image_url": image_url
                }
            ]
        }
        requests.post("https://hooks.slack.com/services/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", data=json.dumps(payload))

    def post(self):
        pgyer = self.get_query_argument("pgyer", None)
        try:
            msg = json.loads(self.request.body)
            fallback = msg["attachments"][0]["fallback"]
            if fallback.find("succeeded") != -1 and pgyer:
                return self.response_success(pgyer)
            else:
                requests.post("https://hooks.slack.com/services/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", data=self.request.body)
        except:
            pass
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
