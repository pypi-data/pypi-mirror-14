# -*- coding: utf-8 -*-
#
# path pattern: define global path aliases, cloneto command
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

"""Define [paths] once and reuse over many repositories.

path_pattern
------------

This extension frees you from defining and maintaining [paths]
individually for every repository.  Instead, you may define general
patterns of how to resolve paths.

For example, write::

    [path_pattern]
    abc.local = ~/abcdevel/{repo}
    abc.remote =  ssh://johny@devel.abc.com/sources/{repo}
    dev.local = ~/sources/{repo}
    dev.remote =  https://tim@devel-department.local/{repo}

and use ``hg push abc`` in any repo kept below ``~/abcdevel`` or ``hg
pull dev`` in any repo below ``~/sources``.

cloneto
-------

The extension defines also ``cloneto`` helper, which clones current
repo to address specified by given path.  It works especially well
together with patterns.  With the example above:

    cd ~/sources/libs
    hg init xyz
    cd xyz
    hg cloneto dev

More information
----------------

For more information, see path_pattern README or
http://bitbucket.org/Mekk/mercurial-path_pattern/
"""

from mercurial import commands, util
from mercurial.i18n import _
import os
import sys
import re


def import_meu():
    """Importing mercurial_extension_utils so it can be found also outside
    Python PATH (support for TortoiseHG/Win and similar setups)"""
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

# pylint:disable=fixme,line-too-long,invalid-name
#   (invalid-name because of ui and cmdtable)

############################################################
# Utility classes and functions
############################################################


class PatternPair(object):
    """
    Represents individual path pattern - pair of local (like
    "~/sources/{path}") and remote (like "ssh://some/where/{path}")
    """
    def __init__(self, prefix):
        self.prefix = prefix
        self.alias = prefix
        self.local = None
        self.remote = None
        self.enforce = False

    def lookup_remote(self, local_directory, ui):
        """
        Checks whether local directory matches, if so, returns
        matching remote, if not, returns None.
        """
        value = None
        if self.local and self.remote:
            match = self.local.search(local_directory)
            if match is not None:
                value = self.remote.fill(**match)
                if not value:
                    ui.warn(_("path_pattern: Invalid pattern - markers mismatch between %s.local and %s.remote\n")
                            % (self.prefix, self.prefix))
        return value

    def learn_local(self, path_text, ui):
        """Parse and save local path"""
        self.local = meu.DirectoryPattern(path_text, ui)

    def learn_remote(self, path_text, ui):
        """Parse and save remote path"""
        self.remote = meu.TextFiller(path_text, ui)
        # TODO: validate whether path_text looks like path

    def validate(self, ui):
        """Checks whether both sides are defined and valid. Warns about problems"""
        for name, obj in [("local", self.local),
                          ("remote", self.remote)]:
            if not obj:
                ui.warn(
                    _("path_pattern: Incomplete pattern - missing %s.%s\n") % (self.prefix, name))
                return False
            if not obj.is_valid():
                ui.warn(
                    _("path_pattern: Invalid pattern %s.%s - bad syntax\n") % (self.prefix, name))
                return False
        return True

    def describe(self):
        return _("%s%s\n    local:  %s\n    remote: %s") % (
            self.alias,
            self.enforce and " [*]" or "",
            self.local.pattern_text, self.remote.fill_text)

    _re_lead = re.compile(r'^([^{(]*)')
    _re_fill = re.compile(r'(?: { [^}]* }   |   \( [^)]* \)  )', re.VERBOSE)

    def calc_score(self):
        """Calculates ”strength” of local part of the pattern, used to prioritize
        patterns."""
        match = self._re_lead.search(self.local.pattern_text)
        lead_items = match.group(1).replace('\\', '/').split('/')
        text_without_fillers = self._re_fill.sub('', self.local.pattern_text)
        return (2 if self.enforce else 0, len(lead_items), len(text_without_fillers))


