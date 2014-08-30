#!/usr/bin/python
# Simple time converting script. Give it an ISO, get back UNIX Timestamp
import sys
from datetime import datetime

if len(sys.argv) == 1:
    print 'Need to give me at least one ISO time to convert'
    sys.exit()

count = 1
for t in sys.argv[1:]:
    print "{0}: {1}".format(count, datetime.strptime(t, '%Y-%m-%d %H:%M:%S').strftime('%s'))
    count += 1
