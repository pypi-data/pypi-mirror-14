#!/usr/bin/env python3.5
"""
    Addic7ed subtitles
"""
from addic7ed_cli.episode import search as search_episode
from addic7ed_cli.util import file_to_query
from tempfile import NamedTemporaryFile


class Addict7edSubtitle:
    """ Addict7d.com subtitles """
    _file = False

    def __init__(self, chapter, sub):
        self.sub = sub
        self.chapter = chapter
        self.language = self.sub.language
        self.release = self.sub.release
        self.completeness = self.sub.completeness

    @property
    def file(self):
        """ Get the sub content """
        if not self._file:
            with NamedTemporaryFile() as file_:
                self.sub.download(file_.name)
                file_.seek(0)
                self._file = file_.read()
        return self._file

    @property
    def score(self):
        """ Completeness is the direct score here """
        if self.completeness == "Completed":
            return 100
        else:
            return 99


async def search(chapter, loop):
    """ Search subs """
    subs = search_episode(file_to_query(chapter.filename)[0])[0]
    subs.fetch_versions()

    return [Addict7edSubtitle(chapter, sub) for sub in
            subs.filter_versions(languages=['En'])]
