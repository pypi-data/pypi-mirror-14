#! /usr/bin/env python
# Copyright (C) 2016 Alain Leufroy
#
# Author: Alain Leufroy <alain@leufroy.fr>
# Licence: WTFPL, grab your copy here: http://sam.zoy.org/wtfpl/
"""The lairucrem librairy."""


from __future__ import unicode_literals, absolute_import

import imp

import sh

from urwid.main_loop import MainLoop
if getattr(MainLoop, 'start', None) is None:
    from . import patch_urwid

from . import patch_sh # apply needed patch


def get_extension_path():
    """Search for lairucrem mercurial extension file path and return it.

    The extension file is not loaded so, lazy import feature of
    mercurial is not activated.
    """
    fid, path = imp.find_module('extension', __path__)[:2]
    fid.close()
    return path


def repository(rootpath=None):
    """Return an sh.Command object that can talk to a mercurial repository.

    >>> repo = repository()
    >>> result = repo.help().__unicode__()

    """
    repo = sh.hg.bake(
        _env={'HGPLAIN': '1'},
        _tty_in=False, _tty_out=False,
        _internal_bufsize=1000,
    )
    if rootpath:
        return repo.bake(_cwd=rootpath)
    else:
        return repo


def sh2cmd(repo):
    """convert a sh.Command into a Popen args."""
    return [repo._path] + repo._partial_baked_args  # pylint: disable=protected-access
