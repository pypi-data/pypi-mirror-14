#!/usr/bin/env python
# -*- coding: utf-8 -*-
from silex import *


print chop("whitespace", 5)
print numberex('1.2euros')
print surround('b', '<', '>')
print strip_html('<p><i>hello</i></p>')
print unslugify('sex_appeal')
print slugify(u'je suis\ épuisé')
print clean('hello\n    word\n')
print kebabcase('hello  world')
print pascalcase('hello world')
print camelcase('hello world')
print snakecase('hello world')
