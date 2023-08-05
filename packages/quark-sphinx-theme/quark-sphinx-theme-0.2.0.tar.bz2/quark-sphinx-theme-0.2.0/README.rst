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
    # To enable more QTextBrowser-compatible HTML generation:
    extensions = ['quark_sphinx_theme.ext.html_compat']


Changelog
=========

* quark-sphinx-theme 0.2.0 *(2016-02-28)*

  - Add ``quark_sphinx_theme.ext.html_compat`` extension.
  - Add styling for citations, footnotes, table captions, and ``rubric`` directives.

* quark-sphinx-theme 0.1.2 *(2016-02-27)*

  - Fix compatibility with Jinja2 2.3.

* quark-sphinx-theme 0.1.1 *(2016-02-24)*

  - Fix spacing of navigation links.

* quark-sphinx-theme 0.1.0 *(2016-02-24)*

  - Initial release.
