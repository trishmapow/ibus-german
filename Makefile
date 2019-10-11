# only really known to work on ubuntu, if you're using anything else, hopefully
# it should at least give you a clue how to install it by hand

PREFIX ?= /usr
SYSCONFDIR ?= /etc
DATADIR ?= $(PREFIX)/share
DESTDIR ?=

PYTHON ?= /usr/bin/python3

all: autogerman.xml config.py

autogerman.xml: autogerman.xml.in
	sed -e "s:@PYTHON@:$(PYTHON):g;" \
	    -e "s:@DATADIR@:$(DATADIR):g" $< > $@

config.py: config.py.in
	sed -e "s:@SYSCONFDIR@:$(SYSCONFDIR):g" $< > $@

install: all
	install -m 0755 -d $(DESTDIR)$(DATADIR)/ibus-german $(DESTDIR)$(SYSCONFDIR)/xdg/ibus-german $(DESTDIR)$(DATADIR)/ibus/component
	install -m 0644 icon.png $(DESTDIR)$(DATADIR)/ibus-german
	install -m 0755 dictcc.py $(DESTDIR)$(DATADIR)/ibus-german
	install -m 0644 en_parsed_dictcc.txt $(DESTDIR)$(DATADIR)/ibus-german
	install -m 0644 de_parsed_dictcc.txt $(DESTDIR)$(DATADIR)/ibus-german
	install -m 0644 config.py $(DESTDIR)$(DATADIR)/ibus-german
	install -m 0644 ibus.py $(DESTDIR)$(DATADIR)/ibus-german
	install -m 0644 autogerman.xml $(DESTDIR)$(DATADIR)/ibus/component

uninstall:
	rm -f $(DESTDIR)$(DATADIR)/ibus-german/icon.png
	rm -f $(DESTDIR)$(DATADIR)/ibus-german/dictcc.py
	rm -f $(DESTDIR)$(DATADIR)/ibus-german/de_parsed_dictcc.txt
	rm -f $(DESTDIR)$(DATADIR)/ibus-german/en_parsed_dictcc.txt
	rm -f $(DESTDIR)$(DATADIR)/ibus-german/config.py
	rm -f $(DESTDIR)$(DATADIR)/ibus-german/ibus.py
	rmdir $(DESTDIR)$(DATADIR)/ibus-german
	rmdir $(DESTDIR)$(SYSCONFDIR)/xdg/ibus-german
	rm -f $(DESTDIR)$(DATADIR)/ibus/component/autogerman.xml

clean:
	rm -f autogerman.xml
	rm -f config.py
