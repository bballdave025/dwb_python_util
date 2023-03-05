#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
'''
@file dwb_pygrep.py
@author David BLACK  @bballdave025
@since 2018-09-04

@todo Perhaps extend this to use the re package
'''
##############################################################################

##-------------------
## IMPORT STATEMENTS
##-------------------
import os
import sys
import re

# Intra-Package
## For Python2
# from __future__ import absolute_import

def main(string_to_find, filename):
  '''
  Allows an entrance for running as a command-line script
  
  Defaults to the `grep` method
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "pygrep.main ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  return grep(string_to_find, filename)
  
##endof:  main(filename)


def run(string_to_find, filename):
  '''
  Easy-to-remember entrance
  
  Defaults to the `grep` method
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "pygrep.run ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  return grep(string_to_find, filename)
  
##endof:  main(filename)


def grep(string_to_find, filename):
  '''
  Mimics part of the behavior of the `bash` command, `grep`.
  
  This only allows one to search for one string in one file. It might
  be nice at a later time to extend this to search using the re module
  (regex)
  
  @param string_to_find  A string for which the file will be searched,
                         the searching being done line-by-line
  @param filename        A string representing the filename whose contents
                         will be searched
  @return                A string representing the line (or sequence of
                         lines) in the file which contain `string_to_find`
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "pygrep.grep ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  the_result_str = ''
  
  with open(filename, 'r') as f:
    lines = f.readlines()
    for line in lines:
      #if string_to_find in line:
      if re.match(string_to_find, line):
        the_result_str += line + "\n"
      ##endof:  if string_to_find in line
    ##endof:  for line in lines
  ##endof:  with open
  
  return the_result_str
  
##endof:  grep(string_to_find, filename)


if __name__ == "__main__":
  '''
  Gets executed if the file is run as a script
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "pygrep from the command line ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  #main(sys.argv[1])
  main(sys.argv[1:3])

##endof:  if __name__ == "__main__"
