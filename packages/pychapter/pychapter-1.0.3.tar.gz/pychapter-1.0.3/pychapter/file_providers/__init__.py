"""
    Providers.
"""
from importlib import import_module as import_
import asyncio
from .. conf import CONFIG

class File:
    """
        Represents a generic file provided by the file_providers.

        This means that:
            - Whoever handles a Chapter() instance must be responsible
            for managing "destionation" property
            - Search_type and Search_value must be implemented by the file
            provider itself, and must be parameters that allows a pychapter
            object to be compared (see ``pychapter.Chapter.__eq__``)
            - Link may be whatever is needed, and must be handled by the
            final user too
            - Each provider may implement a local score based on their data.
            - Each provider must provide a parent_score, otherwise it'll be 1

        .. param search_type:: Param name to pass to Chapter() constructor
            on comparishion
        .. param search_value:: search_type value
        .. param link:: Optional link to be filled by the provider
        .. param attributes:: Dictionary containing extra attributes
        .. param parent_score:: Main score provided by the provider

        Example::

            class MyFile(File):
                search_type = "magnet"
                def __init__(self, link):
                    self.link = link
                @property
                def search_value(self):
                    return self.link
                parent_score = 2

    """
    search_type = False
    search_value = False
    link = False
    destination = False
    attributes = {}
    parent_score = 1

    @property
    def local_score(self):
        """ Local file score """
        return 0

    @property
    def score(self):
        """
            We consider 1000 seeds the max value we actually need
            to have in account.
        """

        return self.parent_score + self.local_score

    def __repr__(self):
        return "<File object {}>".format(self.__dict__)

    def __getstate__(self):
        dict = self.__dict__
        dict.pop('chapter')
        return dict


async def search_files(query, pagelen=1, loop=False):
    """
        Search files amongst file providers
    """
    search_functions = [import_(mod).search for mod in
                        CONFIG['files_providers']]

    tasks = []
    for page in range(0, pagelen):
        for s_func in search_functions:
            tasks.append(asyncio.ensure_future(s_func(query, page + 1, loop)))

    flattened = []
    for provider in await asyncio.gather(*tasks):
        flattened.extend(provider)
    return flattened
