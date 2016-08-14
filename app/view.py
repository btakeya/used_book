import logging
from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import unquote

from .QueryBuilder import *


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def index_page(request):
    response = render(request, 'page/index.html', {})
    return response

def get_used_book(request, keyword='key'):
    log.info('[UB] Keyword raw: {}'.format(keyword))
    raw_keyword = request.GET.get('keyword')
    log.info('[UB] Keyword in: {}'.format(raw_keyword))
    euckr_keyword = raw_keyword.encode('euc-kr')
    log.info('[UB] Keyword encoded: {}'.format(euckr_keyword))
    req_builder = RequestBuilder()
    branches = {'STORE_NAME_GANGNAM': Category.stores['STORE_NAME_GANGNAM'],
                'STORE_NAME_BUNDANG': Category.stores['STORE_NAME_BUNDANG']}

    response_str = ['<p>']

    for name, code in branches.items():
        req_builder.set_params(req_builder.PARAM_NAME_KEYWORD, euckr_keyword) \
                   .set_params(req_builder.PARAM_NAME_X, 1) \
                   .set_params(req_builder.PARAM_NAME_Y, 2) \
                   .set_store(code)
        res = req_builder.get()

        book_parser = BookParser(res)
        found = book_parser.parse()

        log.info('[UB] Searching for books in Branch {}'.format(name))
        response_str.append(name)
        for line in found:
            response_str.append(line)
        response_str.append('')

    response_str.append('</p>')

    response = HttpResponse('<br />'.join(response_str))
    return response
