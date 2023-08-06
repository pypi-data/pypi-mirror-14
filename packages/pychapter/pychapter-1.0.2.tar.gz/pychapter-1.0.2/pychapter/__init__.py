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
from . decorators import series_info, cached
from . file_providers import search_files
from . subs_providers import search_subs

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

__author__ = 'David Francos'
__email__ = 'me@davidfrancos.net'
__version__ = '0.1.0'


class Sub:
    """
        Represents a generic subtitle.
    """
    language = False
    season = False
    episode = False
    series = False

    def score(self):
        if self.language == "en":
            return 100
        else:
            return 0


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
        return 0

    @property
    def score(self):
        """
            We consider 1000 seeds the max value we actually need
            to have in account.
        """

        return self.parent_score + self.local_score


class Chapter:
    """ Represents a specific chapter """
    _episode = False
    _title = False
    _episode_title = False
    _filename = False
    _season = False
    _magnet = False
    _files = False
    _subtitles = False
    _sorting_method = False
    _sub_sorting_method = False
    _video_info = False
    _loop = False

    def __init__(self, **kwargs):
        """
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
                        dest = os.path.expanduser('~/{}'.format(
                            chapter.filename))
                        await chapter.file.get(dest) #: This can be async =)
                        chapter.file.destination = dest
        """

        self._sorting_method = lambda x: x.score
        self._sub_sorting_method = lambda x: x.score
        for arg, value in kwargs.items():
            setattr(self, "_{}".format(arg), value)

    def resolve_all(self):
        """
            Load one of each kind of providers (series info, files and subs)
            This is just for its side effects, we get and cache them.
            This way we can keep lazy load while implementing a full save
            method with all the info.
        """
        LOG.debug(self.file)
        LOG.debug(self.plot)
        LOG.debug(self.subtitle)

    def path(self, directory):
        """
            Returns formatted save/load path
            See `ref:save`
        """

        with suppress(OSError):
            os.makedirs(directory)

        title = ''.join(a for a in str(self.title.lower())
                        if a in ascii_lowercase)
        return os.path.join(directory, title, str(self.season))

    def internal_file(self, directory, extension):
        """
            Get load/save file
        """
        path = self.path(directory)
        return os.path.join(path, '{}.{}'.format(self.episode, extension))

    def read(self, directory):
        """
            Returns a chapter object read from a pickle.
            With this, we can do::

                Chapter(season=1, episode=1, title="MySeries").save('.')
                print("Got: {} ".format(chapter.magnet)

                chapter = Chapter(season=1, episode=1,
                                  title="MySeries").load('.')
                print(chapter.magnet)

            This way, the magnet link will only be looked for once, as
            the second time it'll be read from the pickle and then cached.

            Remember that this library lazy-loads the info, so, if you want
            to save a fully-retrieved chapter you'll need to force it like::

                chapter = Chapter(season=1, episode=1,
                                  title="MySeries")
                chapter.resolve_all()
                chapter.save('.')

                chapter = Chapter(season=1, episode=1,
                                  title="MySeries").load('.')
                print(chapter.magnet)
        """
        return pickle.load(open(self.internal_file(directory, 'pickle'), 'rb'))

    def save(self, directory):
        """
            Save this in the specified directory
            using the following format::

                {series_name}/{season}/{chapter}.pickle
                {series_name}/{season}/{chapter}.srtm

            With the pickled object and the magnet in a srtm file wich
            is playable in some platforms
        """

        path = self.path(directory)
        os.makedirs(path, exist_ok=True)

        # with open(self.internal_file(directory, 'pickle'), 'wb') as file_:
            # pickle.dump(self, file_)

    @property
    @cached
    def video_info(self):
        """ Guessed video info """
        if not self._video_info:
            self._video_info = guessit(self.filename)
        return self._video_info

    @property
    @cached
    def episode(self):
        """ Episode number, mandatory if no magnet specified """
        return self.video_info['episode']

    @property
    @cached
    def title(self):
        """ TV Series title """
        return self.video_info['title']

    @property
    @cached
    def season(self):
        """ season, mandatory if no magnet specified """
        return self.video_info['season']

    @property
    @series_info
    def plot(self):
        """ Chapter plot """
        return ['chapter_plot']

    @property
    @cached
    def episode_title(self):
        """ title, mandatory if no magnet specified """
        return self.get_info_from_chapter('episode_title')

    def get_info_from_chapter(self, what):
        """
            Extracts, from all providers available, a specific data
        """
        for providers in self.series_chapters:
            for chapter in providers:
                chapter['loop'] = self._loop
                chapter = Chapter(**chapter)
                if chapter == self:
                    return getattr(chapter, what)

    @property
    @series_info
    def series_chapters(self):
        """ All the chapters from this series """
        return ['series_chapters']

    @property
    @series_info
    def poster(self):
        """ poster """
        return ['series_poster']

    @property
    def next(self):
        """
            Returns a chapter object for the next episode
            We need data providers for specific
            episodes in order to this to properly work.

            .. warning:: Not currently handling season length.
        """
        return Chapter(title=self.title, loop=self._loop, season=self.season,
                       episode=int(self.episode)+1)

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

        if self._magnet:
            query = urlparse(self._magnet).query
            with suppress(KeyError):
                return parse_qs(query)['dn'][0]

        if all([self._title, self._season, self._episode]):
            return "{} s{:02}e{:02}".format(
                self._title, int(self._season), int(self._episode))

        if self._title and self._title:
            return "{} {}".format(self.title, self.title)

        raise Exception("Not enough data provided")

    @property
    async def file(self):
        """
            Returns the closest match from self.files

            This is actually performed using a sorting method defined
            in self._sorting_method, that you can override passing
            sorting_method=your_custom_method to this class.

            Note that this is done AFTER prioritizing by file provider
            score.

        """
        with suppress(KeyError):
            return sorted(await self.files, key=self._sorting_method)[-1]

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
            if Chapter(**{"loop": self._loop, file.search_type: file.search_value}) == self:
                results.append(file)

        return results

    @property
    async def subtitle(self):
        """
            Returns the first subtitle
        """
        with suppress(KeyError):
            return sorted(await self.subs, key=self._sub_sorting_method)[-1]

    @property
    async def subs(self):
        """ Returns a subtitles list """
        if not self._subtitles:
            self._subtitles = await search_subs(self)
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

    def __enter__(self):
        cache = False
        with suppress(OSError):
            cache = self.read(os.path.expanduser('~/.pychapter_cache'))
        if cache:
            return cache
        else:
            return self

    def __exit__(self, excpt_type, excpt_value, traceback):
        if excpt_type:
            raise excpt_type("Exception happened inside context "
                             "manager, refusing to save")
        self.save(os.path.expanduser('~/.pychapter_cache'))


