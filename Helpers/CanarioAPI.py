#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests

# https://github.com/CanaryPW/Canary-Python

# Canary-Python - A framework for the Canary API
# Copyright (C) 2014 Colin Keigher (colin@keigher.ca)

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


class canary(object):

    def __init__(s, api_key, host=None, debug=False):
        s.api_key = api_key
        if debug:  # This is really for me and nothing else.
            s.url = 'http://%s/_api/?key=%s' % (host, api_key)
        else:
            s.url = 'https://canar.io/_api/?key=%s' % api_key
        s.data = None

    # Simple request made
    def retrieve(s, url, data=None, post=False):
        if post:
            r = requests.post(url, data=data)
        else:
            r = requests.get(url)
        if r.status_code == 200:
            s.data = json.loads(r.text)

    # 'data' must be in the form of a dictionary
    def build_url(s, data):
        d = ['%s=%s' % (x, y) for x, y in data.iteritems()]
        return '%s&%s' % (s.url, '&'.join(d))

    # Does a search--whee. Bangs can be specified via separate argument. This is due to plan to make changes to the search for API users
    # in the future.
    def search(s, query, bang=None):
        if bang is not None:
            query = '!%s %s' % (bang, query)
        url = s.build_url({'action': 'search', 'query': query})
        s.retrieve(url=url)
        return s.data

    # Views a reference ID. Nothing special.
    def view(s, item):
        url = s.build_url({'action': 'view', 'item': item})
        s.retrieve(url=url)
        return s.data

    # Users with the ability to submit data can use this to send. This is not
    # documented.
    def store(s, title, text, source, source_url):
        if title is None:
            title = 'Untitled'
        data = {'title': title, 'text': text,
                'source': source, 'source_url': source_url}
        url = s.build_url({'action': 'store'})
        s.retrieve(url=url, data=data, post=True)
