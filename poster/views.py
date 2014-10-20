# -*- coding: utf-8 -*-
import os
import logging
import json

import cyclone.escape
import cyclone.locale
import cyclone.web
import cyclone.auth

from twisted.internet import defer
from twisted.python import log

from utils import BaseHandler
from utils import TemplateFields


class IndexHandler(BaseHandler, cyclone.auth.FacebookGraphMixin):
    def get(self):
        self.write("Probando")

class AuthLoginHandler(BaseHandler, cyclone.auth.FacebookGraphMixin):
    @cyclone.web.asynchronous
    def get(self):
        print "trying"
        my_url = ("http://localhost:8888/auth/login?next=" +
                  cyclone.escape.url_escape(
                      self.get_argument("next", "/"))
        )
        print "to", my_url
        if self.get_argument("code", False):
            print "code", self.get_argument("code", False)
            self.get_authenticated_user(
                redirect_uri=my_url,
                client_id=os.getenv('FB_API_KEY'),
                client_secret=os.getenv('FB_API_SECRET'),
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_auth)
            )
            return
        print "redirect"
        self.authorize_redirect(
            redirect_uri=my_url,
            client_id=os.getenv('FB_API_KEY'),
            extra_params={"scope": "read_stream,publish_actions"}
        )

    def _on_auth(self, user):
        print "on auth", user
        if not user:
            print "no user"
            raise cyclone.web.HTTPError(500, "Facebook auth failed")
        print "there is user :)"
        # TODO: Change fbdemo_user name
        self.set_secure_cookie("fbdemo_user", cyclone.escape.json_encode(user))
        print "going to", self.get_argument("next", "/")
        self.redirect(self.get_argument("next", "/"))


class PostHandler(BaseHandler, cyclone.auth.FacebookGraphMixin):
    @cyclone.web.authenticated
    @cyclone.web.asynchronous
    def post(self):
        # TODO: must check sent content type, return 415
        self.set_header("Content-type", "application/json; charset=utf-8")
        try:
            body = json.loads(self.request.body)
        except ValueError:
            self.set_status(400, "Bad json")
            # TODO: Add code
            self.finish(json.dumps({'message': "Bad json sent"}))
            return
        if 'message' not in body:
            self.set_status(422, "Message not sent")
            self.finish(json.dumps({'message': 'must send message'}))

        self.facebook_request(
            "/me/feed",
            callback=self.async_callback(self._on_post),
            access_token=self.current_user['access_token'],
            post_args={'message': body['message']},
        )

    def _on_post(self, new_entry):
        if not new_entry:
            self.redirect('/auth/login')
            return
        self.set_status(201)
        print "new_entry", new_entry
        self.finish(json.dumps({'message': 'Post created'}))


class LangHandler(BaseHandler):
    def get(self, lang_code):
        if lang_code in cyclone.locale.get_supported_locales():
            self.set_secure_cookie("lang", lang_code)

        self.redirect(self.request.headers.get("Referer",
                                               self.get_argument("next", "/")))
