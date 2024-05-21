#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
'''
@file check_is_a_file.py
@author David BLACK  @bballdave025
@since 2018-08-03 (idea noted possibly as early as 2018-07-03)

'''
##############################################################################

##-------------------
## IMPORT STATEMENTS
##-------------------
import os
import sys

# Intra-Package
## For Python2
# from __future__ import absolute_import


def main(possible_filename_str, do_verbosity=True, is_initial=False):
  '''
  Provides an easy command-line entrance to the file detection
  '''
  
  return run(possible_filename_str, do_verbosity, is_initial)
  
##endof:  main(filename)


def run(possible_filename_str, do_verbosity=True, is_initial=False):
  '''
  Provides an easy-to-remember method name for file detection
  '''
  
  return check_is_a_file(possible_filename_str, do_verbosity, is_initial)
  
##endof:  run(filename)


def check_is_a_file(possible_filename_str, 
                    do_verbosity=True, 
                    is_initial=False):
  '''
  Returns a boolean showing whether the string is a filename for a real file
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "ciaf.check_is_a_file ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  check_str = possible_filename_str
  
  str_represents_a_file = False # Guilty until proven innocent
  
  # ## might do a check, try/catch with this
  # #check_str = os.path.abspath(check_str)
  
  try:
    if os.stat(check_str).st_size > 0:
      str_represents_a_file = True
    else:
      warn_str = "\nWARNING! File\n  " + check_str + "\nis empty.\n"
      if do_verbosity:
        if not is_initial:
          sys.stdout.write(warn_str)
        ##endof:  if not is_initial
      ##endof:  if do_verbosity
      str_represents_a_file = True
    ##endof:  if os.stat(check_str).st_size > 0
  except OSError as ose:
    warn_str = "WARNING!\nFile\n  " + check_str + \
               "\ndoesn't exist or is inaccessible ... " + \
               "check permissions.\n"
    warn_str += "\nThe OSError was:\n" + str(ose) + "\n"
    warn_str += "\nIt is possible that we can interpret the input,\n" + \
                check_str + "\n , as a string."
    warn_str += "\nThat is likely the way that the program " + \
                "will continue.\n"
    if do_verbosity:
      if not is_initial:
        sys.stdout.write(warn_str)
      ##endof:  if not is_initial
    else:
      pass
    ##endof:  if/else do_verbosity
    
    #str_represents_a_file = False
                      
  except FileNotFoundError as fnfe:
    if do_verbosity:
      warn_str = "\WARNING!\nThere was no file named\n  " + check_str + \
      "\nfound.\nIt's very likely that a string was passed in." + \
      "\nThat is likely the way that the program will continue.\n"
    
      sys.stdout.write(warn_str)
      
    else:
      pass
    ##endof:  if/else do_verbosity
    
    #str_represents_a_file = False
                      
  finally:
    pass
    
  ##endof:  try/except/finally
  
  return str_represents_a_file
  
##endof:  check_is_a_file(filename)


if __name__ == "__main__":
  '''
  Gets executed if the file is run as a script
  '''
  
  main(sys.argv[1])

##endof:  if __name__ == "__main__"
