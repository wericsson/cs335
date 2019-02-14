#!/usr/bin/python

import re
import urllib
import urlparse
import sys

class BabyNames :
  def __init__(self, year):
    self.year = year
  
  def add_url(self, target):
    try:
      text = urllib.urlopen(target)
    except:
      print "Error opening ",
      print target
    else:
      if text.info().gettype() == 'text/html':
        print None

def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] URL'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  try:
    text = urllib.urlopen(args[0])
  except:
    print "Error connecting to ",
    print args[0]
  else:
    if text.info().gettype() == 'text/html':
      uls = re.findall(r"\d+\sto\s\d+</h2><ul>.*?</ul>", text.read())
      for ul in uls:
        lis = re.findall(r"<li>.*?</li>", ul)
        for li in lis:
          match = re.search(r'href="(.*?)".*?(\d\d\d\d)</a>', li)
          thisYear = BabyNames(match.group(2))
          thisYear.add_url(urlparse.urlparse(args[0])[0] + "://" + urlparse.urlparse(args[0])[1] + match.group(1))
          print urlparse.urlparse(args[0])[0] + "://" + urlparse.urlparse(args[0])[1] + match.group(1)
          

if __name__ == '__main__':
  main()