class Season:
    """
        Represents a season
        .. param number:: Season number
        .. param chapters:: Chapter objects or dicts representing the chapters
    """
    def __init__(self, number, chapters):
        self._chapters = chapters
        self.number = number

    @property
    def chapters(self):
        """ Chapters """
        for chapter in self._chapters:
            if not isinstance(chapter, Chapter):
                if not isinstance(chapter, dict):
                    raise ValueError("Chapter must be either a dict compatible"
                                     "with a `Chapter` object or a `Chapter`")
                chapter['loop'] = self._loop
                yield Chapter(**chapter)
            else:
                yield chapter

    @property
    @series_info
    def poster(self):
        """ poster """
        return ['series_poster']


class Series:
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

    @property
    def title(self):
        """ Title """
        return self._title

    @property
    @series_info
    def poster(self):
        """ poster """
        return ['series_poster']

    @property
    @series_info
    def plot(self):
        """ Plot """
        return ['series_plot']

    @property
    @series_info
    def genre(self):
        """ genre """
        return ['series_genre']

    @property
    @series_info
    def _raw_chapters(self):
        """ This is just to be later used by chapters."""
        return ['series_chapters']

    @property
    def chapters(self):
        """ Returns a Chapter object for each chapter in this series"""
        for provider in self._raw_chapters:
            for chapter in provider:
                chapter['loop'] = self._loop
                yield Chapter(**chapter)

    def save(self, directory):
        """ Save """
        for chapter in self.chapters:
            chapter.resolve_all()
            chapter.save(directory)

    @property
    def seasons(self):
        """ Return seasons given a set of chapters """
        seasons = defaultdict(list)
        for chapter in self.chapters:
            seasons[chapter.season].append(chapter)
        for id_, chapters in seasons.items():
            yield Season(chapters=chapters, number=id_)
