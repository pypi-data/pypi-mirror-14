#!/usr/bin/env python3.5
import os
from json import load, JSONDecodeError
from contextlib import suppress

CONFIG = {
    'files_providers': ['pychapter.file_providers.kat'],
    'info_providers': ['pychapter.info_providers.omdb',
                       'pychapter.info_providers.thetvdb'],
    'subs_providers': ['pychapter.subs_providers.addic7ed']
}
with suppress(JSONDecodeError, FileNotFoundError):
    CONFIG.update(load(open(os.path.expanduser('~/pychapter.conf'))))
