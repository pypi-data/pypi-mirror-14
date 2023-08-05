# silex
![Build](https://travis-ci.org/walidsa3d/silex.svg?branch=master)
![downloads](https://img.shields.io/pypi/dm/silex.svg)
![license](https://img.shields.io/pypi/l/silex.svg)
![version](https://img.shields.io/pypi/v/silex.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

A bunch of useful functions for string manipulation.

## Install (automatic)
```
$ pip install silex
```
## Install (manual)
```
$ git clone 
$ cd silex
$ python setup.py install
```
## Usage
```python
In [1]: from silex import *

In [2]: print chop("whitespace", 5)
['white', 'space', '']

In [3]: print numberex('1.2euros')
1.2

In [4]: print surround('b', '<', '>')
<b>

In [5]: print strip_html('<p><i>hello</i></p>')
hello

In [6]: print unslugify('sex_appeal')
sex appeal

In [7]: print slugify(u'je suis\ épuisé')
je-suis-epuise

In [8]: print clean('hello\n    word\n')
hello word

In [9]: print kebabcase('hello  world')
hello-world

In [10]: print pascalcase('hello world')
HelloWorld

In [11]: print camelcase('hello world')
helloWorld

In [12]: print snakecase('hello world')
hello_world
```

## License
MIT