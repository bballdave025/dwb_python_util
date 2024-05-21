#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
'''
@file dwb_pycat.py
@author David BLACK  @bballdave025
@since 2018-07-18
'''
##############################################################################

##-------------------
## IMPORT STATEMENTS
##-------------------
import os
import sys
import shutil

# Intra-Package
## For Python2
# from __future__ import absolute_import
import check_is_a_file

DEBUG_PYCAT = False
LET_THE_PYCAT_OUT = False

length_of_pre_text = 10

def main(*filenames):
  '''
  Allows an entrance for running as a command-line script
  
  Defaults to the `cat_output` method with no `line_length_max`
  (meaning there will be no word-wrap), and no prefix. The
  `line_length_max` and `prefix` may be passed in.
  
  @param filenames A tuple of strings representing filenames
  @RESULT Same as `cat_output`
  '''
  
  return run(*filenames)
  
##endof:  main(*filenames)


def run(*filenames):
  '''
  Easy-to-remember entrance.
  
  Defaults to the `cat_output` method with no `line_length_max`
  (meaning there will be no word-wrap), and no prefix. The
  `line_length_max` and `prefix` may be passed in.
  
  @param filenames A tuple of strings representing filenames
  @RESULT Same as `cat_output`
  '''
  
  return cat_output(*filenames, 
                    line_length_max = None, 
                    prefix = None,
                    create_new_file_with_concatenations = False,
                    new_filename = None)
  
##endof:  run(*filenames)


def cat(*filenames,
        create_new_file_with_concatenations = False,
        new_filename = None):
  '''
  Mimics the behavior of the `bash` command, `cat`.
  
  This takes all the files and concatenates them in the order
  that their filenames are passed in. Unlike the other cat methods
  in this module, there is no extra newline between files -
  the new file gets added wherever the previous file ended.
  
  @param filenames A variable-length tuple of strings representing filenames
                   which will be concatenated and outputted to stdout.
  @RESULT The text resulting from the concatenation of the files will be
          output to stdout.
  
  @TODO  incorporate the new creation of a new file
  
  '''
  
  for filename in filenames:
    with open(filename, 'r') as f:
      shutil.copyfileobj(f, sys.stdout)
    ##endof:  with open
    
    ##sys.stdout.write("\n")
    
  ##endof:  for filename in filenames
  
##endof:  cat_standard(*filenames)


