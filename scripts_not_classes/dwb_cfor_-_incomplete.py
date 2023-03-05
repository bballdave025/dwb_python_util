#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
'''
@file dwb_cfor.py
@author David BLACK  @bballdave025

@since 2020-02-26

Simulates the C-style for loop. Credit goes to

@ref https://stackoverflow.com/q/2740901/6505499
@ref https://stackoverflow.com/a/2741943/6505499

Basically, we're using tests instead of an iterator. It just bugged me that
I couldn't do it on Python. Specifically, I'm writing it for the convert-
to-a-percentage-and-round-to-the-parameter's-number-of-digits-after-the-
decimal-marker method test.

Actually, Python doesn't have a proper for loop, it only has foreach loops.
https://en.wikipedia.org/wiki/For_loop#1972:_C/C++


An example use (actually a test) from the interactive console

 >>> from acuss.acuss_utils.dwb_cfor import cfor as cfor
 >>> max_val_plus_one = 4
 >>> this_array = []
 >>> for i in cfor(0, lambda i:i < max_val_plus_one, lambda i:i + 1):
 ...   this_array.append(i)
 ... ##endof:  for
 ...
 >>> print(str(this_array))
 [0, 1, 2, 3]
 >>>

'''
##############################################################################

##-------------------
## IMPORT STATEMENTS
##-------------------
from __future__ import absolute_import

# Intra-Package
## For Python2 ... but no error on Python3...
#from __future__ import absolute_import

##-------------------
## METHODS
##-------------------

def main(initial_value, break_out_test_func, change_func):
  '''
  Provide a command-line interface to the cfor functionality
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "cfor.main ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  run(initial_value, break_out_test_func, change_func)
  
##endof:  main()


def run(initial_value, break_out_test_func, change_func):
  '''
  Provide an easy-to-remember entrance to the cfor functionality
  
  Example use:
  >>> max_val_plus_one = 4
  >>> this_array = []
  >>> for i in project.stuff.dwb_cfor.run(0, 
                                      lambda i:i < max_val_plus_one,
                                      lambda i:i + 1):
        this_array.append(i)
      ##endof:  for i in cfor
  >>> print(str(this_array))
  
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "cfor.run ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  cfor(initial_value, break_out_test_func, change_func)
  
##endof:  main()


def cfor(initial_value, break_out_test_func, change_func):
  '''
  Provide a c-type loop functionality, based on tests rather than iterators
  
  Example use:
  >>> max_val_plus_one = 4
  >>> this_array = []
  >>> for i in project.stuff.dwb_cfor.cfor(0, 
                                      lambda i:i < max_val_plus_one,
                                      lambda i:i + 1):
        this_array.append(i)
      ##endof:  for i in cfor
  >>> print(str(this_array))
  
  @param  initial value        :  the starting value yielded by the loop
  @param  break_out_test_func  :  a lambda function which returns a
                                  boolean value - False when the test means
                                  we break out of the loop 
  @param  change_func          :  a lambda function that makes the change
                                  moving us closer toward the break-out
                                  condition (unless you want an infinite 
                                  loop)
  
  @returns  values as per the initial and change stuff until we get to the
            break-out stuff
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "cfor.cfor ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  # debug_this = (agp.DEBUG_C_STYLE_FOR or
                # agp.ACUSS_VERBOSITY.value > agp.Verbosity.HIGH.value)
  # Before part of the important, non-comment, non-previous-try, non-debug
  # lines, you'll see `#--------------------------------------`
  
  
  debug_this = False
  
  if debug_this:
    print()
    print("Debugging the C-style for loop, `cfor`.")
  ##endof:  if debug_this
  
  # #DIDN'T WORK# better_name_for_current_value = initial_value
  
  if debug_this:
    print()
    print("Point (0) initial_value: ", str(initial_value))
    # #DIDN'T WORK# print("better_name_for_current_value:", 
          # #DIDN'T WORK# str(better_name_for_current_value))
    print("break_out_test_func(initial_value)",
          str(break_out_test_func(initial_value)))
    print()
  ##endof:  if debug_this
  
  # #DIDN'T WORK# while break_out_test_func(better_name_for_current_value):
  
  #----------------------------------------
  while break_out_test_func(initial_value):
    if debug_this:
      print("Inside while")
    ##endof:  if debug_this
    
    # #DIDN'T WORK# print("better_name_for_current_value:", 
          # #DIDN'T WORK# str(better_name_for_current_value))
    # #DIDN'T WORK# yield better_name_for_current_value
    
    if debug_this:
      print("Point (1) initial_value: ", str(initial_value))
    ##endof:  if debug_this
    
    #------------------
    yield initial_value
    
    if debug_this:
      print()
      print("Point (a), initial_value: " + str(initial_value))
    ##endof:  if debug_this
    
    #-----------------------------------------
    initial_value = change_func(initial_value)
    
    if debug_this:
      print("Point (b), initial_value: " + str(initial_value))
      print()
      print("break_out_test_func(initial_value)",
            str(break_out_test_func(initial_value)))
      print()
      print()
    ##endof:  if debug_this
  ##endof:  while test_func(curr_val)
  
  if debug_this:
    print("Out of while")
    print()
  ##endof:  
  
##endof:  cfor()


if __name__ == "__main__": # Gets executed if the file is run as a script
  '''
  Takes all the command line arguments and dumps them as parameters to the
  main() method, implemented at the top of this Python file.
  '''
  
  # if agp.DEBUG_METHOD_ENTRANCE:
    # sys.stdout.write("\nYOU ARE ENTERING " + \
                     # "cfor from the command line ." + \
                     # "WELCOME\n")
  # ##endof:  if
  
  main(sys.argv[1:4])

##endof:  if __name__ == "__main__"
