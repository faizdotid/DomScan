import requests
import argparse
from lib.scan import RequestSite
import re

class Lookup:

    def __init__(self, url):
        self.url = url
        self.domain = self.get_root_domain()
        self.results = list()

    def get_root_domain(self):
        if '://' in self.url:
            domain = self.url.split('/')[2]
        elif self.url.endswith('/'):
            domain = self.url.split('/')[0]
        else:
            domain = self.url
        return domain
    
    def request(self, _api):
        try:
            resp = requests.get(_api, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}, timeout=70).text
            if re.search('error', resp):
                return False
            else:
                return resp
        except requests.RequestException:
            print('check ur connection')
            return False

    def reverseip(self):
        api = 'https://api.hackertarget.com/reverseiplookup/?q={}'.format(self.domain)
        _resp = self.request(api)
        if _resp:
            self.results.extend(_resp.splitlines())
        else:
            pass
    
    def subdomain(self):
        api = 'https://api.hackertarget.com/hostsearch/?q={}'.format(self.domain)
        _resp = self.request(api)
        if _resp:
            self.results.extend([url.split(',')[0] for url in _resp.splitlines()])
        else:
            pass

class Main(object):
    def __init__(self, domain, option):
        self.target = domain
        self.option = option

    def _output(self, result_lookup):
        scanner = RequestSite(result_lookup)
        scanner.request()
        _format = '{:<50} - {}'
        if scanner.response:
            domain_target = scanner.get_domain()
            cms = scanner.get_cms()
            server = scanner.get_server()
            http_status_code = scanner.get_status_code()
            _fp = _format.format(domain_target, '{:^15} | {:^5} | {}'.format(cms, http_status_code, server))
            print(_fp)
        else:
            _fp = _format.format('http://'+result_lookup, scanner.invalid)


    def _start(self):
        lookup = Lookup(self.target)
        _getresults = getattr(lookup, self.option)
        _getresults()
        if len(lookup.results) > 0:
            print('Found {} {} in {}'.format(len(lookup.results), self.option, lookup.domain))
            for dom in lookup.results:
                self._output(dom)
        else:
            print('No results found')

Main('klatenkab.go.id', 'subdomain')._start()