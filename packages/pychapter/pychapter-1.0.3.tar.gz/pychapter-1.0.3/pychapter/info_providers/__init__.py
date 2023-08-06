"""
    External data providers.
"""
import asyncio
from importlib import import_module as import_
from .. conf import CONFIG

SEARCH_F = [import_(mod).search for mod in CONFIG['info_providers']]


async def search_info(series, season, episodenumber, loop):
    """
        Search info amongst various providers.
        Right now, first found is returned for everything
        .. TODO:: Make this sortable somehow.
    """
    tasks = []

    for s_func in SEARCH_F:
        tasks.append(asyncio.ensure_future(s_func(series, season,
                                                  episodenumber, loop)))

    flattened = {}
    for provider in await asyncio.gather(*tasks):
        flattened.update(provider)
    return flattened
