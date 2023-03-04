#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
'''
@file py_terminal_logger.py
@author Brian BURNS
@author David BLACK @bballdave025
        
@since 2018-09-13

Allows logging of an interactive Python session

Taken from:
@ref: https://stackoverflow.com/a/41477104/6505499
then edited for my needs
# @author 'Brian Burns' (SO Username)

####################
### IMPORTANT!!! ###
Before this is used, one should run 
test_in_python_interpreter.is_in_interpreter()

If this returns `False`, this module should not be used.


# StackOverflow versiondocumentation 
Transcript - direct print output to a file, in addition to terminal.

Usage:
    import transcript
    transcript.start('logfile.log')
    print("inside file")
    transcript.stop()
    print("outside file")
'''

##-----------------
# IMPORT STATEMENTS
##-----------------
import sys

# Intra-Package
## For Python2
# from __future__ import absolute_import


##-------------------
# DATA MEMBERS/
#   GLOBAL VARIABLES
##-------------------


##-----------------
# CODE
##-----------------


class Py_terminal_logger(object):
  '''
  The Py_terminal_logger class object
  '''
  
  def __init__(self, filename):
    '''
    Constructor
    '''
    
    #@TODO: Check that we're in the interpreter. If not, exit or return.
    
    self.terminal = sys.stdout
    self.logfile = open(filename, "a")
    #try_to_chmod.run(filename)
    
  ##endof:  __init__(self, filename)
  
  def write(self, message):
    '''
    
    '''
    
    self.terminal.write(message)
    self.logfile.write(message)
  ##endof:  write(self, message)
  
  def flush(self):
    '''
    # this flush method is needed for python 3 compatibility.
    # this handles the flush command by doing nothing.
    # you might want to specify some extra behavior here.
    '''
    
    pass
    
  ##endof:  flush(self)

##endof:  class Py_terminal_logger(object) #Transcript(object)


def start(filename):
  '''
  Start transcript, appending print output to given filename
  '''
  
  #TODO: Check that we're in the interpreter, if not, exit.
  
  sys.stdout.write("Beginning interactive console logger.\n")
  sys.stdout.write("Output file is: " + filename + "\n\n")
  sys.stdout = Py_terminal_logger(filename)

##endof:  start(filename)


def stop():
  '''
  Stop transcript and return print functionality to normal
  '''
  
  #try_to_chmod.run(sys.stdout.logfile)
  sys.stdout.logfile.close()
  sys.stdout = sys.stdout.terminal

##endof:  stop()