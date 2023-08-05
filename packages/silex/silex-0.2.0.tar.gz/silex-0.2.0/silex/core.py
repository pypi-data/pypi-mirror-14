#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import unicodedata


def strip_html(stringvar):
    ''' remove html tags from string '''
    return re.sub(r'<[^<]+?>', '', stringvar)


def unslugify(stringvar):
    return re.sub(r'-|_', ' ', stringvar)


def slugify(stringvar):
    if isinstance(stringvar, str):
        stringvar = stringvar.decode('utf-8')
    slug = unicodedata.normalize('NFKD', stringvar)
    slug = slug.encode('ascii', 'ignore')
    slug = slug.strip()
    slug = slug.lower()
    slug = unicode(slug)
    slug = re.sub(r'[^\w\s-]', '', slug)
    l = re.sub(r' ', '-', slug)
    return l


def chop(stringvar, step):
    ''' equal-sized chunks '''
    l = []
    i = 0
    while i <= len(stringvar):
        l.append(stringvar[i:i+step])
        i = i+step
    return l


def numberex(stringvar):
    ''' extract numbers from string '''
    s = re.search('\d+(\.\d*)?', stringvar)
    if s:
        return s.group()
    return


def surround(stringvar, prefix, suffix):
    return ''.join([prefix, stringvar, suffix])


def clean(stringvar):
    ''' squeeze multiple spaces and trim '''
    s = re.sub('\s+', ' ', stringvar)
    return s.strip()


def kebabcase(stringvar):
    ''' hello world --> hello-world'''
    s = stringvar.lower().split()
    return '-'.join(s)


def pascalcase(stringvar):
    ''' hello world --> HelloWorld'''
    s = [word.title() for word in stringvar.split()]
    return ''.join(s)


def camelcase(stringvar):
    ''' hello world --> helloWorld'''
    s = stringvar.split()
    s1 = [word.title() for word in s[1:]]
    s2 = [s[0].lower()]+s1
    return ''.join(s2)


def snakecase(stringvar):
    ''' hello world --> hello_world'''
    s = stringvar.lower().split()
    return '_'.join(s)
