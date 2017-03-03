# -*- coding: utf-8 -*-

class APIError(Exception):
    def __init__(self, status, info):
        self.status = status
        self.info = info
    def __str__(self):
        return repr((self.status, self.info))
