# coding: utf-8
import os
import logging

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
        if self.get_argument("code", False):
            print "code"
            self.authorize_redirect(
                redirect_uri='http://localhost:8888/trial',
                client_id=os.getenv('FB_API_KEY'),
                client_secret=os.getenv('FB_API_SECRET'),
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_auth)
            )
            return
        print "redirect"
        self.authorize_redirect(
            redirect_uri='http://localhost:8888/trial',
            client_id=os.getenv('FB_API_KEY'),
            extra_params={"scope": "publish_actions"}
        )

    def _on_auth(self, user):
        if not user:
            raise cyclone.web.HTTPError(500, "Facebook auth failed")
        self.set_secure_cookie("fbdemo_user", cyclone.escape.json_encode(user))
        self.redirect(self.get_argument("next", "/"))


class PostHandler(BaseHandler, cyclone.auth.FacebookGraphMixin):
    @cyclone.web.authenticated
    @cyclone.web.asynchronous
    def get(self):
        print "Posting to facebook wall", self
        self.facebook_request(
            "/me/feed",
            post_args={'message': 'Desde aplicación cyclone'},
            access_token=self.current_user['access_token'],
            callback=self._on_post,
        )

    def _on_post(self, new_entry):
        print "new_entry is", new_entry
        if not new_entry:
            self.redirect('/auth/login')
            return

        self.finish("Posted a message! {}".format(new_entry))


class LangHandler(BaseHandler):
    def get(self, lang_code):
        if lang_code in cyclone.locale.get_supported_locales():
            self.set_secure_cookie("lang", lang_code)

        self.redirect(self.request.headers.get("Referer",
                                               self.get_argument("next", "/")))
