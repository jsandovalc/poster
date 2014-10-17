# coding: utf-8
#
# Copyright 2014 Jonathan Sandoval
# Powered by cyclone

import cyclone.escape
import cyclone.web

from twisted.enterprise import adbapi


class TemplateFields(dict):
    """Helper class to make sure ourp
        template doesn't fail due to an invalid key"""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        self[name] = value


class BaseHandler(cyclone.web.RequestHandler):
    def get_current_user(self):
        print "in current user"
        user_json = self.get_secure_cookie("fbdemo_user")
        if user_json:
            print "returnig", user_json
            return cyclone.escape.json_decode(user_json)

        print "not returning :("

    def get_user_locale(self):
        lang = self.get_secure_cookie("lang")
        if lang:
            return cyclone.locale.get(lang)
