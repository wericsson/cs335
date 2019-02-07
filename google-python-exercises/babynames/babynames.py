#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  file = open(filename, 'r')
  infile =  file.read()
  file.close()
  yearmatch = re.search(r'Popularity\sin\s(\d+)', infile)
  year = 0
  if yearmatch:
    year = yearmatch.group(1)
  else:
    sys.exit(1)
  namerankmatches = re.findall(r'td>(\d+)</td><td>(\w+)</td><td>(\w+)', infile)
  result = [year]
  namerankdict = {}
  for namerankmatch in namerankmatches:
    #result.append(namerankmatch[1] + " " + namerankmatch[0])
    #result.append(namerankmatch[2] + " " + namerankmatch[0])
    if namerankmatch[1] in namerankdict:
      if namerankmatch[0] < namerankdict[namerankmatch[1]]:
        namerankdict[namerankmatch[1]] = namerankmatch[0]
    else:
      namerankdict[namerankmatch[1]] = namerankmatch[0]
    if namerankmatch[2] in namerankdict:
      if namerankmatch[0] < namerankdict[namerankmatch[2]]:
        namerankdict[namerankmatch[2]] = namerankmatch[0]
    else:
      namerankdict[namerankmatch[2]] = namerankmatch[0]
  for name, rank in namerankdict.items():
    result.append(name + " " + str(rank))
  return sorted(result)

def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  while len(args):
    if (summary):
      summarydestination = args[0] +".summary"
      summaryfile = open(summarydestination, 'w')
      summaryfile.write('\n'.join(extract_names(args[0])) + '\n')
      summaryfile.close()
    else:
      print '\n'.join(extract_names(args[0])) + '\n'
    del args[0]
  
if __name__ == '__main__':
  main()
