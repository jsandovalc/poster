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
                callback=self.async_callback(self._on_login)
            )
            return
        print "redirect"
        self.authorize_redirect(
            redirect_uri='http://localhost:8888/trial',
            client_id=os.getenv('FB_API_KEY'),
            extra_params={"scope": "read_stream"}
        )

    def _on_login(self):
        logging.error(user)
        self.finish()

    def post(self):
        tpl_fields = TemplateFields()
        tpl_fields['post'] = True
        tpl_fields['ip'] = self.request.remote_ip
        # you can also fetch your own config variables defined in
        # poster.conf using
        # self.settings.raw.get('section', 'parameter')
        tpl_fields['mysql_host'] = self.settings.raw.get('mysql', 'host')
        self.render("post.html", fields=tpl_fields)


class LangHandler(BaseHandler):
    def get(self, lang_code):
        if lang_code in cyclone.locale.get_supported_locales():
            self.set_secure_cookie("lang", lang_code)

        self.redirect(self.request.headers.get("Referer",
                                               self.get_argument("next", "/")))
