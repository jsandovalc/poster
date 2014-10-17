#-*- coding: utf-8 -*-
#
# Copyright 2014 Foo Bar
# Powered by cyclone

import cyclone.locale
import cyclone.web

import views
import config


class Application(cyclone.web.Application):
    def __init__(self, config_file):
        handlers = [
            (r"/", views.IndexHandler),
            (r"/auth/login", views.AuthLoginHandler),
            (r"/trial", views.PostHandler),
            (r"/lang/(.+)", views.LangHandler),
        ]

        settings = config.parse_config(config_file)

        # Initialize locales
        locales = settings.get("locale_path")
        if locales:
            cyclone.locale.load_gettext_translations(locales, "poster")

        settings["login_url"] = "/auth/login"
        #settings["autoescape"] = None
        print "settings are", settings
        cyclone.web.Application.__init__(self, handlers, **settings)
