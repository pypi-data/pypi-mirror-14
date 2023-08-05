========================================
Quark: a Sphinx theme for QTextBrowser
========================================

About
=====

Quark is a Sphinx theme specifically designed to look and work well within the
limitations of the Qt toolkit's ``QTextBrowser``.

This theme was originally designed for the bundled manual of `SpeedCrunch`_.

.. _SpeedCrunch: http://speedcrunch.org


Installation
============

* ``pip install quark-sphinx-theme``
* In your ``conf.py``::

    import quark_sphinx_theme
    html_theme_path = [quark_sphinx_theme.get_path()]
    html_theme = 'quark'


Changelog
=========

* quark-sphinx-theme 0.1.2 *(2016-02-27)*

  - Fix compatibility with Jinja2 2.3.

* quark-sphinx-theme 0.1.1 *(2016-02-24)*

  - Fix spacing of navigation links.

* quark-sphinx-theme 0.1.0 *(2016-02-24)*

  - Initial release.


License
=======

The Quark theme is released under the terms of the MIT license, as reproduced
below:

Copyright (c) 2016 Felix Krull <f_krull@gmx.de>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
