# -*- coding: utf-8 -*-
#
# dynamic username: switch commit username depending on the location
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

"""Define your username per directory tree.

Use different name and/or email depending on where you work.  For
example, if you write in your ``~/.hgrc``::

    [extensions]
    mercurial_dynamic_username =

    [dynamic_username]
    work.location = ~/work
    work.username = John Smith <john.smith@serious.com>
    hobby.location = ~/hobby, ~/blogging
    hobby.username = Johny <fastjohny@fantasy.net>

you will commit as John Smith in ``~/work/libs/payproc`` and as Johny
in ``~/blogging/travel``.

You can test effects by callling::

    hg showconfig ui.username

See extension README.txt or
http://bitbucket.org/Mekk/mercurial-dynamic_username/ for more info.
"""

# pylint:disable=fixme,line-too-long,invalid-name
#   (invalid-name because of ui and cmdtable)

from mercurial import util
from mercurial.i18n import _
import os
import sys


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

############################################################
# Extension logic
############################################################

CONFIG_SECTION = "dynamic_username"


def lookup_dynamic_username(ui, repo):
    """Checks whether any dynamic username is set for given repo.
    Returns it if so, returns None elsewhere"""
    meu = import_meu()

    # Looking up longest match
    if not hasattr(repo, 'root'):
        return None
    repo_path = os.path.abspath(repo.root)
    best_path = ''
    best_username = None

    # Iterate over «anything».location in [dynamic_username] section,
    # reading values as lists
    for prefix, trees in meu.suffix_configlist_items(
            ui, CONFIG_SECTION, "location"):
        canon_path = meu.belongs_to_tree_group(repo_path, trees)
        if canon_path:
            if len(canon_path) > len(best_path):
                best_path = canon_path
                # This will also set best_username to None if we miss .username to revert to default
                best_username = ui.config(CONFIG_SECTION, prefix + ".username", None)

    return best_username


############################################################
# Mercurial extension hooks
############################################################

def reposetup(ui, repo):
    """Setup repo: rewrite ui/username if needed"""
    dynamic_name = lookup_dynamic_username(ui, repo)
    if dynamic_name:
        ui.debug(_("dynamic_username: Updating username to dynamically-selected %s\n") % dynamic_name)
        ui.setconfig("ui", "username", dynamic_name)


############################################################
# Extension setup
############################################################

testedwith = '2.7 2.9 3.0 3.3 3.6 3.7'
buglink = 'https://bitbucket.org/Mekk/mercurial-dynamic_username/issues'

