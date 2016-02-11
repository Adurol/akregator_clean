![works badge](https://img.shields.io/badge/works-for_me-brightgreen.svg)
![license](http://img.shields.io/badge/license-MIT-blue.svg?link=http://opensource.org/licenses/MIT)
# akregator_clean

When a feed subscription in Akregator is deleted, the corresponding Metakit-File will remain. `akregator_clean_orphans.py` searches for these orphan MK4-Files with no subscription and reports or deletes them.

### Requirements
* KDE Plasma 5
* Python >= 3.2

### Usage
```
$ python3 akregator_clean_orphans.py -h

usage: akregator_clean_orphans.py [-h] [-l] [-b] [-d]

List all MK4-Files within "/home/username/.local/share/akregator/Archive/"
without being found in the "/home/username/.local/share/akregator/data/feeds.opml".
These are most likely orphans from deleted subscriptions.

optional arguments:
  -h, --help    show this help message and exit
  -l, --long    list orphan MK4-Files with full path
  -b, --broken  list entries found in the OPML with no corresponding MK4-File
  -d, --delete  delete orphan MK4-Files to Trash
```

### License
* MIT

### Notes
* Works and (eyeball)tested on KDE Plasma 5 with a few hundred MK4-Files.
* To lazy to parse the ```feeds.opml```. Just did a ```readline```. Dirty, but works. Maybe if I need a parsing exercise it will be revised.
* This script was born out of the need from an old (apparently fixed) bug that would crash Akregator with an overfull Archive-Directory.
* Just change the path accordingly and it should work with KDE4.