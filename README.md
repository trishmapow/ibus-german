AutoGerman for IBus
==================

(forked from the lovely [ibus-uniemoji](https://github.com/salty-horse/ibus-uniemoji) project)

This simple input method for [ibus](https://github.com/ibus/ibus) allows you to autocomplete German words and phrases (by typing in English or German) and view definitions provided by dict.cc. Word type, gender and both English and German tags are displayed when available.

![Example usage](/example.gif?raw=true)

Dependencies
-------------
- ibus
- python3
- python `recordclass` module e.g. `pip3 install recordclass`
- ibus gobject introspection information e.g. `sudo apt install gir1.2-ibus-1.0`

Installing
-----------

Unfortunately I cannot distribute the dict.cc dictionary with this package, and due to format quirks there are a few steps to make the txt file usable:

1. Download the raw file from https://www1.dict.cc/translation_file_request.php?l=e
2. Move the file to the `ibus-german` folder and rename to `dictcc.txt`
3. Run `python3 dictcc.py` once which will parse the file and output to `de_parsed_dictcc.txt` and `en_parsed_dictcc.txt`. This may take ~30s. These files are sorted in German/English for faster lookups. (Approximate size ~100MB each)
4. Run `sudo make install`

Old instructions: to install, type `make install`. If your ibus isn't on /usr/share/ibus, or you want to install to /usr/local, you can pass any of `PREFIX`, `DATADIR`, and `SYSCONFDIR` to `make`. You can also pass `DESTDIR` to aid in packaging, or `PYTHON` to use a different Python executable.

Running
--------

Restart (or start) your ibus. This can be done with the command `ibus restart`.

If you have customized your active input methods, you'll need to enable AutoGerman: open preferences (use the indicator if you have it, otherwise open “Keyboard Input Methods” on Ubuntu's dash, or run “ibus-setup”), go to the “Input Method” tab, click the “Select an input method” drop-down, AutoGerman will be in the “Other” category.

Then activate ibus using whatever key combination you have configured, and change input method until you have AutoGerman on (or use the drop-down you get by clicking the input method name on the input method toolbar).

Type some text you believe to be part of the name of an emoji or symbol. Select the one you want the usual ways (type more, use the cursor, numbers, mouse, touch...), and press Enter to insert.

Then you probably want to turn it off so you can type normal text.

Credits
--------

* AutoGerman fork: Christopher Malau
* Original author: Lalo Martins
* Original maintainer: Ori Avtalion


License
--------

AutoGerman is licensed under the GNU General Public License v3.0.