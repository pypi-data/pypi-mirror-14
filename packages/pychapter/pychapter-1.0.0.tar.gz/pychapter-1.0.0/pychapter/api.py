"""
    PyChapter basic API
"""
from contextlib import suppress
import logging
import asyncio
import pathlib
import aiohttp
import aiohttp.web
from pychapter import Chapter

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class PyChapterAPI(aiohttp.web.View):
    """ Main API """

    @property
    def chapter(self):
        """ Get chapter from match_info"""
        magnet = False
        with suppress(KeyError):
            magnet = self.request.match_info['magnet']

        if not magnet:
            title = self.request.match_info['series']
            season = self.request.match_info['season']
            episode = self.request.match_info['chapter']
            chapter = Chapter(title=title, episode=episode,
                              season=season, loop=self.request.app._loop)
        else:
            chapter = Chapter(magnet=magnet, loop=self.request.app._loop)

        if chapter.filename in self.request.app:
            raise aiohttp.web.HTTPFound(
                self.request.app[chapter.filename]['url'])

        return chapter

    async def get(self):
        """ Get a chapter stream. Will redirect once chapter is ready """
        chapter = self.chapter
        with chapter as chapter_:
            file_ = await chapter_.file
            LOG.info("Got file:  {}".format(file_))
            awaitable, file = await file_.get()
            file_url = "http://localhost:8080/streams/{}".format(file.path)
            self.request.app[chapter_.filename] = {
                'cancelable': asyncio.ensure_future(awaitable),
                'url': file_url
            }
            chapter_.destination = file.path
        raise aiohttp.web.HTTPFound(file_url)

    async def delete(self):
        """ Cancels the torrent download """
        chapter = self.chapter
        if chapter.filename in self.request.app:
            self.request.app[chapter.filename]['cancelable'].cancel()
            return aiohttp.web.Response(text="OK")

        raise aiohttp.web.HTTPNotFound()


def server():
    """ Main server """
    app = aiohttp.web.Application()
    app.router.add_route('*', '/get/{series}/{season}/{chapter}', PyChapterAPI)
    app.router.add_route('*', '/get/{magnet}', PyChapterAPI)
    app.router.add_static("/streams/", pathlib.Path('.').absolute())
    aiohttp.web.run_app(app)


if __name__ == "__main__":
    server()
