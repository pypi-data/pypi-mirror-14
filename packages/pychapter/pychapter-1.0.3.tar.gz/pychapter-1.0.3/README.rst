PyChapter
=========


PyChapter is a python3.5 series management tool.
PyChapter is asynchronous, beware of coroutines!

Using various data providers for each kind of data needed, we gather as many
information as we can to provide.

.. image:: https://img.shields.io/pypi/v/pychapter.svg
        :target: https://pypi.python.org/pypi/pychapter

.. image:: https://img.shields.io/travis/XayOn/pychapter.svg
        :target: https://travis-ci.org/XayOn/pychapter

.. image:: https://readthedocs.org/projects/pychapter/badge/?version=latest
        :target: https://readthedocs.org/projects/pychapter/?badge=latest
        :alt: Documentation Status


* Free software: ISC license
* Documentation: https://pychapter.readthedocs.org.


PyChapter providers
-------------------

There are currently 3 types of data providers:

* File providers
* Info providers
* Subs providers


File providers
++++++++++++++

File providers allow us to actually GET the chapter. 
Currently, only kat.cr + torrent management is implemented


Subs providers
++++++++++++++

Subs providers allow us to get subtitles for a chapter
At this point, subtitles are forced to english and only addict7ed
is supported


Info providers
++++++++++++++

Get all kind of data related to a specific chapter (plot, title, cover,
series plot, series seasons...)


API
---

PyChapter provides a simple endpoint as kind-of an example use.
It's installed with the package as an entry_point with the name "pychapter",
so you can just run "pychapter" and it'll launch the sample API running
on localhost:8080.

TODO: Link API docs here from api.py


Complete series management
--------------------------

This is a simple example of the usage of "Series" object to get
an entire series' main file objects.

::

    async def get_magnets(serie_name):
        for season in Series(title=serie_name):
            for chapter in season.chapters:
                print(await chapter.file)


Features
--------

* Simple REST API 
* Easily extensible
* Subtitles, Files and Info management 

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
