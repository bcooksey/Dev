#!/bin/python
# The purpose of this script is to scan a directory and substitute one substring for another in all the files in that dir
# Freely edit the regexes to match whatever pattern you need
import os, re

DIR = './' # Change so that this points to the directory you need to scan
files = os.listdir(DIR)

print "Found {} files".format(len(files))

regex = re.compile('<a.*?data-nav="(.*?)"')
regex2 = re.compile('href="(.*?)"')

for file_name in files:
    print DIR + file_name
    f = open(DIR + file_name, 'r')
    text = f.read()
    f.close()

    matches = regex.finditer(text)
    rev_matches = []
    for match in matches:
        rev_matches.insert(0, match)

    last_pos = None
    new_text = ''
    for match in rev_matches:
        new_text = text[match.end():last_pos] + new_text
        replacement = 'href="{}"' if match.groups()[0].startswith('/') else 'href="/{}"'
        new_text = regex2.sub(replacement.format(match.groups()[0]), text[match.start():match.end()]) + new_text
        last_pos = match.start()

    new_text = text[0:last_pos] + new_text
    print new_text
    # Uncomment to do it for real!
    # f = open(DIR + file_name, 'w')
    # f.write(new_text)
    # f.close()
