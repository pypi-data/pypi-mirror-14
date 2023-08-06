#!/usr/bin/env python3.5
"""
    Easy-as-it-gets python3.5 library to search magnets
    in kickasstorrents (kat.cr)
"""
import random
from contextlib import suppress
from .. import File, Chapter
from pyquery import PyQuery as pq
from humanfriendly import parse_size
from torrentstream import _stream_torrent, Torrent
import aiohttp


class MagnetFile(File):
    """ MagnetFile class, implementing seeds-based score"""
    parent_score = 1
    search_type = "magnet"
    attributes = {}

    def __init__(self, chapter, link):
        self.chapter = chapter
        self.link = link

    @property
    def search_value(self):
        """ We'll use the link as value to send to pychapter """
        return self.link

    @property
    def local_score(self):
        seeds = 0
        with suppress(KeyError):
            seeds = self.attributes['seeds']

        if seeds > 1000:
            seeds_score = float(1000)

        seeds_score = seeds / 1000

        return seeds_score

    def get(self):
        """
            Get file, must return a tuple (filename, awaitable)
        """
        port1 = random.randrange(1024, 9000)
        filter_ = self.chapter.create_playable_filter()

        torrent = Torrent(self.link, {}, (port1, port1+1))
        return _stream_torrent(loop=self.chapter._loop,
                               torrent=torrent,
                               stream_func=lambda x, y: y,
                               filter_func=filter_)


async def search(query, page, loop):
    """ search magnets in kat.cr """
    with aiohttp.ClientSession(loop=loop) as session:
        url = 'https://kat.cr/usearch/{}/{}/'.format(query, page)
        async with session.get(url) as response:
            results = []
            if response.status != 200:
                return results
            content = await response.text()
            magnets = pq(content)('a[href^="magnet"]')
            for magnet in magnets:
                tr_ = magnet.getparent().getparent().getparent()
                magnetfile = MagnetFile(Chapter(filename=query, loop=loop),
                                        magnet.attrib['href'])
                magnetfile.attributes = {
                    'size': parse_size(tr_[1].text),
                    'files': int(tr_[2].text),
                    'age': tr_[3].text,
                    'seeds': int(tr_[4].text),
                    'leech': int(tr_[5].text)
                }
                results.append(magnetfile)
            return results
