# -*- coding: utf-8 -*-
#
# all dirs: execute the same Mercurial command on many repositories
#
# Copyright (c) 2015 Marcin Kasperski <Marcin.Kasperski@mekk.waw.pl>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# See README.txt for more details.

"""Execute the same command on many repositories

Imagine ~/src/libs/util, ~/src/libs/net/raw, ~/src/libs/net/logic,
and ~/src/progs/emit are Mercurial repositories. Then::

    cd ~/src
    hg alldirs status
    hg alldirs pull
    hg alldirs log -l 2
    hg alldirs commit -m "Licence change"

etc. The ``alldirs`` command locates all Mercurial repositories
inside current directory tree, and executes given command on each
of them in order.

For more information, see
    http://bitbucket.org/Mekk/mercurial-all_dirs/
"""

# pylint:disable=fixme,line-too-long,invalid-name
#   (invalid-name because of ui and cmdtable)

from mercurial import commands, util, dispatch, error, fancyopts, hg
from mercurial.i18n import _
import os
import sys


def import_meu():
    """Import mercurial_extension_utils, handling a few corner cases
    related to TortoiseHg@Win and similar installations."""
    try:
        import mercurial_extension_utils
    except ImportError:
        my_dir = os.path.dirname(__file__)
        sys.path.extend([
            # In the same dir (manual or site-packages after pip)
            my_dir,
            # Developer clone
            os.path.join(os.path.dirname(my_dir), "extension_utils"),
            # Side clone
            os.path.join(os.path.dirname(my_dir), "mercurial-extension_utils"),
        ])
        try:
            import mercurial_extension_utils
        except ImportError:
            raise util.Abort(_("""Can not import mercurial_extension_utils.
Please install this module in Python path.
See Installation chapter in https://bitbucket.org/Mekk/mercurial-dynamic_username/ for details
(and for info about TortoiseHG on Windows, or other bundled Python)."""))
    return mercurial_extension_utils

meu = import_meu()


ALL_DIRS_COMMAND = "alldirs"

############################################################
# Mercurial monkeypatching
#
# We need monkeypatching for two reasons:
#
# a) We wish to capture all options and args in commands
#    like
#         hg alld log -l 3 Makefile
#    and predeclaring them all seems difficult and unpleasant.
#
# b) We wish to reuse dispatch.dispatch multiple times,
#    but prefer to parse command line just once.
#
# Monkeypatching _parse resolves both issues. First, we
# handle detecting alldirs command and modifying parsing
# behaviour if it is found. Then, we let remaining code
# pre-define what _parse should return once called the very
# next time.
############################################################

# pylint: disable=global-statement
_predef_parse_reply = None


def set_predef_parse_reply(reply):
    """Sets reply which _parse is to return whenever called"""
    global _predef_parse_reply
    _predef_parse_reply = reply


def clear_predef_parse_reply():
    """Revert _parse to standard behaviour"""
    global _predef_parse_reply
    _predef_parse_reply = None


@meu.monkeypatch_function(dispatch)
def _parse(lui, args):
    """Monkeypathed Mercurial own parse.

    Modifies parsing behaviour in case alldirs command is being handled,
    to re-parse without it and return both alldirs as executed command,
    and actual parsing results.

    Returns predefined reply, if it is set (used while re-executing commands
    in subrepos).

    _parse returns 5-tuple:
         command name, command function, args, options, cmdoptions
     where:
         args are standalone args,
         options are (resolved) mercurial global flags (like quiet or debug)
         cmdoptions are (resolved) command-specific options
    """

    # Even when we run under --debug, lui does not (yet)
    # know about that (it is normally set inside _dispatch,
    # after parse).  As we need some debugging for a time,
    # this is quick hack
    if '--debug' in args:
        lui.debugflag = True

    # Recursive case, _parse called by dispatch we called ourselves
    if _predef_parse_reply:
        # lui.debug("all_dirs: _parse returns predefined reply:\n%s\n%s\n%s\n%s\n%s\n" % _predef_parse_reply)
        # Args turn out to be modified, so we copy it, to be safe also copy *opts*
        return (_predef_parse_reply[0],
                _predef_parse_reply[1],
                _predef_parse_reply[2][:],
                _predef_parse_reply[3].copy(),
                _predef_parse_reply[4].copy())

    lui.debug("all_dirs: _parse called with args %s\n" % args)
    try:
        parsed = _parse.orig(lui, args)
        if parsed[0] != ALL_DIRS_COMMAND:
            # Some other command is handled
            lui.debug("all_dirs: _parse found another command %s\n" % str(parsed[0]))
            return parsed
        # alldirs accidentally succeeded, good, we can use global options
        lui.debug(_("all_dirs: initial parse succeeded, some trivial command\n"))
        p_args, p_glbopts, p_cmdoptions = parsed[2], parsed[3], parsed[4]
        if p_cmdoptions:
            # Happens. Things like {mq: None} in status
            lui.debug(_("all_dirs: non-empty cmdoptions in pre-parse: %s\n") % p_cmdoptions)
    except error.CommandError as e:
        if e.args[0] != ALL_DIRS_COMMAND:
            # Some other command got bad options
            raise
        lui.debug(_("all_dirs: normal parse failed, fixing up (%s)\n") % str(e))
        # We parse global options, to get actual command on first place
        # but also to get consistent with non-exception variant
        p_glbopts = {}
        p_args = fancyopts.fancyopts(args, commands.globalopts, p_glbopts)
        # We have to drop alld command itself from args
        # There is also tiny risk some --option stayed before alld, so
        # we look for it carefully.
        idx = 0
        while idx < len(p_args):
            if p_args[idx].startswith(ALL_DIRS_COMMAND[0]):
                break
            idx += 1
        if idx >= len(p_args):
            raise util.Abort(_("alldirs: Can not find command name in parsed arguments. Please, contact the extension author. Args: %s") % p_args)
        p_args = p_args[:idx] + p_args[idx + 1:]

    # Parsing options of actual command.  Depending on the
    # path above, p_args contains only two names ("alld",
    # "log") or so, or also various unparsed args. Whatever
    # happened, we drop alldirs command and parse the rest.
    cmdparsed = _parse.orig(lui, p_args)

    lui.debug(_("all_dirs: finished parsing. Returning wrapper for %s command\n") % cmdparsed[0])
    return (
        ALL_DIRS_COMMAND,
        cmd_alldirs,
        [cmdparsed[0]],
        p_glbopts,   # From first parse, second didn't get options
        {
            # 'cmd': cmdparsed[0],
            'cmdfunc': cmdparsed[1],
            'cmdargs': cmdparsed[2],
            'cmdoptions': cmdparsed[4],
            'fullargs': args,
            'options': p_glbopts,
        }
    )


