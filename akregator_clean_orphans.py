#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Clean up unnecessary MK4-Files from Akregator in the Archive-Directory.
#
# Open the "feeds.opml" and search "xmlUrl"-tags as reference to construct valid
# Metakit-Filenames (MK4). Search for matching MK4-Files in the Archive-Directory.
# Report oprhan files found only in the Archive-Directory and not listed in the "feeds.opml".
#
# Version:  2016-03-10

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


import os

try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

from datetime import datetime


feeds_opml = os.path.join(os.environ['HOME'], '.local/share/akregator/data/feeds.opml')
archive_path = os.path.join(os.environ['HOME'], '.local/share/akregator/Archive/')

mk4 = os.listdir(archive_path)
mk4.remove('feedlistbackup.mk4')
mk4.remove('archiveindex.mk4')


outline = []

with open(feeds_opml, mode='rt') as opml:
    tree = ElementTree.parse(opml)
    opml.close()

for node in tree.iter('outline'):
    xmlUrl = node.attrib.get('xmlUrl')

    # folders have no xmlUrl
    if xmlUrl is not None:
        # convert entries found in the feed.opml to mk4-filenames used by Akregator
        xmlUrl = xmlUrl.replace('/', '_')
        xmlUrl = xmlUrl.replace(':', '_')
        xmlUrl = xmlUrl.replace('&amp;', '&')
        xmlUrl = xmlUrl + '.mk4'
        outline.append(xmlUrl)


# here works the magic
orphans = [filename for filename in mk4 if filename not in outline]
broken = [element for element in outline if element not in mk4]


def trash(filepath):
    """Move file to Trash if requested and create corresponding metadata.

    This implementation is pretty simplified and is NOT conform with the FreeDesktop.org
    Trash specification v1.0 (2014-01-02). If the file already exist in the Trash can,
    it will be replaced silently. This is not appropriate as the specification states
    "each subsequent trashing must not overwrite a previous copy"!
    For the usecase here, it should be good enough. You have been warned.
    """
    try:
        org_path = os.path.normpath(filepath)
        org_filename = os.path.basename(org_path)

        # getting $XDG_DATA_HOME is cumbersome, so hardcoding the path to trash
        trash_files = os.path.join(os.environ['HOME'],
                                   '.local/share/Trash/files/', org_filename)
        trash_info = os.path.join(os.environ['HOME'],
                                  '.local/share/Trash/info/', org_filename + '.trashinfo')

        with open(trash_info, mode='w') as info:
            info.write('[Trash Info]\n')
            info.write('Path=' + del_file + '\n')
            info.write('DeletionDate=' + datetime.now().isoformat()[0:19] + '\n')
            info.close()

        os.rename(org_path, trash_files)

    except FileNotFoundError:
        raise FileNotFoundError(filepath)


if __name__ == "__main__":
    # hack to bypass the default column size of 80 for argparse
    os.environ['COLUMNS'] = os.popen('stty size', 'r').read().split()[1]

    import argparse

    parser = argparse.ArgumentParser(description='List all MK4-Files within "' + archive_path +
                                     '" without being found in the "' + feeds_opml +
                                     '". These are most likely orphans from deleted subscriptions.')

    parser.add_argument('-l', '--long',
                        help='list orphan MK4-Files with full path',
                        action='store_true')

    parser.add_argument('-b', '--broken',
                        help='list entries found in the OPML with no corresponding MK4-File',
                        action='store_true')

    parser.add_argument('-d', '--delete',
                        help='delete orphan MK4-Files to Trash',
                        action='store_true')

    args = parser.parse_args()

    if args.long:
        for orphan in orphans:
            path = os.path.join(archive_path, orphan)
            print(path)

    elif args.delete:
        for orphan in orphans:
            del_file = os.path.join(archive_path, orphan)
            trash(del_file)
            print('Removed ' + del_file)

    elif args.broken:
        for entrie in broken:
            print(entrie)

    else:
        for orphan in orphans:
            print(orphan)
