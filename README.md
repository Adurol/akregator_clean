# akregator_clean

If a feed subscription in Akregator is deleted, the corresponding Metakit-File will remain.<br>
```akregator_clean_orphans.py``` searches for orphan MK4-Files with no subscription and reports or deletes them.

### Requirements
* KDE4
* Python >= 3.2

### Usage
```bash
python3 akregator_clean_orphans.py -h
```
### License
* DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE

### Notes
* Works and (eyeball)tested on KDE4 with a few hundred MK4-Files.
* To lazy to parse the ```feeds.opml``` as XML. Just did a ```readline```. Dirty, but works.
Maybe if I need a parsing exercise it will be revised.
* This script was born out of the need from an old (apparently fixed) bug that would crash Akregator with an overfull Archive-Directory.
