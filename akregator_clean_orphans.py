#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Search unnecessary MK4-Files of Akregator in the Archive-Directory.
#
# Open the "feeds.opml" and search the tag "xmlUrl" for reference.
# Construct valid Metakit-Filenames and compare with MK4-Files in
# the Archive-Directory. Report oprhan files only found in the
# Archive-Directory and not listed in the "feeds.opml".
#
# Version:  2016-02-10

# The MIT License (MIT)
#
# Copyright (c) lies with the work's creator
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from datetime import datetime
import argparse
import os


file_opml = os.path.join(os.environ['HOME'], '.local/share/akregator/data/feeds.opml')
dir_archive = os.path.join(os.environ['HOME'], '.local/share/akregator/Archive/')


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
orphans = [f for f in mk4_dir if f not in mk4_opml]
broken = [e for e in mk4_opml if e not in mk4_dir]


parser = argparse.ArgumentParser(description='List all MK4-Files from "' + dir_archive + '"\
                                 without being found in the OPML. These are \
                                 most likely orphans from deleted subscription.')
parser.add_argument('-l', '--long',
                    help='List orphan MK4-Files with full path',
                    action='store_true')
parser.add_argument('-d', '--delete',
                    help='Delete orphan MK4-Files',
                    action='store_true')
parser.add_argument('-b', '--broken',
                    help='List entries found in the OPML with no corresponding MK4-File',
                    action='store_true')
args = parser.parse_args()
if args.long:
    for orphan in orphans:
        path = os.path.join(dir_archive, orphan)
        print(path)
elif args.delete:
    for orphan in orphans:
        del_file = os.path.join(dir_archive, orphan)
        trash_dir = os.path.join(os.environ['HOME'], '.local/share/Trash/')
        trash_file = os.path.join(trash_dir, 'files/', orphan)
        trash_info = os.path.join(trash_dir, 'info/', orphan + '.trashinfo')
        os.rename(del_file, trash_file)
        with open(trash_info, mode='w') as info:
            info.write('[Trash Info]\n')
            info.write('Path=' + del_file + '\n')
            info.write('DeletionDate=' + datetime.now().isoformat()[0:19] + '\n')
            info.close()
        print('Removed ' + del_file)
elif args.broken:
    for e in broken:
        print(e)
else:
    for orphan in orphans:
        print(orphan)
