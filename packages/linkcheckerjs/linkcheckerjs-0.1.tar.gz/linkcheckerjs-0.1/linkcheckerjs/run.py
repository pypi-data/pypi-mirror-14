#!/usr/bin/env python

import os
import re
import json
import logging
import threading

from urlparse import urlparse
from optparse import OptionParser
from collections import OrderedDict

from . import thread, reader
from .exc import CheckerException
from .checker import (
    phantomjs_checker,
    requests_checker,
    standardize_url,
)

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(thread)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
log.addHandler(handler)


IGNORED_URL_PREFIXES = ['javascript:', 'data:', 'mailto:']


class Linkchecker(object):

    def __init__(self, pool, ignore_ssl_errors=False,
                 ignore_url_patterns=None, domains=None, maxdepth=None,
                 timeout=None):
        self.pool = pool
        # Option passed to phantomjs
        self.ignore_ssl_errors = ignore_ssl_errors

        self.ignored_urls_regex = set(re.compile(p)
                                      for p in ignore_url_patterns or [])
        self.valid_domains = domains or []
        self.maxdepth = maxdepth
        self.timeout = timeout

        self.__checkLock = threading.Condition(threading.Lock())
        self.results = OrderedDict()

        # Security to not crawl all the web
        self.max_nb_urls = 50000

    def check(self, url, parent_url=None, depth=0):
        try:
            result = phantomjs_checker(
                url, parent_url=parent_url,
                ignore_ssl_errors=self.ignore_ssl_errors)
        except CheckerException as e:
            if self.results.get(url) is None:
                self.results[url] = {
                    'checker': 'phantomjs_checker',
                    'url': standardize_url(url),
                    'redirect_url': None,
                    'status_code': 500,
                    'status': 'Internal Error - %s' % unicode(e),
                    'parent_url': parent_url,
                }
                return

        for page in result:
            if self.results.get(page['url']) is None:
                self.results[page['url']] = page

        if len(self.results) > self.max_nb_urls:
            return
        self.feed_result(url, result[-1], depth+1)

    def quick_check(self, url, parent_url=None):
        try:
            result = requests_checker(url, parent_url=parent_url,
                                      ignore_ssl_errors=self.ignore_ssl_errors)
            for page in result:
                if self.results.get(page['url']) is None:
                    self.results[page['url']] = page
        except CheckerException as e:
            if self.results.get(url) is None:
                self.results[url] = {
                    'checker': 'requests',
                    'url': standardize_url(url),
                    'redirect_url': None,
                    'status_code': 500,
                    'status': 'Internal Error - %s' % unicode(e),
                    'parent_url': parent_url,
                }

    def schedule(self, url, parent_url=None, new_depth=0):
        too_far = False
        if self.maxdepth is not None:
            if new_depth > (self.maxdepth + 1):
                # We are too far
                return
            if new_depth > self.maxdepth:
                # Check the link with requestspy
                too_far = True
        self.results[standardize_url(url)] = None

        if too_far or urlparse(url).hostname not in self.valid_domains:
            self.pool.add_task(self.quick_check, parent_url=parent_url,
                               url=url)
        else:
            self.pool.add_task(self.check, url=url, parent_url=parent_url,
                               depth=new_depth)

    def filter_urls(self, urls):
        return (u for u in urls
                if not any(u.startswith(p) for p in IGNORED_URL_PREFIXES))

    def filter_ignore_urls_patterns(self, urls):
        return (u for u in urls
                if not any(r.search(u) for r in self.ignored_urls_regex))

    def feed_result(self, url, result, new_depth):
        urls_to_check = self.filter_urls(result['urls'])
        urls_to_check = self.filter_ignore_urls_patterns(urls_to_check)

        # Feed discovered url to the checker
        self.__checkLock.acquire()
        try:
            for next_url in urls_to_check:
                if next_url in self.results:
                    continue
                self.schedule(next_url, url, new_depth)
        finally:
            self.__checkLock.release()

    def wait(self):
        self.pool.join_all()


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="Urls list", metavar="FILE")
    parser.add_option("-o", "--output", dest="output",
                      help="Json output file", metavar="FILE")
    parser.add_option("-i", "--ignore-ssl-errors", action="store_true",
                      dest="ignore_ssl_errors",
                      help="Ignore ssl errors for self signed certificate")
    parser.add_option("-d", "--max-depth", dest="maxdepth", type="int")
    parser.add_option("-t", "--thread", dest="thread", type="int", default=8)
    parser.add_option("--timeout", dest="timeout", type="int", default=5)
    parser.add_option("--ignore-url-pattern", action="append",
                      dest="ignore_url_patterns",
                      help="Pattern to ignore when crawling pages")
    parser.add_option("-v", "--verbose", action="store_true",
                      dest="verbose")

    # Linkreader options
    parser.add_option("-l", "--log-level", type="int", dest="log_level",
                      help="linkcheckerjs log level")
    (options, args) = parser.parse_args()

    if options.filename is None and not args:
        raise Exception('Filename required')

    if options.verbose:
        handler.setLevel(logging.DEBUG)
        thread.handler.setLevel(logging.DEBUG)

    if options.filename:
        with open(options.filename, 'r') as f:
            urls = [url for url in f.readlines()]
    else:
        urls = args

    # Create a pool
    log.debug('Starting pool with %i threads' % options.thread)
    pool = thread.ThreadPool(options.thread)

    linkchecker = Linkchecker(
        pool,
        ignore_url_patterns=options.ignore_url_patterns,
        ignore_ssl_errors=options.ignore_ssl_errors,
        maxdepth=options.maxdepth,
        domains=set(urlparse(url).hostname for url in urls),
        timeout=options.timeout,
    )

    for url in urls:
        url = url.strip()
        linkchecker.schedule(url)

    linkchecker.wait()

    if options.output:
        with open(options.output, 'w') as f:
            json.dump(linkchecker.results, f)
    else:
        reader.terminal_output(linkchecker.results,
                               options_log_level=options.log_level)


if __name__ == "__main__":
    main()
