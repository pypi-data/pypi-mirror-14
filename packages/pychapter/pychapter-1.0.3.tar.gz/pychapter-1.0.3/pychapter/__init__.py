#!/usr/bin/env python3
"""
    PyChapter
    ---------
"""
import mimetypes
from string import ascii_lowercase
import logging
import os
from collections import defaultdict
from urllib.parse import urlparse, parse_qs
from contextlib import suppress
import dill as pickle
from guessit import guessit
from . info_providers import search_info
from . decorators import cached
from . file_providers import search_files
from . subs_providers import search_subs

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

__author__ = 'David Francos'
__email__ = 'me@davidfrancos.net'
__version__ = '0.1.11'


class Chapter:
    """
        Represents a specific chapter

        .. param episode :: Number of the episode in the season
        .. param season :: Number of season
        .. param title :: Series name
        .. param episode_title :: Title of the chapter
        .. param magnet :: Magnet file

        If episode, season and series are specified, those will be
        used to get the magnet and no search will be performed.

        If only series and title are specified, a search on the providers
        will be performed to get the magnet, and from there, the rest of
        the data

        If only the magnet is specified, again, a search on the providers
        will return the rest.

        Example use::

            from pychapter import Chapter
            import os

            async def get_chapter():
                with Chapter(title="foo", episode=1, season=1) as chapter:
                    await chapter.file.get()
    """

    _title = False
    _season = False
    _episode = False

    _episode_title = False
    _filename = False

    _file = False
    _files = False

    _subtitle = False
    _subtitles = False

    _video_info = False
    _info = False

    _loop = False

    _files_sorting_method = False
    _subs_sorting_method = False

    def __init__(self, **kwargs):
        """
        """

        self._files_sorting_method = lambda x: x.score
        self._subs_sorting_method = lambda x: x.score
        for arg, value in kwargs.items():
            setattr(self, "_{}".format(arg), value)

    @property
    def filename(self):
        """
            If we've got series, season and episodenumber
            compose a filename.
            If we've got a magnet, get the filename from it.
            Otherwise, we don't do any magic here, just raise an exception.
        """
        if self._filename:
            return self._filename

        if self._file:
            try:
                query = urlparse(self._file['link']).query
            except (KeyError, TypeError):
                query = urlparse(self._file).query
            with suppress(KeyError):
                return parse_qs(query)['dn'][0]

        if all([self._title, self._season, self._episode]):
            return "{} s{:02}e{:02}".format(
                self._title, int(self._season), int(self._episode))

        raise Exception("Not enough data provided")

    def internal_file(self, directory, extension):
        """
            Get load/save file
        """

        os.makedirs(directory, exist_ok=True)

        title = ''.join(a for a in str(self.title.lower())
                        if a in ascii_lowercase)
        path = os.path.join(directory, title, str(self.season))
        return os.path.join(path, '{}.{}'.format(self.episode, extension))

    def read(self, directory):
        """
            Returns a chapter object read from a pickle.

            Remember that this library lazy-loads the info, so, if you want
            to save a fully-retrieved chapter you'll need to force it like::

                chapter = Chapter(season=1, episode=1,
                                  title="MySeries")
                chapter.__dict__()
                chapter.save('.')

            .. TODO:: Make __dict__ save only what we want.
        """
        return Chapter(**pickle.load(open(self.internal_file(
            directory, 'pickle'), 'rb')))

    async def save(self, directory):
        """
            Save this in the specified directory
            using the following format::

                {series_name}/{season}/{chapter}.pickle
                {series_name}/{season}/{chapter}.srtm

            With the pickled object and the magnet in a srtm file wich
            is playable in some platforms
        """

        with open(self.internal_file(directory, 'dict'), 'wb') as file_:
            dict = await self.__dict__
            print(dict)
            pickle.dump(dict, file_)

    @property
    @cached
    def video_info(self):
        """ Guessed video info """
        if not self._video_info:
            self._video_info = guessit(self.filename)
        return self._video_info

    @property
    def episode(self):
        """ Episode number, mandatory if no magnet specified """
        return self.video_info['episode']

    @property
    def title(self):
        """ TV Series title """
        return self.video_info['title']

    @property
    def season(self):
        """ season, mandatory if no magnet specified """
        return self.video_info['season']

    @property
    async def episode_title(self):
        """ Episode title """
        for chapter in self.series_chapters:
            if chapter == self:
                return chapter.episode_title

    @property
    async def series_chapters(self):
        """
            All the chapters from this series
            This actually returns Chapter objects, so we
            can retrieve a complete tv series from here.
        """
        await self.info
        chapters = self._info['series_chapters']
        result = []
        for chapter in chapters:
            result.append(Chapter(loop=self._loop, **chapter))
        return result

    @property
    async def poster(self):
        """ poster """
        await self.info
        return self._info['series_poster']

    @property
    async def plot(self):
        """ plot """
        await self.info
        return self._info['series_plot']

    @property
    async def next(self):
        """
            Returns a chapter object for the next episode
            We need data providers for specific
            episodes in order to this to properly work.
        """
        nex_ = Chapter(title=self.title, loop=self._loop, season=self.season,
                       episode=int(self.episode)+1)
        if nex_ in await self.series_chapters:
            return nex_

    @property
    async def file(self):
        """
            Returns the closest match from self.files
        """
        with suppress(KeyError):
            return sorted(await self.files, key=self._files_sorting_method)[-1]

    @property
    async def files(self):
        """
            This searches in all magnet providers, and then returns those that
            are from this same chapter.
        """
        if not self._files:
            self._files = await search_files(self.filename,
                                             loop=self._loop)

        results = []
        for file in self._files:
            if Chapter(**{"loop": self._loop,
                          file.search_type: file.search_value}) == self:
                results.append(file)

        return results

    @property
    async def info(self):
        """
            This searches in all magnet providers, and then returns those that
            are from this same chapter.
        """
        if not self._info:
            self._info = await search_info(self.title, self.season,
                                           self.episode, loop=self._loop)
        return self._info

    @property
    async def subtitle(self):
        """
            Returns the closes match to the best subtitle
        """
        with suppress(KeyError):
            return sorted(await self.subs, key=self._subs_sorting_method)[-1]

    @property
    async def subs(self):
        """ Returns a subtitles list """
        if not self._subtitles:
            self._subtitles = await search_subs(self, loop=self._loop)
        return self._subtitles

    def create_playable_filter(self):
        """
            Filter files for a chapter.
            As a side-effect this donwloads the subtitles if they're not
            already present.
            .. return :: Coroutine
        """
        async def filter_(files):
            """
                Gets a list of files and returns the first one matching
                the chapter
            """
            reserved_ = ['sample']
            for file in files:

                if any([res in file.path.lower() for res in reserved_]):
                    continue

                if Chapter(filename=file.path, loop=self._loop) == self:
                    if 'video' in mimetypes.guess_type(file.path)[0]:
                        with suppress(OSError):
                            os.makedirs(os.path.dirname(file.path))
                        spath = '.'.join(file.path.split('.')[:-1])
                        if not os.path.exists("{}.srt".format(spath)):
                            with open("{}.srt".format(spath), 'wb') as subs:
                                sub = await self.subtitle
                                subs.write(sub.file)
                        return file

        return filter_

    def __repr__(self):
        return "<Chapter object ({})>".format(self.filename)

    def __eq__(self, other):
        conds = [self.title.lower().strip() == other.title.lower().strip(),
                 int(self.episode) == int(other.episode),
                 int(self.season) == int(other.season)]
        return all(conds)

    async def __aenter__(self):
        cache_ = self
        with suppress(OSError):
            cache_ = self.read(os.path.expanduser('~/.pychapter_cache'))
        return cache_

    async def __aexit__(self, excpt_type, excpt_value, traceback):
        if excpt_type:
            raise excpt_type("Exception happened inside context "
                             "manager, refusing to save")
        return await self.save(os.path.expanduser('~/.pychapter_cache'))

    @property
    async def __dict__(self):
        return {
            '_files': self._files,
            '_video_file': self._video_info,
            '_subtitles': self._subtitles
        }