def cat_output(*filenames, 
               line_length_max = None, 
               prefix = None,
               create_new_file_with_concatenations = False,
               new_filename = None):
  '''
  Output the contents of a file (or files) to stdout with formatting options
  
  Adds an extra newline between files and at the end.
  
  Word wrapping is implemented through the optional `line_length_max`
  parameter. A newline will be inserted after the a space after the
  last complete word before the specified length. E.g. With original
  file contents
    He is going to go to the game and he is going to see the athletes play.
  and `line_length_max` of 10, the method would be implemented as follows
  
  first space
  before position           10 chars after
  10 `-_     position 10    second split          etc.
        \    |               / (it's a space)
         ^   X     X        ^         X        X     X         X      X
    He is going to go to the game and he is going to see the athletes play.
        (^)       ^|       (^)       ^     ^        ^       ^        ^     ^
    first space _/ |
    before the_/   10 characters aftter                   
    second 10      the first split
  
  with the following result
  and `line_length_max` as 10, the result would be
  
    He is 
    going to 
    go to the 
    game and 
    he is 
    going to 
    see the 
    athletes 
    play.
  
  Details:
  
    1         10
   |^         ^
   |He is     |
   |going to  |
   |go to the |
   |game and  |
   |he is     |
   |going to  |
   |see the   |
   |athletes  |
   |play.     |
  
  @todo The situation in which a word is longer than the `line_length_max`
        is not handled. I'll need to decide how to handle it and implement it
  
  The prefix will be handled as follows. If the prefix string is (==) "HYP" 
  and
      ... not sure where I was going here, mostly because I'm not taking the
          time to look at it today. -DWB 20200227
  
  
  @param filenames A tuple of strings representing filenames whose associated
                   files will be concatenated.
  @RESULT The word-wrapped version of the filename # WORD WRAP ABANDONED
                                                   # FOR A BIT
  
  @TODO  incorporate the new creation of a new file
  '''
  
  for filename in filenames:
    if not check_is_a_file.run(filename):
      sys.stderr.write("\n" + str(filename))
      sys.stderr.write("\ndoes not represent a file, therefore its")
      sys.stderr.write("\ntext content will not be shown.")
      sys.stderr.write("\nHowever, the program should be able to")
      sys.stderr.write("\ncontinue without problem.\n")
      return "__DWB_PYCAT_FAILURE_NOT_A_FILE_DWB__"
    ##endof:  if not check_is_a_file.run(filename)
    
    if os.path.isdir(filename):
      sys.stderr.write("\n" + str(filename))
      sys.stderr.write("\nrepresents a directory, therefore its")
      sys.stderr.write("\ntext content will not be shown.")
      sys.stderr.write("\nHowever, the program should be able to")
      sys.stderr.write("\ncontinue without problem.\n")
      return "__DWB_PYCAT_FAILURE_IS_A_DIRECTORY_DWB__"
    ##endof:  if os.path.isdir(filename)
    
    if line_length_max == None and prefix == None:
      with open(filename, 'r') as f:
        shutil.copyfileobj(f, sys.stdout)
      ##endof:  with open
      sys.stdout.write("\n")
    elif line_length_max == None and (not prefix == None):
      output_file_with_prefix(filename, prefix)
    elif not line_length_max == None:
      lines = output_file_with_word_wrap(filename, line_length_max, prefix)
      lines_to_stdout(lines, prefix)
    else:
      sys.stderr.write("Shouldn't get here in dwb_pycat.py")
    ##endof:  if/else
  ##endof:  for filename in filenames

##endof:  cat_output(filename)


def output_file_with_prefix(filename, prefix):
  '''
  Has standard, `bash` `cat` behavior, but with one prefix and an ending '\n'
  
  @param filename The filename whose contents will be output
  @param prefix A string representing a prefix.
  @RESULT the contents of the file with the prefix before and an extra
          newline after.
  '''
  
  sys.stdout.write(prefix + ":  ")
  
  with open(filename, 'r') as f:
    shutil.copyfileobj(f, sys.stdout)
  ##endof:  with
  
  # if LET_THE_PYCAT_OUT:
    # sys.stdout.write("\n")
  # ##endof:  if LET_THE_PYCAT_OUT
  
##endof:  output_file_with_prefix()


def output_file_with_word_wrap(filename, line_max, prefix = None):
  '''
  Takes a file and outputs it with specified word wrap and optional prefix
  
  The word-wrapped lines are put one at a time int an array of strings. There
  is also an optional prefix  
  
  This has been abandoned for a bit.
  '''
  
  lines = None
  
  with open(filename, 'r') as f:
    total_str = f.read()
    lines = output_str_with_word_wrap(total_str, line_max, prefix)
  ##endof:  with open(filename, 'r') as f
  
  return lines
  
##endof:  output_file_with_word_wrap()


def lines_to_stdout(lines, prefix = None):
  '''
  Send an array of text lines to stdout
  '''
  
  line_counter = 0
  for line in lines:
    line_counter += 1
    if not prefix == None:
      if line_counter == 1:
        # make a uniformly-long prefix before file contents come
        prefix_to_use = prefix
        length_colon = 1
        while (len(prefix_to_use) < length_of_pre_text - length_colon):
          prefix_to_use += "_"
        ##endof:  while
        sys.stdout.write(prefix_to_use + ":  " + line + "\n")
      else:
        # make a uniformly-long prefix before file contents come
        prefix_to_use = prefix
        length_colon = 1
        length_gt_intro = 3 # ">> "
        while (len(prefix_to_use) < length_of_pre_text - 
                                     length_colon - length_gt_intro): 
          sys.stdout.write(">> " + prefix_to_use + ":  " + line + "\n")
      ##endof:  if/else line_counter == 1
    ##endof:  if not prefix == None
    else:
      sys.stdout.write(line)
    ##endof:  if/else not prefix == None
  ##endof:  for line in lines
  
