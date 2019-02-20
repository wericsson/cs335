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
    except IOError:
      print "Error opening ",
      print target
    else:
      if text.info().gettype() == 'text/html':
        pagetext = text.read()
        ols = re.findall(r"<ol.*?>.*?</ol>", pagetext)
        if len(ols) == 0:
          print "Found no ordered lists at " + target
          errf = open('dump.txt','w')
          errf.write(pagetext)
          errf.close
        for ol in ols:
          lis = re.findall(r"<li>.*?</li>", ol)
          rank = 1
          while rank <= len(lis):
            # Using the built in for/in construct would be tempting, but we
            # still need a counter anyway.
            try:
              match = re.search(r'>\s*(\w+?)\s*<', lis[rank-1])
              if match.group(1) in self.namerankdict:
                self.namerankdict[match.group(1)] = min(self.namerankdict[match.group(1)],rank)
              else:
                self.namerankdict[match.group(1)] = rank
            except:
              print "Error extracting name from the following:",
              print lis[rank-1]
            rank += 1
      else:
        print "Not HTML?"
      text.close()
  
  def text(self):
    outtext = str(self.year) + '\n\n'
    outlist = []
    for name, rank in self.namerankdict.items():
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
  
  # dict matching years with corresponding BabyNames objects
  Years = {}

  try:
    text = urllib.urlopen(args[0])
  except IOError:
    print "Error connecting to ",
    print args[0]
    raise IOError
    # I mean, this is still fatal.
  else:
    if text.info().gettype() == 'text/html':
      uls = re.findall(r"\d+\sto\s\d+</h2><ul>.*?</ul>", text.read())
      print "len(uls) = " + str(len(uls))
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
  if summary:
    try:
      f = open('babysummary.txt', 'w')
    except:
      print "Error writing to babysummary.txt. Abort, Retry, and Fail, in any order you wish."
    else:
      for Year in sorted(Years.keys()):
        f.write(Years[Year].text())
        f.write('\n\n')
      f.close()
  else:
    for Year in sorted(Years.keys()):
      print Years[Year].text()
          
if __name__ == '__main__':
  main()