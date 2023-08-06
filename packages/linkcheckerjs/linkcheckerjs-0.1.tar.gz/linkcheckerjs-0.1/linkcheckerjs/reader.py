#!/usr/bin/env python

from optparse import OptionParser

import json
from urlparse import urlparse
from collections import OrderedDict
from colorterm import formatter


ERROR = 0
WARNING = 1
INFO = 2
DEBUG = 3

LEVELS = [DEBUG, INFO, WARNING, ERROR]


COLORS = {
    DEBUG: 'green',
    INFO: 'blue',
    WARNING: 'yellow',
    ERROR: 'red',
}


def print_indent(s, indent_level, display_level=None):
    output = ''
    if indent_level:
        output += ' ' * (indent_level * 4)

    if display_level is not None:
        color = COLORS[display_level]
        output += formatter('{%(color)s}%(content)s{/%(color)s}' % {
            'color': color,
            'content': s
        })
    else:
        output += s
    return output


def print_title(title, s, *args, **kw):
    return print_indent('%s: %s' % (title.ljust(12), s),
                        *args, **kw)


class Element(object):

    def __init__(self, result):
        for k, v in result.iteritems():
            setattr(self, k, v)
        self.display_level = self._get_display_level()

    def _get_display_level(self):
        if self.status_code == 200:
            return DEBUG
        elif self.status_code == 301:
            return WARNING
        elif self.status_code == 302:
            return INFO
        return ERROR

    def check_display_level(self, level):
        if self.display_level <= level:
            return True
        return False

    def short_display(self, level, indent_level=0):
        s = []
        s.append(
            print_title('url', self.url, indent_level=indent_level))
        s.append(
            print_title('parent url', self.parent_url,
                        indent_level=indent_level))
        if self.redirect_url:
            s.append(
                print_title('redirect url', self.redirect_url,
                            indent_level=indent_level))
        s.append(
            print_title('status', '%s %s' % (self.status_code, self.status),
                        indent_level=indent_level,
                        display_level=self.display_level))
        return '\n'.join(s)

    def display(self, level, indent_level=0):
        return self.short_display(level=level, indent_level=indent_level)


class Resource(Element):

    def __init__(self, result):
        super(Resource, self).__init__(result)
        if self.url.startswith('data:'):
            # TODO: not the best place for this logic
            self.display_level = INFO
            self.status = 'Unable to parse data:'
        elif self.parent_url and urlparse(self.parent_url).scheme == 'https':
            if urlparse(self.url).scheme == 'http':
                self.display_level = ERROR


class Page(Element):

    def __init__(self, result, pages):
        # Set default in case page has been checked by requests
        self.resources = []
        self.urls = []
        super(Page, self).__init__(result)
        self.pages = pages
        self.resource_objs = []
        for res in self.resources:
            self.resource_objs.append(Resource(res))

    def display(self, level, indent_level=0):
        s = []
        resources = []
        for res in self.resource_objs:
            if res.check_display_level(level=level):
                resources.append(
                    res.display(level=level, indent_level=indent_level + 1))
        if resources:
            s.append(
                print_title('Resources', '', indent_level=indent_level,
                            display_level=None))
            s.append('\n\n'.join(resources))

        urls = []
        for url in self.urls:
            if self.pages.get(url) is None:
                # Be robust: it seems the process has been canceled
                continue

            if self.pages[url].check_display_level(level):
                urls.append(
                    self.pages[url].short_display(level,
                                                  indent_level=indent_level+1))
        if urls:
            s.append(
                print_title('Links', '', indent_level=indent_level,
                            display_level=None))
            s.append('\n\n'.join(urls))

        if s or self.check_display_level(level=level):
            return '\n'.join([super(Page, self).display(
                level=level, indent_level=indent_level)] + s)


def terminal_output(data, options_log_level):
    if options_log_level not in LEVELS:
        level = ERROR
    else:
        level = options_log_level

    pages = OrderedDict()
    for url, value in data.iteritems():
        if value is None:
            # Be robust: it seems the process has been canceled
            continue
        page = Page(value, pages)
        pages[url] = page

    for page in pages.itervalues():
        res = page.display(level=level)
        if res:
            print res
            print '---'
            print


def main():
    parser = OptionParser()
    parser.add_option("-l", "--log-level", type="int", dest="log_level",
                      help="linkcheckerjs log level")
    parser.add_option("-i", "--input", dest="filename",
                      help="Json file generated by linkcheckerjs",
                      metavar="FILE")
    (options, args) = parser.parse_args()

    if options.filename is None:
        raise Exception('Please provide a json file '
                        'generated by linkcheckerjs')

    data = json.load(open(options.filename),
                     object_pairs_hook=OrderedDict)
    terminal_output(data, level=options.log_level)


if __name__ == '__main__':
    main()