##endof:  lines_to_stdout


def output_str_with_word_wrap(total_string, line_max, prefix = None):
  '''
  Output the string with word wrapping.
  
  Set aside for a while. Too many problems that I didn't have time to solve
  '''
  
  ##it had better be on one line ## Never mind, I think I fixed that
  #current_working_str = ' '.join(total_string.split())
  
  if DEBUG_PYCAT:
    sys.stdout.write("\n")
    sys.stdout.write("complete string:\n" + \
                     total_string)
    sys.stdout.write("\n")
  ##endof:  if DEBUG_PYCAT
  
  lines = []
  current_index = 0
  current_working_str = total_string
  
  while ( len(current_working_str) > line_max ):
    current_index *= 0
    
    str_with_line_max_chars = current_working_str[:line_max]
    
    if DEBUG_PYCAT:
      sys.stdout.write("\n")
      sys.stdout.write("before trimming:\n" + \
                       str_with_line_max_chars)
      sys.stdout.write("\n")
    ##endof:  if DEBUG_PYCAT
    
    #chars_not_used = []
    
    added_line = str_with_line_max_chars
    
    if '\n' in added_line:
      added_line = added_line.split('\n')[0] + "\n"
    else:
      while not added_line[-1].isspace():
        #chars_not_used.append(added_line[-1])
        added_line = added_line[:-1]
      ##endof:  while not
    ##endof:  if/else
    
    lines.append(added_line)
    
    #current_index = line_max - len(chars_not_used)
    current_index = len(added_line)
    current_working_str = current_working_str[current_index:]
    
    if DEBUG_PYCAT:
      sys.stdout.write("\n")
      sys.stdout.write("after trimming...\n" + \
                       "lines: \n" + str(lines) + "\n" + \
                       "remaining string:\n" + \
                       current_working_str)
      sys.stdout.write("\n")
      
      #input("Press [Enter] to continue.")
    ##endof:  if DEBUG_PYCAT
      
  ##endof:  while len(current_working_str) > line_max
  
  while '\n' in current_working_str[:-1]:
    added_line = current_working_str.split('\n')[0] + "\n"
    lines.append(added_line)
    current_working_str = current_working_str[len(added_line):]
    if DEBUG_PYCAT:
      sys.stdout.write("\n")
      sys.stdout.write("after trimming...\n" + \
                       "lines: \n" + str(lines) + "\n" + \
                       "remaining string:\n" + \
                       current_working_str)
      sys.stdout.write("\n")
      
      #input("Press [Enter] to continue.")
    ##endof:  if DEBUG_PYCAT
  ##endof:  while '\n' in current_working_str[:-1]
  
  if not current_working_str == '':  
    lines.append(current_working_str + "\n")
  
  return lines
  
##endof:  output_with_word_wrap(total_string, line_max)


def cat_and_outfile(out_filename, *in_filenames):
  '''
  Takes all of the infilenames in order and joins them together.
  The output is written to outfilename
  Adds an extra newline between files and at the end.
  '''
  
  with open(out_filename, 'w') as ofh:
    for filename in in_filenames:
      with open(filename) as ifh:
        for line in ifh:
          ofh.write(line)
        ##endof:  for line in ifh
      ##endof with open(filename) as ifh
      
      ofh.write("\n")
      
    ##endof:  for filename in in_filenames
  ##endof:  with open(out_filename, 'w') as ofh

##endof:  cat_concatenate_and_outfile(out_filename, *in_filenames)


if __name__ == "__main__":
  '''
  Gets executed if the file is run as a script
  '''
  
  main(sys.argv[1:])

##endof:  if __name__ == "__main__"
