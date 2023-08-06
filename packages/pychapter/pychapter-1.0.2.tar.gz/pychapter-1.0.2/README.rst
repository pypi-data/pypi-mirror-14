===============================
pychapter
===============================

Pychapter is a simple library written in python3.5 that handles tv series data.
That is, given a set of data, it tries to gather as much data as possible from
its providers.

There are three kinds of providers:

- Data providers, for tv show information
- Magnet providers, for magnet links
- Subtitles providers, for subitles


Examples::

    chapter = Chapter(title='limitless', season=1, chapter=1)
    chapter.magnet # This will return the closest magnet with most seeds
    chapter.plot # Chapter plot

    # This will print a magnet link for each chapter in the whole series
    for season in Series(title="limitless"):
        for chapter in season.chapters:
            print(chapter.magnet)


.. image:: https://img.shields.io/pypi/v/pychapter.svg
        :target: https://pypi.python.org/pypi/pychapter

.. image:: https://img.shields.io/travis/XayOn/pychapter.svg
        :target: https://travis-ci.org/XayOn/pychapter

.. image:: https://readthedocs.org/projects/pychapter/badge/?version=latest
        :target: https://readthedocs.org/projects/pychapter/?badge=latest
        :alt: Documentation Status


TV Series management tool

* Free software: ISC license
* Documentation: https://pychapter.readthedocs.org.

Features
--------

* Series object
* Season object
* Chapter object

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
