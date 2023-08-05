#! /usr/bin/env python
# coding: utf-8
# Copyright (C) 2016 Alain Leufroy
#
# Author: Alain Leufroy <alain@leufroy.fr>
# Licence: WTFPL, grab your copy here: http://sam.zoy.org/wtfpl/
"""Commands that can be processed depending on a given changeset."""


from subprocess import call
from . import sh2cmd


cmd_registry = []

# registry can be changed for test purpose
# pylint: disable=dangerous-default-value
def get_valid_actions(repo, cset, registry=cmd_registry):
    """Return the list of actions that can be applied to the given changeset"""
    cache = {}
    iter_actions = ((name, func(repo, cset, cache)) for func, name in registry)
    return ((choice, cmd) for choice, cmd in iter_actions if next(cmd))


# registry can be changed for test purpose
# pylint: disable=dangerous-default-value
def cmd(name=None, replace=None, _registry=cmd_registry):
    """Decorator that registers a command function.

    :name: name displayed in the choice menu
           or the decorated function name if not given.

    :replace: (func, name), if given, is replaced by the current one.
    """
    def wrapper(func=None):
        """wrapper that register the command"""
        _name = name or func.__name__
        if replace and replace in _registry:
            _registry[_registry.index(replace)] = (func, _name)
        else:
            _registry.append((func, _name))
        return func
    return wrapper

# commands
# ########

@cmd(name='Commit: commit all outstanding changes')
def commit(repo, cset, _cache):
    """Commit all outstanding changes

    Commit changes to the given files into the repository using the interactive mode.
    Add '[experimental] crecord=true' in the HGRC for a curses base interface.
    """
    yield not cset and not is_clean(repo, cset, _cache)
    call(sh2cmd(repo.commit.bake(
        interactive=True, edit=True, config="experimental.crecord=true")))

@cmd(name='Amend: amend the parent of the working directory')
def amend(repo, cset, _cache):
    """Amend the parent of the working directory

    with new commit that contains the changes in the parent in
    addition to those currently outstanding.

    Add '[experimental] crecord=true' in the HGRC for a curses base
    interface.
    """
    yield not cset and not is_clean(repo, cset, _cache)
    call(sh2cmd(repo.commit.bake(
        interactive=True, amend=True, edit=True, config="experimental.crecord=true")))

@cmd(name='addremove: add all new files, delete all missing files')
def addremove(repo, cset, _cache):
    """add all new files, delete all missing files.
    """
    summary = get_summary(repo, cset, _cache)['commit']
    yield not cset and ('unknown' in summary or 'deleted' in summary)
    call(sh2cmd(repo.addremove))

@cmd(name='Shelve: save and set aside changes from the working directory')
def shelve(repo, cset, _cache):
    """Save and set aside changes from the working directory.

    Shelvinf takes files from the durty working directory, saves the
    modifications to a bundle and reverts files so that their state in
    the working directory becomes clean.
    """
    yield not cset and not is_clean(repo, cset, _cache)
    call(sh2cmd(repo.shelve.bake(interactive=True)))

@cmd(name='Update: update working directory (or switch revisions)')
def update(repo, cset, _cache):
    """Update working directory (or switch revisions)

    Update the repository's working directory to the specified changeset.
    """
    yield cset and not is_cwd(repo, cset, _cache)
    call(sh2cmd(repo.update.bake(rev=cset)))

@cmd(name='Histedit: edit the chunck of history between cwd and selected')
def histedit(repo, cset, _cache):
    """perform `histedit' if the repository is clean"""
    # XXX check if selected is before cwd but it may take a while :/
    yield cset and is_clean(repo, cset, _cache) and not is_cwd(repo, cset, _cache)
    call(sh2cmd(repo.histedit.bake(rev=cset)))

@cmd(name='Rebase: move changeset (and descendants) onto of the working directory')
def rebase(repo, cset, _cache):
    """Move changeset (and descendants) onto of the working directory"""
    yield cset and is_rebasable(repo, cset, _cache)
    call(sh2cmd(repo.rebase.bake(source=cset, dest='.')))
    call(sh2cmd(repo.update.bake(rev='tip')))

