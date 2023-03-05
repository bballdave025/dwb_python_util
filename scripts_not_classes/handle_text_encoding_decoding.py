#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
'''
@brief 
@file handle_encoding_decoding.py
@author David BLACK  @bballdave025
@since 2018-07-03
       2020-03-26, moved to its own module

'''
#https://github.com/ahupp/python-magic#dependencies
#https://stackoverflow.com/q/18374103/6505499
#https://pypi.org/project/python-magic-bin/0.4.14/
##############################################################################

##-----------------
# IMPORT STATEMENTS
##-----------------
import os
import sys
import traceback

from bs4 import UnicodeDammit



import agp
import check_is_a_file


##------------------------------
## FUNCTIONS
##------------------------------

def main(input_param, outfile_dir=None):
  '''
  @brief A to-be-written entry value for command-line use
  
  @TODO: write this according to the specifications I've given here.
          -DWB 20180807
  
  @param input_param A string which will either represent a file containing
                     the transcript or represent the string on which 
                     essential parsing is desired
                     ## For now, a filename ##
  @RESULT/return Either the modified transcript string or an output file
                 containing the modified transcript string
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "ep.main ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  #essentially_parsed_str = parse_file(input_param)
  #write_out_processed_file(filename_str, essentially_parsed_str, 
  #                         outfile_dir=None)
  
  run(input_param)
  
  #pass
  ##@TODO:
  #@todo
  #if test_is_file(input_param):
    #parse_file(input_param)
  #elif test_is_str(input_param):
    #parse_string(input_param)
  #else:
    #give_some_warning
    #parse_string(str(input_param))
  ##endof:  if/elif/else

##endof:  main(input_param)


def run(input_param, outfile_dir=None):
  '''
  @brief An easy-to-access method name which allows parsing of a file
  
  IMPORTANT! For now, this method expects a filename string
  
  @TODO: perhaps this will do automatic detection of whether the input
         parameter be a string representing a file or simply a string
         that needs to be parsed.
  
  @param filename_str A string representing the filename
  @RESULT A file which will contain the raw-format version of the transcript
          in the original file
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "ep.run ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  # essentially_parsed_str = parse_file(filename_str)
  # write_out_processed_file(filename_str, essentially_parsed_str,
                           # outfile_dir)
  
  
  input_filename_or_string = input_param
  return do_the_encdec_swear(input_filename_or_string)
  
##endof:  run(filename_str)


