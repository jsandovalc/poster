# -*- coding: utf-8 -*-
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


from twisted.trial import unittest
from twisted.internet import defer
from mock import patch, MagicMock
from poster.views import PostHandler


class TestPostHandler(unittest.TestCase):
    def setUp(self):
        self.app = app = MagicMock()
        app.ui_methods = {}
        app.ui_modules = {}
        self.request = request = MagicMock()
        request.headers = {}
        request.method = "POST"
        request.version = "HTTP MOCK"
        request.notifyFinish.return_value = defer.Deferred()
        request.supports_http_1_1.return_value = True
        self.handler = PostHandler(app, request)

    @patch('cyclone.auth.httpclient.fetch')
    def test_post(self, mock):
        print 'prueba'
        self.handler.post()
