from bs4 import *


logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)


class BookParser(object):
    def __init__(self, result):
        self.page = result.text
        self.soup = BeautifulSoup(self.page, 'html.parser')

    def parse(self):
        results = []
        divs = self.soup.findAll('div')
        for div in divs:
            div_class_list = div.get('class')
            if type(div_class_list) is list and \
               'ss_book_box' in div.get('class'):
                search_text = div.get_text()
                for line in search_text.split('\n'):
                    if len(line) > 0:
                        results.append(line)

        return results
