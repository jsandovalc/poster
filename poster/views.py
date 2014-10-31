# coding: utf-8
# This file is part of Poster.

#     Poster is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     Poster is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with Poster.  If not, see <http://www.gnu.org/licenses/>.

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
        self.render("index.html", hello='world',
                    awesome='I am')

class AuthLoginHandler(BaseHandler, cyclone.auth.FacebookGraphMixin):
    @cyclone.web.asynchronous
    def get(self):
        my_url = ("http://localhost:8888/auth/login?next=" +
                  cyclone.escape.url_escape(
                      self.get_argument("next", "/"))
        )
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri=my_url,
                client_id=os.getenv('FB_API_KEY'),
                client_secret=os.getenv('FB_API_SECRET'),
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_auth)
            )
            return
        self.authorize_redirect(
            redirect_uri=my_url,
            client_id=os.getenv('FB_API_KEY'),
            extra_params={"scope": "read_stream,publish_actions"}
        )

    def _on_auth(self, user):
        if not user:
            raise cyclone.web.HTTPError(500, "Facebook auth failed")
        # TODO: Change fbdemo_user name
        self.set_secure_cookie("fbdemo_user", cyclone.escape.json_encode(user))
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
        self.finish(json.dumps({'message': 'Post created'}))


class LangHandler(BaseHandler):
    def get(self, lang_code):
        if lang_code in cyclone.locale.get_supported_locales():
            self.set_secure_cookie("lang", lang_code)

        self.redirect(self.request.headers.get("Referer",
                                               self.get_argument("next", "/")))
