#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#2009-02-18
# Copyright 2009 Michael Towers

"""
1) Generally something like: pygettext.py -p i18n -o larchin.pot *.py

I think poedit can do most of the processing, but the steps are:

2) cd i18n ; msginit -i larchin.pot -l de

OR:
2a) to update a po file:

cd i18n ; msgmerge -U larchin.po larchin.pot

3) edit po file

4) generate binary file:
cd i18n ; msgfmt -c -v -o larchin.mo larchin.po

5) move the .mo file to i18n/de/LC_MESSAGES

6) Add to the main program file:

import gettext
gettext.install('larchin', 'i18n', unicode=1)

5) Run, e.g.:
LANG=de_DE larchin.py
"""

import sys, os, shutil
from subprocess import call

thisdir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(thisdir)
os.chdir(basedir)

if (len(sys.argv) < 2):
    lang = "de"
else:
    lang = sys.argv[1]
print "Generating internationalization for language '%s'\n" % lang
print "    If you wanted a different language run 'i18n.py <language>'"
print "    For example 'i18n.py fr'\n"

dirs = ["run", "modules", "modules/stages", "modules/gtk"]
allpy = [os.path.join(d, "*.py") for d in dirs]
call(["pygettext.py", "-p", thisdir, "-o", "larchin.pot"] + allpy)

os.chdir(thisdir)
langfile = lang + ".po"
pofile = os.path.join(lang, "LC_MESSAGES", langfile)
if os.path.isfile(pofile):
    shutil.copy(pofile, ".")
    call(["msgmerge", "-U", langfile, "larchin.pot"])
else:
    call(["sed", "-i", "s|CHARSET|utf-8|", "larchin.pot"])
    call(["msginit", "--no-translator", "-i", "larchin.pot", "-l", lang])

lf = open("lang", "w")
lf.write(lang)
lf.close()

print "Now edit '%s' and then run 'i18n2.py'" % langfile
