#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import requests as _req

class Api(object):
    """Main object for working with api"""
    def __init__(self, nick, passwd):
        super(Api, self).__init__()

        self.domain = "http://shikimori.org/api/"

        self.nick = nick
        self.passwd = passwd

        self.token = _req.get(self.domain + "access_token?nickname={}&password={}".format(self.nick, self.passwd)).json()["api_access_token"]

        self.headers = {"X-User-Nickname": self.nick,
                        "X-User-Api-Access-Token": self.token}
        self.s = _req.Session() # Session for http-requests
        self.s.headers.update(self.headers)

    def _makeReq(self, request, meth):
        args = request._method_args
        req_url = self.domain + request._method_name
        if meth == "get":
            r = self.s.get(req_url, params=args)
        elif meth == "post":
            r = self.s.post(req_url, json=args)
        elif meth == "patch":
            r = self.s.patch(req_url, json=args)
        elif meth == "put":
            r = self.s.put(req_url, json=args)
        elif meth == "delete":
            r = self.s.delete(req_url)
        return r.json()


    def __str__(self):
        return "<API-object nickname={} token={}>".format(self.nick, self.token)

    
    def __getattr__(self, method_name):
        return Request(self, method_name)


class Request(object):
    __slots__ = ('_api', '_method_name', '_method_args')

    def __init__(self, api, method_name):
        self._api = api
        self._method_name = method_name

    def __call__(self, path, **method_args):
        self._method_name += "/" + path
        self._method_args = method_args
        return self

    def get(self):
        return self._api._makeReq(self, "get")

    def post(self, **args):
        return self._api._makeReq(self, "post")

    def patch(self, **args):
        return self._api._makeReq(self, "patch")

    def put(self, **args):
        return self._api._makeReq(self, "put")

    def delete(self, **args):
        return self._api._makeReq(self, "delete")

