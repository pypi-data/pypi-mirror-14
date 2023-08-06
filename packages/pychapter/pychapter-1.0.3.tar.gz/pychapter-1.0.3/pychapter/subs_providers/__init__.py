"""
    External subs providers.
"""
import asyncio
from importlib import import_module as import_
from .. conf import CONFIG

SEARCH_F = [import_(mod).search for mod in CONFIG['subs_providers']]


async def search_subs(query, loop):
    """ Search subs"""
    tasks = []

    for s_func in SEARCH_F:
        tasks.append(asyncio.ensure_future(s_func(query, loop)))

    flattened = []
    for provider in await asyncio.gather(*tasks):
        flattened.extend(provider)

    return flattened