@cmd(name='rebase one: move changeset onto the working directory')
def rebase_one(repo, cset, _cache):
    """Move changeset onto the working directory"""
    yield cset and is_rebasable(repo, cset, _cache)
    call(sh2cmd(repo.rebase.bake(rev=cset, dest='.')))
    call(sh2cmd(repo.update.bake(rev='tip')))

@cmd(name='Graft: copy changes from other branches onto the working direstory')
def graft(repo, cset, _cache):
    """Copy changes from other branches onto the working direstory"""
    yield cset and is_rebasable(repo, cset, _cache)
    call(sh2cmd(repo.graft.bake(source=cset)))

@cmd(name="Draft: mark the changeset as draft")
def draft(repo, cset, _cache):
    """Set the changeset as draft"""
    yield cset and get_phase(repo, cset, _cache) == 'secret'
    call(sh2cmd(repo.phase.bake(draft=True)))

@cmd(name="Push: push changes to the default destination")
def push(repo, cset, _cache):
    """push changes to the default destination"""
    yield cset and get_phase(repo, cset, _cache) != 'secret'
    call(sh2cmd(repo.push.bake(rev=cset, new_branch=True)))

@cmd(name='Revert: restore files to the selected chechout state')
def revert(repo, cset, _cache):
    """perform 'revert --all' depending on cset if the repository is not
    clean or selected is not cwd"""
    yield cset or not is_clean(repo, cset, _cache)
    if cset:
        call(sh2cmd(repo.revert.bake(rev=cset, all=True)))
    else:
        call(sh2cmd(repo.revert.bake(all=True)))

@cmd(name='Edit description: amend changeset description and rebase unstables')
def edit_description(repo, cset, _cache):
    """Perform multiple tasks (update, amend, rebase) to edit the commit
    description."""
    yield cset and is_clean(repo, cset, _cache) and get_phase(repo, cset, _cache) != 'public'
    revset = 'children(%(n)s)' % {'n': cset}
    torebase = unicode(repo.log(template='{node},', rev=revset)).strip()
    call(sh2cmd(repo.update.bake(rev=cset)))
    call(sh2cmd(repo.commit.bake(edit=True, amend=True)))
    newcset = unicode(repo.log(limit=1, template='{node}')).strip()
    if not torebase:
        return
    for node in torebase.split(','):
        node = node.strip()
        if node:
            call(sh2cmd(repo.rebase.bake(source=node, dest=newcset)))

# tests
# #####

def is_rebasable(repo, cset, _cache):
    """Return True if the given cset can be rebased"""
    if is_cwd(repo, cset, _cache) or get_phase(repo, cset, _cache) == 'public':
        _cache['rebasable'] = False
    elif not _cache.get('rebasable'):
        revset = 'ancestor(%(c)s,.) and not %(c)s' % {'c': cset}
        _cache['rebasable'] = bool(unicode(repo.log(rev=revset, template="{node}")))
    return _cache['rebasable']

def get_phase(repo, cset, _cache):
    """Return the phase name of the cset"""
    if not _cache.get('phase'):
        _cache['phase'] = unicode(repo.log(rev=cset, template="{phase}"))
    return _cache['phase']

def is_cwd(repo, cset, _cache):
    """Return True if the given cset is the parent of the working directory"""
    parent = unicode(get_summary(repo, cset, _cache)['parent'])
    return parent.split(':', 1)[1][:12] == cset[:12]

def is_clean(repo, cset, _cache):
    """Return True if the working directory is not durty"""
    return 'clean' in get_summary(repo, cset, _cache)['commit']

# pylint: disable=unused-argument
def get_summary(repo, cset, _cache):
    """Return `hg summary -v`"""
    if not _cache.get('summary'):
        _cache['summary'] = dict(line.split(':', 1)
                                 for line in repo.summary(verbose=True)
                                 if ':' in line)
    return _cache['summary']
