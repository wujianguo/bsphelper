#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os.path
import tornado.ioloop
import tornado.web
import tornado.wsgi
import requests
import logging


class BuddybuildHandler(tornado.web.RequestHandler):

    def post(self):
        logging.error(self.request.body)
        headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI1NmM3ZWM4MzNiY2ZmMzAxMDA4NTY5YmUiLCJpYXQiOjE0NTU5NjIzNzIxMzQsImV4cCI6MTQ1NTk4MDM3MjEzNH0.ZFzUmadAo5rO-nkd42VRhn7d0l0v_3J9ceVtX9kQSWM"}
        r = requests.post("https://dashboard.buddybuild.com/api/apps/56c80da323276801006af4ed/build?branch=master", headers=headers)
        if r.json().get("error", None):
            self.write(json.dumps({"text": "error:" + r.json().get("error", "")}))
        else:
            self.write(json.dumps({"text": "deploy 开始成功，正在编译。。。"}))

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
        logging.error(self.request.body)
        msg = json.loads(self.request.body)
        fallback = msg["attachments"][0]["fallback"]
        if fallback.find("succeeded") != -1 and pgyer:
            self.response_success(pgyer)
        else:
            requests.post("https://hooks.slack.com/services/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", data=self.request.body)
        self.write("ok")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "public"),
    "template_path": os.path.join(os.path.dirname(__file__), "views"),
    "gzip": True,
    "debug": True
}

application = tornado.web.Application([
    (r"/slack", SlackHandler),
    (r"/buddybuild", BuddybuildHandler)
], **settings)

app = tornado.wsgi.WSGIAdapter(application)


def main():
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