def do_the_encdec_swear(input_filename_or_string):
  '''
  @brief Gets a string representing the file content.
  method, for details on what "raw format" means
  
  @param filename_str  The string representing the filename
  @return              A string (repeat, A STRING) which is encoded in UTF-8
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "endec.parse_file ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  bunches_verbosity_stuff = False
  
  # if (bunches_verbosity_stuff):
    
    # sys.stdout.write("\n\n")
    # sys.stdout.write("\n\n###############################\n")
    # sys.stdout.write    ("# BEGINNING ESSENTIAL PARSING #\n")
    # sys.stdout.write    ("###############################\n")
    # sys.stdout.write("\n")    
    
  # ##endof:  if <verbosity and debug>
  
  getting_fixed_output_str = ''
  
  #try_to_chmod.run(filename_str)
  
  
  try:
    getting_fixed_output_str = do_the_swear(input_filename_or_string)
  except Exception as e:
    sys.stderr.write("\n\nSomething went wrong. The exception string is:\n")
    sys.stderr.write((str(e)))
    traceback.print_exc()
    sys.stderr.write("\n\n")
  finally:
    pass
  ##endof:  try/except/finally
  
  # try:
    # with open(filename_str, 'r', encoding='utf-8') as ifh:
      # getting_fixed_output_str = ifh.read()
    # ##endof:  with open(filename_str, 'r') as ifh
  # except UnicodeDecodeError as ude:
    # #if agp.DO_ALERT_NON_UTF8:
    # DO_ALERT_NON_UTF8 = True
    # if DO_ALERT_NON_UTF8:
      # sys.stdout.write("\nNon-UTF-8 encoding. Time to swear!\n")
    # ##endof:  if agp.DO_ALERT_NON_UTF8
    # getting_fixed_output_str = do_the_swear(filename_str)
  # finally:
    # pass
  # ##endof:  try/except/finally
  
  processing = getting_fixed_output_str
  
  other_verbosity_stuff = False
  if other_verbosity_stuff:
    sys.stdout.write("\n\n\nStraight from file:\n" + processing + "\n")
  
  #str_to_return = parse_string(processing)
  
  if other_verbosity_stuff:
    sys.stdout.write("\n")
  ##endof:  if <verbosity>
  
  return str_to_return
  
##endof:  parse_file(filename_str)


def do_the_swear(filename_or_regular_str):
  '''
  Run the UnicodeDammit stuff from Beautiful Soup 4 to get unicode
  (officially, the utf-8 encoded string using Unicode)
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "ep.do_the_swear ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  data = ''
  
  if not check_is_a_file.run(filename_or_regular_str):
    ## The path/filename given doesn't point to a valid
    ## file. We'll treat it as string input.
    data = filename_or_regular_str
  else:
    with open(filename_or_regular_str, 'rb') as data_fh:
      data = data_fh.read()
    ##endof:  with open ... data_fh
  ##endof:  if/else not check_is_a_file(filename_or_regular_str)
  
  swear_object = UnicodeDammit(data)
  swear_string = str(swear_object.unicode_markup)
  
  ## For what seems to be input from Microsoft Office stuff,
  ## where real Unicode is mixed up with another encoding
  ## (often cp1252, aka the Windows abomination)
  less_swear_str = re.sub(r"\x85\x20", " ... ",
                          swear_string)
  less_swear_str = re.sub(r"\x85", " ... ",
                          less_swear_str)
  
  less_swear_str = re.sub(r"\x92\x20", "' ",
                          less_swear_str)
  less_swear_str = re.sub(r"\x92", "'",
                          less_swear_str)
  less_swear_str = re.sub(r"\x20\x91", " '",
                          less_swear_str)
  less_swear_str = re.sub(r"\x91", "'",
                          less_swear_str)
  less_swear_str = re.sub(r"\x20\x93", ' " ',
                          less_swear_str)
  less_swear_str = re.sub(r"\x93", ' " ',
                          less_swear_str)
  less_swear_str = re.sub(r"\x94\x20", ' " ',
                          less_swear_str)
  less_swear_str = re.sub(r"\x94", ' " ',
                          less_swear_str)
  
  less_swear_str = re.sub(r"\x20\x80", " EUR ",
                          less_swear_str)
  less_swear_str = re.sub(r"\x80\x20", " EUR ",
                          less_swear_str)
  less_swear_str = re.sub(r"\x80", " EUR ",
                          less_swear_str)
  
  less_swear_str = re.sub(r"\x20\x8a", " S",
                          less_swear_str,
                          flags=re.IGNORECASE)
  less_swear_str = re.sub(r"\x8a", "S",
                          less_swear_str,
                          flags=re.IGNORECASE)
  less_swear_str = re.sub(r"\x9a", "s",
                          less_swear_str,
                          flags=re.IGNORECASE)
  
  less_swear_str = re.sub(r"\x20\x8b", " < ",
                          less_swear_str,
                          flags=re.IGNORECASE)
  less_swear_str = re.sub(r"\x8b", " < ",
                          less_swear_str,
                          flags=re.IGNORECASE)
  less_swear_str = re.sub(r"\x9b\x20", " > ",
                          less_swear_str,
                          flags=re.IGNORECASE)
  less_swear_str = re.sub(r"\x9b", " > ",
                          less_swear_str,
                          flags=re.IGNORECASE)
  
  less_swear_str = re.sub(r"\x20\x8c", " OE",
                          less_swear_str,
                          flags=re.IGNORECASE)
  less_swear_str = re.sub(r"\x8c", "OE",
                          less_swear_str,
                          flags=re.IGNORECASE)
  less_swear_str = re.sub(r"\x9c", "oe",
                          less_swear_str,
                          flags=re.IGNORECASE)
  
  less_swear_str = re.sub(r"\x20\x8e", " Z",
                          less_swear_str,
                          flags=re.IGNORECASE)
  less_swear_str = re.sub(r"\x8e", "Z",
                          less_swear_str,
                          flags=re.IGNORECASE)
  less_swear_str = re.sub(r"\x9e", "z",
                          less_swear_str,
                          flags=re.IGNORECASE)
  
  less_swear_str = re.sub(r"\x20\x9f", " Y",
                          less_swear_str,
                          flags=re.IGNORECASE)
  less_swear_str = re.sub(r"\x9f", "Y",
                          less_swear_str,
                          flags=re.IGNORECASE)
  
  less_swear_str = re.sub(r"\x95", " . ",
                          less_swear_str)
  
  less_swear_str = re.sub(r"\x96", " - ",
                          less_swear_str)
  less_swear_str = re.sub(r"\x97", " - ",
                          less_swear_str)
  
  less_swear_str = re.sub(r"\x99", " TM ",
                          less_swear_str)
  
  # less_swear_str = re.sub(r"\x8c", "'",
                          # less_swear_str,
                          # flags=re.IGNORECASE)
  # less_swear_str = re.sub(r"\x8c", "'",
                          # less_swear_str,
                          # flags=re.IGNORECASE)
  
  return less_swear_str
  
##endof:  do_the_swear(filename_or_regular_str)
