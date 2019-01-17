#!/usr/bin/python

import sys

def mult(x,y):
  print(str(x*y))
  
def main():
  mult(int(sys.argv[1]),int(sys.argv[2]))

if __name__ == "__main__":
  main()