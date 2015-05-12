#!/usr/bin/env python3

# Search for unnecessary MK4-Files from Akregator in the Archive-Directory.
#
# Open the "feeds.opml" and search for the tag "xmlUrl".
# Construct valid Metakit-Filenames and compare these
# with the MK4-Files found in the Archive-Directory.
# Report wich files are found only in the Archive-Directory and
# not listed in the feeds.opml.
#
# Version:  2015-05-08
#
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

from datetime import datetime
import argparse
import os

file_opml = os.path.join(os.environ['HOME'],
                         '.kde4/share/apps/akregator/data/feeds.opml')
dir_archive = os.path.join(os.environ['HOME'],
                           '.kde4/share/apps/akregator/Archive/')

mk4_dir = os.listdir(dir_archive)
mk4_dir.remove('feedlistbackup.mk4')
mk4_dir.remove('archiveindex.mk4')

mk4_opml = []
with open(file_opml, mode='rt') as opml:
    line = opml.readline()
    while line is not '':
        elements = line.split()
        for element in elements:
            if element.startswith('xmlUrl'):
                # rename the entries in the feed.opml to valid mk4-files
                element = element.lstrip('xmlUrl=')
                element = element.strip('"')
                element = element.replace('/', '_')
                element = element.replace(':', '_')
                element = element.replace('&amp;', '&')
                element = element + '.mk4'
                mk4_opml.append(element)
        line = opml.readline()
    opml.close()

# create new list with filenames found in mk4_dir but not in the mk4_opml
orphan_mk4 = [f for f in mk4_dir if f not in mk4_opml]
broken_opml = [e for e in mk4_opml if e not in mk4_dir]

parser = argparse.ArgumentParser(description=
                                 'List all MK4-Files from "' + dir_archive + '"\
                                 without being found in the OPML. These are \
                                 most likely orphans from deleted subscription.')
parser.add_argument('-l',
                    '--long',
                    help='List orphan MK4-Files with full path',
                    action='store_true')
parser.add_argument('-d',
                    '--delete',
                    help='Delete orphan MK4-Files',
                    action='store_true')
parser.add_argument('-b',
                    '--broken',
                    help='List entries found in the OPML with no corresponding MK4-File',
                    action='store_true')
args = parser.parse_args()
if args.long:
    for f in orphan_mk4:
        path = os.path.join(dir_archive, f)
        print(path)
elif args.delete:
    for f in orphan_mk4:
        delete = os.path.join(dir_archive, f)
        print('Removed ' + delete)
        trashfiles = os.path.join(os.environ['HOME'],
                                  '.local/share/Trash/files/', f)
        os.rename(delete, trashfiles)
        trashinfo = os.path.join(os.environ['HOME'],
                                 '.local/share/Trash/info/', f + '.trashinfo')
        with open(trashinfo, mode='w') as info:
            info.write('[Trash Info]\n')
            info.write('Path=' + delete + '\n')
            info.write('DeletionDate=' + datetime.now().isoformat()[0:19] + '\n')
            info.close()
elif args.broken:
    for e in broken_opml:
        print(e)
else:
    for f in orphan_mk4:
        print(f)
