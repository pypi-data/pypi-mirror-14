#!/usr/bin/env python3.5
"""
    Get info for a tv series from omdb
"""
from bs4 import BeautifulSoup
import asyncio
import aiohttp


async def search(series, season, episodenumber, loop):
    with aiohttp.ClientSession(loop=loop) as session:
        url = 'http://www.omdbapi.com/?type=series&t={}'.format(series)
        async with session.get(url) as response:
            if response.status != 200:
                return {}
            results = await response.json()
            return {
                'series_plot': results['Plot'],
                'series_genre': results['Genre'],
                'series_poster': results['Poster'],
            }
