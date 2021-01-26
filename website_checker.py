import requests
import logging
import time
from typing import Dict


class WebsiteChecker:

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }

    DELAY = 1

    CHECK_REGEXP = ''
    CHECK_WORD = 'test'

    def __init__(self, *args, **kwargs):
        self.website_url = args[0]
        self.delay = kwargs.get('delay', WebsiteChecker.DELAY)
        self.headers = kwargs.get('headers', WebsiteChecker.HEADERS)
        self.check_word = kwargs.get('check_word', WebsiteChecker.CHECK_WORD)
        self.check_regexp = kwargs.get('check_regexp', WebsiteChecker.CHECK_REGEXP)

    def start_checker(self):
        while True:
            response = requests.get(self.website_url, headers=self.headers)
            yield self._process_response(response)
            time.sleep(self.delay)

    def _process_response(self, response: requests.Response) -> Dict:
        data = {
            'url': self.website_url,
            'code': response.status_code,
            'time': response.elapsed.total_seconds(),
            'content_check': self._content_check(response.text)
        }
        return data

    def _content_check(self, page_content) -> bool:
        return self.check_word in page_content
