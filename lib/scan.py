import requests
import re
from colorama import Fore, init as colorama_init


class RequestSite:
    def __init__(self, domain):
        self.domain = 'http://'+domain
        self.invalid = Fore.RED + 'Unknown'
        self.valid = Fore.GREEN + '{}'

    def request(self):
        try:
            self.response = requests.get(self.domain, headers={
                                         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}, timeout=10, allow_redirects=True)
        except KeyboardInterrupt:
            print(Fore.RED + "CTRL + C Detected\nExiting Tools....")
            exit()
        except:
            self.response = False

    def get_server(self):
        try:
            _server = self.valid.format(self.response.headers['Server'])
        except:
            _server = self.invalid
        finally:
            return _server

    def get_status_code(self):
        try:
            _status_code = self.valid.format(str(self.response.status_code))
        except:
            _status_code = self.invalid
        finally:
            return _status_code

    def get_cms(self):
        conf = {
            'WordPress': {
                'text': 'wp-content',
                'context': self.response.text
            },
            'Drupal': {
                'text': '/sites/default/files/',
                'context': self.response.text
            },
            'Joomla': {
                'text': 'com_content',
                'context': self.response.text
            },
            'Laravel': {
                'text': 'laravel_session|XSRF-TOKEN',
                'context': self.response.headers
            },
        }
        for key, value in conf.items():
            if re.search(value['text'], value['context']):
                return self.valid.format(key)
            else:
                return self.invalid

    # def get_domain(self):
    #     url = self.response.url
    #     urls = url.split('/')
    #     _url = urls[0] + '//' + urls[2]
    #     return _url