class Season:
    """
        Represents a season
        .. param season:: Season number
        .. param title :: TV Series title
        .. param chapters:: Chapters as chapter objects.

        If chapters is specified, season and title will be ignored
    """
    _chapters = False

    def __init__(self, season=False, title=False, chapters=False):
        if chapters:
            self.chapter = chapters[0]
            self._chapters = chapters
            self._season = self.chapter.season
        else:
            self.chapter = Chapter(season=season, title=title, episode=1)
            self.season = season

    @property
    async def title(self):
        """ Title """
        return self._title

    @property
    async def poster(self):
        """ poster """
        return await self.chapter.poster

    @property
    async def plot(self):
        """ Plot """
        return await self.chapter.plot

    @property
    async def chapters(self):
        """ Chapters """
        if self._chapters:
            return self._chapters

        chapters = []
        for chapter in await self.chapter.series_chapters:
            if chapter.season == self.season:
                chapters.append(chapter)
        return sorted(chapters, key=lambda x: x.episode)


class Series(Season):
    """
        Represent a whole tv series, just specify

        .. param title:: [Required] Series title
    """
    season = False
    episode = False
    _title = False

    def __init__(self, **kwargs):
        for arg, value in kwargs.items():
            setattr(self, "_{}".format(arg), value)
        self.chapter = Chapter(title=self._title, season=1, episode=1)

    @property
    async def chapters(self):
        return await self.chapter.series_chapters

    def save(self, directory):
        """ Save """
        for chapter in self.chapters:
            chapter.save(directory)

    @property
    def seasons(self):
        """ Return seasons given a set of chapters """
        seasons = defaultdict(list)
        for chapter in self.chapters:
            seasons[chapter.season].append(chapter)
        for id_, chapters in seasons.items():
            yield Season(chapters=chapters, season=id_)
