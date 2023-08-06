"""
    Providers.
"""
from importlib import import_module as import_
import asyncio
from .. conf import CONFIG


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
