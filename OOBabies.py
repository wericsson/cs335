#!/usr/bin/python

import re
import urllib
import urlparse
import sys

class BabyNames :
  def __init__(self, year):
    self.year = year
    self.namerankdict = {}
  
  def add_url(self, target):
    try:
      text = urllib.urlopen(target)
    except:
      print "Error opening ",
      print target
    else:
      if text.info().gettype() == 'text/html':
        ols = re.findall(r"<ol>.*?</ol>", text.read())
        for ol in ols:
          lis = re.findall(r"<li>.*?</li>", ol)
          rank = 0
          while rank <= len(lis):
            # Using the built in for/in construct would be tempting, but we
            # still need a counter anyway.
            match = re.search(r'<a.*?>(.*?)</a>', lis[rank])
            rank += 1
            if match.group(1) in self.namerankdict:
              self.namerankdict[match.group(1)] = min(self.namerankdict[match.group(1)],rank)
            else:
              self.namerankdict[match.group(1)] = rank
      text.close()
  
  def text(self):
    outtext = '\n\n' + str(self.year) + '\n\n'
    outlist = []
    for name, rank in self.namerankdict:
      outlist.append(name + " " + str(rank))
    for namerankstring in sorted(outlist):
      outtext += namerankstring
      outtext += '\n'
    return outtext
        

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] URL'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]
  
  Years = {}

  try:
    text = urllib.urlopen(args[0])
  except IOError:
    print "Error connecting to ",
    print args[0]
    raise
    # I mean, this is still fatal.
  else:
    if text.info().gettype() == 'text/html':
      uls = re.findall(r"\d+\sto\s\d+</h2><ul>.*?</ul>", text.read())
      for ul in uls:
        lis = re.findall(r"<li>.*?</li>", ul)
        for li in lis:
          match = re.search(r'href="(.*?)".*?(\d\d\d\d)</a>', li)
          Year = int(match.group(2))
          if Year in Years:
            Years[Year].add_url(urlparse.urlparse(args[0])[0] + "://" + urlparse.urlparse(args[0])[1] + match.group(1))
          else:
            Years[Year] = BabyNames(Year)
            Years[Year].add_url(urlparse.urlparse(args[0])[0] + "://" + urlparse.urlparse(args[0])[1] + match.group(1))
    text.close()
  isopen = False
  if summary:
    try:
      f = open('babysummary.txt', 'w')
    except:
      print "Error writing to babysummary.txt. Abort, Retry, and Fail, in any order you wish."
    else:
      isopen = True
  for Year in sorted(Years.keys()):
    if isopen:
      f.write(Years[Year].text())
    else:
      print Years[Year].text()
          
if __name__ == '__main__':
  main()