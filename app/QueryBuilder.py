import requests
from urllib.parse import urlencode
from urllib.request import urlretrieve

from BookParser import *
from Category import *

class RequestBuilder(object):
    _domain = 'http://off.aladin.co.kr'
    _path = 'usedstore/wsearchresult.aspx'

    PARAM_NAME_KEYWORD = 'SearchWord'
    PARAM_NAME_X = 'x'
    PARAM_NAME_Y = 'Y'


    def __init__(self):
        self.url_params = {}
        self.cookie_params = {}

    def set_params(self, key, value):
        self.url_params[key] = value
        return self

    def set_store(self, storeCode):
        self.cookie_params['OffCode'] = storeCode
        return self

    def make_params(self, key, x, y):
        return dict(SearchWord=key, x=x, y=y)

    def get(self):
        cookies = dict(AladinUsedStore=urlencode(self.cookie_params))

        return requests.get('{}/{}'.format(self._domain, self._path),
                            cookies=cookies, params=self.url_params)


if __name__ == '__main__':
    keyword = 'hello'
    req_builder = RequestBuilder()

    for name, code in Category.stores.items():
        req_builder.set_params(req_builder.PARAM_NAME_KEYWORD, keyword) \
                   .set_params(req_builder.PARAM_NAME_X, 1) \
                   .set_params(req_builder.PARAM_NAME_Y, 2) \
                   .set_store(code)
        res = req_builder.get()

        book_parser = BookParser(res)
        found = book_parser.parse()

        print(name)
        for line in found:
            print(line)
        print()
