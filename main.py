import requests
import argparse
from lib.scan import RequestSite, Fore, colorama_init
import re

colorama_init(autoreset=True)


class Lookup:

    def __init__(self, url):
        self.url = url
        self.domain = self.get_root_domain()
        self.results = list()

    def get_ip(self):
        try:
            ip = socket.gethostbyname(self.domain)
        except:
            ip = self.domain
        finally:
            return ip
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
            resp = requests.get(_api, headers={
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}, timeout=70).text
            if re.search('error|API count exceeded', resp):
                return False
            else:
                return resp
        except requests.RequestException:
            print(Fore.RED + "Please Check Ur Connection!!!")
            return False

    def reverseip(self):
        api = 'https://api.hackertarget.com/reverseiplookup/?q={}'.format(
            self.get_ip())
        _resp = self.request(api)
        if _resp:
            self.results.extend(_resp.splitlines())
        else:
            pass

    def subdomain(self):
        api = 'https://api.hackertarget.com/hostsearch/?q={}'.format(
            self.domain)
        _resp = self.request(api)
        if _resp:
            self.results.extend([url.split(',')[0]
                                for url in _resp.splitlines()])
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
            cms = scanner.get_cms()
            server = scanner.get_server()
            http_status_code = scanner.get_status_code()
            _fp = _format.format('http://'+result_lookup, '{:^25} | {:^30} | {}'.format(
                cms + Fore.WHITE, http_status_code + Fore.WHITE, server))
            print(_fp)
        else:
            _fp = _format.format('http://'+result_lookup, scanner.invalid)
            print(_fp)

    def _start(self):
        try:
            _fm = "{:^50} - {}"
            lookup = Lookup(self.target)
            _getresults = getattr(lookup, self.option)
            _getresults()
            if len(lookup.results) > 0:
                print('Found {} {} in {}\n'.format(
                    len(lookup.results), self.option, lookup.domain))
                print(_fm.format("Domain", '{:^20} | {:^25} | {}'.format(
                    "CMS" + Fore.WHITE, "HTTP Code" + Fore.WHITE, "Server")))
                for dom in lookup.results:
                    self._output(dom)
            else:
                print('No results found for domain {}'.format(self.target))
        except KeyboardInterrupt:
            print(Fore.RED + "CTRL + C Detected\nExiting Tools....")
            exit()


print(Fore.GREEN + """
█▀▄ █▀█ █▀▄▀█ █▀ █▀▀ ▄▀█ █▄░█
█▄▀ █▄█ █░▀░█ ▄█ █▄▄ █▀█ █░▀█
Simple D0main Scanner\n""")
parser = argparse.ArgumentParser(
    prog="main", description="Domain Scanner", usage="%(prog)s domain [option]")
parser.add_argument("-u", "--url", required=True,
                    type=str, help="Domain to scan")
parser.add_argument(
    "-o", "--option", choices=["reverseip", "subdomain"], required=True, help="Option to scan")

args = parser.parse_args()

if args:
    Main(domain=args.url, option=args.option)._start()
else:
    parser.print_help()