############################################################
# Mercurial extension hooks
############################################################

# def extsetup(ui):
#    """Setup extension: load patterns definitions from config"""
#    pass
#

############################################################
# Commands
############################################################

cmdtable = {}
command = meu.command(cmdtable)

@command(ALL_DIRS_COMMAND,
         [],
         "ANY-MERCURIAL-COMMAND [COMMAND-ARGS]",
         optionalrepo=True)
def cmd_alldirs(ui, repo, cmdname, **opts):
    """
    Execute given Mercurial command on all subdirectories
    """
    # print "UI", ui
    # print "REPO", repo
    # print "CMDNAME", cmdname
    # import pprint; print "OPTS", pprint.pformat(opts)

    # Provided by monkey-patched _parse
    cmdfunc = opts['cmdfunc']        # Actual function to call
    cmdargs = opts['cmdargs']        # Positional command args
    cmdoptions = opts['cmdoptions']  # Named command args
    options = opts['options']        # Global options
    fullargs = opts['fullargs']      # Original args

    # pylint: disable=too-many-arguments,star-args
    def execute_cmd(ui, repo,
                    cmdname, cmdfunc, cmdargs, cmdoptions,
                    options, fullargs):
        """Actually execute command. Mimicks _dispatch final steps."""
        msg = ' '.join(' ' in a and repr(a) or a for a in fullargs)
        ui.log("command", '%s\n', msg)
        d = lambda: util.checksignature(cmdfunc)(ui, repo, *cmdargs, **cmdoptions)
        ui.debug("all_dirs: spawning %s\n" % msg)
        return dispatch.runcommand(
            ui, repo, cmdname, fullargs, repo.ui, options, d,
            cmdargs[:], cmdoptions)

    if repo:
        # We are inside some repository. So just forward the call
        # to actual command without further fuss
        return execute_cmd(ui, repo,
                           cmdname, cmdfunc, cmdargs, cmdoptions,
                           options, fullargs)

    # We aren't inside repo, so let's iterate. We're looking for repos
    # starting from getcwd, as --cwd was already handled by Mercurial.
    failed = []
    initial_cwd = os.getcwd()
    try:
        # dispatch.dispatch calls _parse, so we overwrite expected reply
        set_predef_parse_reply(
            (cmdname, cmdfunc, cmdargs, options, cmdoptions))

        for path in meu.find_repositories_below(initial_cwd):
            ui.status(_("=> all_dirs: Executing %s in %s\n") % (cmdname, path))
            # Switching directory so file names work better
            os.chdir(path)

            # This snippet mimicks dispatch internal works
            copied_ui = ui.copy()
            repo = hg.repository(copied_ui, path=path)
            if not repo.local():
                raise util.Abort(_("repository '%s' is not local") % path)
            repo.ui.setconfig("bundle", "mainreporoot", repo.root)

            req = dispatch.request(
                args=fullargs, ui=copied_ui, repo=repo)
            ret = dispatch.dispatch(req)

            ui.debug("all_dirs: return status: %s\n" % ret)
            if ret == -1:
                failed.append(path)
    finally:
        # In case commandserver or sth like that works many commands
        clear_predef_parse_reply()
        os.chdir(initial_cwd)

    if failed:
        raise util.Abort(_("all_dirs: Executed command failed in:\n%s\n") % (
            "\n".join(["- " + path for path in failed])))
        # return -1
    return 0

############################################################
# Extension setup
############################################################

testedwith = '2.7 2.9 3.0 3.3 3.6 3.7'
buglink = 'https://bitbucket.org/Mekk/mercurial-all_dirs/issues'
