#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
'''
@file dwb_pyhead.py
@author David BLACK  @bballdave025
@since 2024-05-20
'''
##############################################################################

##-------------------
## IMPORT STATEMENTS
##-------------------

# Intra-Package
## For Python2
# from __future__ import absolute_import

def main(n_lines, filename):
  '''
  Allows an entrance for running as a command-line script
  
  Defaults to the `head` method
  '''
  
  return grep(n_lines, filename)
  
##endof:  main(n_lines, filename)


def run(n_lines, filename):
  '''
  Easy-to-remember entrance
  
  Defaults to the `head` method
  '''
  
  return head(n_lines, filename)
  
##endof:  main(n_lines, filename)


def head(n_lines, filename):
  '''
  Mimics part of the behavior of the `bash` command, `head`.
  
  @param n_lines         The number of lines. It will be the  n_lines
                         first lines.
  @param filename        A string representing the filename whose first lines
                         will be found.
  @result                A string representing the first  n_lines  lines of
                         the file represented by  filename  will print out.
  '''

  # @todo  For all  with open , allow 'utf-8' encoding, and use UnicodeDammit
  with open(filename, 'r') as ifh:
    for i in range(n_lines):
      #  getting rid of the linefeed character at the end.
      #+ it also gets rid of any trailing whitespace, which
      #+ is probably not what I want to do
      # @todo  Only take off the trailing linefeed
      this_line = next(ifh).rstrip()
      print(this_line)
  ##endof:  with open ... ifh # Input File Handle
##endof:  head(n_lines, filename)


if __name__ == "__main__":
  '''
  Gets executed if the file is run as a script
  '''
  
  main(sys.argv[1:2])
  
##endof:  if __name__ == "__main__"
