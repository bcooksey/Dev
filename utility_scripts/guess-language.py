#!/usr/bin/python
import os
import sys
import http.client
from collections import defaultdict

if len(sys.argv) < 2:
    print('You need to provide a URL')
    exit()

EXTENSION_MAP = {
    '.py': 'Python',
    '.ts': 'TypeScript',
    '.js': 'JavaScript',
    '.go': 'Golang',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.java': 'Java',
    '.pl': 'Pearl',
    '.sh': 'Shell',
    '.bash': 'Shell',
    '.rs': 'Rust',
    '.cs': 'C#',
    '.cpp': 'C++',
    '.md': 'Ignore',
    '.txt': 'Ignore',
    '.log': 'Ignore',
    '.html': 'Ignore',
    '.css': 'Ignore',
    '.sql': 'Ignore',
    '.xml': 'Ignore',
    '.json': 'Ignore',
}

data = []
line_counts_by_extension = defaultdict(int)

# Read the file
conn = http.client.HTTPSConnection("patch-diff.githubusercontent.com")
conn.request("GET", sys.argv[1])
res = conn.getresponse()
if res.status != 200:
    conn.close()
    print('Could not read the data')
    exit()
data = res.read().decode('utf-8').splitlines()
conn.close()

# These are for debugging using a local file
# with open(sys.argv[1]) as source_file:
#     data = list(source_file)

# Count the lines by file type
current_extension = ''
for line in data:
    line = line.strip()
    if line.startswith('+++'):
        current_extension = os.path.splitext(line)[1]
    elif line.startswith('+'):
        line_counts_by_extension[current_extension] += 1
    else:
        pass

sorted_counts = list(line_counts_by_extension.items())
sorted_counts.sort(key=lambda y: y[1], reverse=True)

for tup in sorted_counts:
    language = EXTENSION_MAP.get(tup[0])
    if not language:
        break
    elif language != 'Ignore':
        print('This project is mostly {}'.format(language))
        exit()
    else:
        pass

print('It is not clear what this project is written in. Here is the breakdown of LOC by file type:')
print(sorted_counts)
