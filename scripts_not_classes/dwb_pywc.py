#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
'''
@file dwb_pywc.py
@author David BLACK  @bballdave025
@since 2024-05-20

@todo Give options for pure bash-like output
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
  
  Defaults to the `wc` method
  '''
  
  return wc(filename)
  
##endof:  main(filename)


def run(filename):
  '''
  Easy-to-remember entrance
  
  Defaults to the `wc` method
  '''
    
  return wc(filename)
  
##endof:  main(filename)


def wc(filename):
  '''
  Mimics part of the behavior of the `bash` command, `wc`.
  
  @param filename        A string representing the filename whose length
                         in lines, words, and characters will be given
  @return                A string with the lengths
  '''
  
  n_lines = 0
  n_words = 0
  n_chars = 0
  
  # @todo  Get all with open ready to use 'utf-8' as encoding and
  #        to use UnicodeDammit
  with open(filename, 'r') as f:
    for line in f:
      words = line.split()
      
      n_lines += 1
      n_words += len(words)
      n_chars += len(chars)
  
    ##endof:  for line in f
  
  ##endof for line in f
  
  print("n_lines: " + str(n_lines))
  print("n_words: " + str(n_words))
  print("n_chars: " + str(n_chars))
  
##endof:  wc(filename)


if __name__ == "__main__":
  '''
  Gets executed if the file is run as a script
  '''
  
  main(sys.argv[1])
  
##endof:  if __name__ == "__main__"
