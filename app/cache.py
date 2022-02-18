import requests
import re


class Cache:
    def __init__(self, **kwargs):
        self.url = 'https://raw.githubusercontent.com/{}/master/'.format(
                kwargs.get('repo'))
        self.tm = 'https://api.github.com/repos/{}/commits'.format(
                kwargs.get('repo'))
        self.cache = kwargs.get('file')
        self.pattern = re.compile(
                '^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}')

    def parse(self):
        res = requests.get(url='{}{}'.format(self.url, self.cache)).json()
        dns_list = []
        for i in res['cache_domains']:
            name = i['name']
            result = requests.get(
                    url=self.url + i['domain_files'][0]).text.splitlines()
            for n in result:
                if(re.search(self.pattern, n)):
                    dns_list.append(tuple((name, n, self._tm)))
        return dns_list

    def check_tm(self, repo):
        self.tm = 'https://api.github.com/repos/{}/commits'.format(repo)
        return self._tm

    @property
    def tm(self): return self._tm

    @tm.setter
    def tm(self, url):
        self._tm = requests.get(url).json(
                )[0]['commit']['author']['date'].replace(
                        'T', ' ').replace('Z', ' ').strip()

    @tm.deleter
    def tm(self):
        del self._tm
