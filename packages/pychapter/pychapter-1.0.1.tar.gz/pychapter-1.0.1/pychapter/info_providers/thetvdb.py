#!/usr/bin/env python3.5
"""
    Get info for a tv series from thetvdb
"""
from bs4 import BeautifulSoup
import asyncio
import xmltodict
import aiohttp
import asyncio
import zipfile
from io import BytesIO


def episodes(series_data):
    for episode in series_data['Episode']:
        yield {
            'episode': int(float(episode['Combined_episodenumber'])),
            'plot': episode['Overview'],
            'season': episode['SeasonNumber'],
            'episode_title': episode['EpisodeName'],
            'title': series_data['Series']['SeriesName']
        }


async def search(series, season, episodenumber, loop):
    with aiohttp.ClientSession(loop=loop) as session:
        url = "http://thetvdb.com/api/GetSeries.php?seriesname={}".format(
            series)

        async with session.get(url) as response:
            if response.status != 200:
                return {}
            results = await response.text()
            results = xmltodict.parse(results)['Data']['Series']
            if isinstance(results, list):
                results = results[0]
            url_zip = ("http://thetvdb.com/api/8F096C5F8"
                       "58EDDD2/series/{}/all/en.zip".format(results['id']))
            async with session.get(url_zip) as response_zip:
                zip_ = BytesIO(await response_zip.read())
                zip = zipfile.ZipFile(zip_)
                series_data = xmltodict.parse(zip.read('en.xml'))['Data']

                return {
                    'series_plot': series_data['Series']['Overview'],
                    'series_poster': series_data['Series']['banner'],
                    'series_chapters': list(episodes(series_data))
                }
