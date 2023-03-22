#-*- coding: utf-8 -*-
import csv
import sys

from pathlib import PurePath

if len(sys.argv) < 3:
    print('Must specify <path_to_csv_with_file_names> <path_to_codeowners>')
    sys.exit(1)

def parse_codeowners(file_path):
    with open(file_path) as codeowners_file:
        codeowners = []
        for line_num, line in enumerate(codeowners_file):
            if line.startswith('#') or not line.strip():
                continue
            line = line.replace('\t', ' ')
            path = line.split(' ')[0]
            parts = line.split(' ', 1)
            if len(parts) != 2:
                print(f'Not sure what to do with line {line_num + 1} `{line.strip()}`')
                continue
            owners = parts[1].strip()
            codeowners.append((path, owners))
    return codeowners

def find_best_match(path, codeowners):
    file_to_match = PurePath(path)
    if file_to_match.is_absolute():
        print(f"Skipping {path} because it looks like an absolute path. Must be relative")
        return None
    best_matched_owners = None
    best_matched_path = PurePath()
    for (owner_path, owners) in codeowners:
        # For this to work, have to turn absolute paths in CODEOWNERS into relative paths
        # TODO: Do this in a platform agnostic way
        owner_path = owner_path[1:] if owner_path.startswith('/') else owner_path
        owner_path = PurePath(owner_path)
        try:
            # Since a CODEOWNER file can have an entry like /foo/bar/ and /foo/bar/baz.py
            # We have keep iterating through and only keep the most specific path possible
            if file_to_match.relative_to(owner_path) and len(owner_path.parts) > len(best_matched_path.parts):
                best_matched_owners = owners
                best_matched_path = owner_path
        except ValueError:
            # This owners entry did not cover the file in question
            pass
    return best_matched_owners


matches = []
codeowners = parse_codeowners(sys.argv[2])

with open(sys.argv[1]) as usage_file:
    usage_csv = csv.DictReader(usage_file, delimiter=',')
    for i, row in enumerate(usage_csv):
        best_matched_owners = find_best_match(row['File'], codeowners)
        if best_matched_owners:
            # print(f"Owner for {row['File']} is {best_matched_owners}")
            matches.append([row['File'], best_matched_owners])
        else:
            # print(f"No owner found for {row['File']}")
            matches.append([row['File'], 'None Found'])

with open('output.csv', 'w') as output_file:
    writer = csv.writer(output_file)
    for match in matches:
        writer.writerow(match)