class PathPatterns(object):
    """
    Loads and parses pattern definitions
    """
    def __init__(self, ui):
        self.patterns = {}   # prefix → PatternPair
        # Read «sth».local
        for prefix, value in meu.suffix_config_items(ui, "path_pattern", "local"):
            if prefix not in self.patterns:
                self.patterns[prefix] = PatternPair(prefix)
            ui.debug(_("path_pattern: Parsing local side of path pattern %s") % prefix)
            self.patterns[prefix].learn_local(value, ui)
        # Read «sth».remote
        for prefix, value in meu.suffix_config_items(ui, "path_pattern", "remote"):
            if prefix not in self.patterns:
                self.patterns[prefix] = PatternPair(prefix)
            ui.debug(_("path_pattern: Parsing remote side of path pattern %s") % prefix)
            self.patterns[prefix].learn_remote(value, ui)
        # Read «sth».enforce
        for prefix, value in meu.suffix_configbool_items(ui, "path_pattern", "enforce"):
            if prefix in self.patterns:
                self.patterns[prefix].enforce = value
        # Read «sth».alias
        for prefix, value in meu.suffix_config_items(ui, "path_pattern", "alias"):
            if prefix in self.patterns:
                self.patterns[prefix].alias = value
        # Check for incomplete and invalid items
        for prefix in self.patterns.keys()[:]:
            if not self.patterns[prefix].validate(ui):
                del self.patterns[prefix]

    def generate_paths(self, ui, repo):
        """
        Updates ui config with new path's for given repo, generated from patterns
        """
        HGRC_PATH_SCORE = (1,)

        # Support for priority management. This is a mapping
        #    alias → (name, score)
        # where score is a tuple reflecting the priority (first item is
        # 0 for normal patterns, 1 for per-repo paths, 2 for enforced patterns,
        # see calc_score)
        known_aliases = {}

        # Reading known paths to avoid overwriting them (unless enforced).
        for key, value in ui.configitems("paths"):
            known_aliases[key] = (".hg/hgrc in " + repo.root, HGRC_PATH_SCORE)

        # Actually applying new patterns (with respect to prioritization)
        for prefix, pattern_pair in self.patterns.iteritems():
            expanded = pattern_pair.lookup_remote(repo.root, ui)
            if expanded:
                path_alias = pattern_pair.alias
                score = pattern_pair.calc_score()
                if path_alias in known_aliases:
                    prev_name, prev_score = known_aliases[path_alias]
                    if score < prev_score:
                        ui.debug(_("path_pattern: NOT defining path %s as %s (pattern %s is less important than %s)\n") % (path_alias, expanded, prefix, prev_name))
                        continue
                    else:
                        ui.debug(_("path_pattern: Defining path %s as %s (using pattern %s, overriding %s applied earlier as new pattern is stronger\n") % (path_alias, expanded, prefix, prev_name))
                else:
                    ui.debug(_("path_pattern: Defining path %s as %s (using pattern %s)\n") % (path_alias, expanded, prefix))
                known_aliases[path_alias] = (prefix, score)
                ui.setconfig("paths", path_alias, expanded)


    def print_patterns(self, ui, list_repos=False):
        """
        Prints pattern information to standard output
        """
        if self.patterns:
            has_enforced = any(p.enforce for p in self.patterns.values())
            ui.status(_("Defined path patterns:\n%s\n%s") % (
                "\n".join(
                    self.patterns[pname].describe()
                    for pname in sorted(self.patterns.keys())),
                _("[*]-marked patterns are enforced over .hg/hgrc") if has_enforced else "",
            ))
        else:
            ui.status(_("No path patterns defined. Add [path_pattern] section to ~/.hgrc\n"))


############################################################
# Mercurial extension hooks
############################################################

patterns = None

# def uisetup(ui):
# Not used, better to load patterns later, config can be updated by plugins


def extsetup(ui):
    """Setup extension: load patterns definitions from config"""
    global patterns    # pylint:disable=global-statement
    patterns = PathPatterns(ui)


def reposetup(ui, repo):
    """Setup repo: add pattern-based paths to repository config"""
    # Checking whether this is local repository, for other types extension
    # is pointless. Unfortunately we can't test repo type, as some extensions
    # change it (for example hgext.git.hgrepo.hgrepo happens to me…)
    if not hasattr(repo, 'root'):
        return
    patterns.generate_paths(ui, repo)


############################################################
# Commands
############################################################

cmdtable = {}
command = meu.command(cmdtable)


@command("list_path_patterns",
         [
             # ('r', 'list-repos', None, 'List repositories matching the pattern'),
         ],
         _("list_path_patterns"),
         norepo=True)
def cmd_list_path_patterns(ui, **opts):
    """
    List all active path patterns.
    """
    patterns.print_patterns(ui)


@command("cloneto",
         [],
         _("cloneto ALIAS"))
def cmd_cloneto(ui, repo, path_alias, **opts):
    """
    Clone current repository to (usually remote) url
    pointed by already defined path alias::

        hg cloneto somealias

    is equivalent to::

        hg clone . <aliaspath>

    where <aliaspath> is whatever somealias expands to
    according to ``hg paths``.

    Command most useful together with path_pattern. 
    """
    known_paths = []
    for key, value in ui.configitems("paths"):
        if key == path_alias:
            ui.status(_("Cloning current repository to %s (resolved from: %s)\n" % (value, path_alias)))
            return commands.clone(ui, source=repo, dest=value)
        else:
            known_paths.append(key)
    # Failing helpfully
    if known_paths:
        raise util.Abort(_("Unknown alias: %s. Defined path aliases: %s") % (
            path_alias, ", ".join(known_paths)))
    else:
        raise util.Abort(_("Uknown alias: %s. No paths defined, consider creating some paths or path_patterns") % path_alias)

############################################################
# Extension setup
############################################################

testedwith = '2.7 2.9 3.0 3.3 3.6'
buglink = 'https://bitbucket.org/Mekk/mercurial-path_pattern/issues'
