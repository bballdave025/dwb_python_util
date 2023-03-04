#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
##############################################################################
# @file   TeeTerminalLogger.py
# @author David BLACK   @bballdave025
# @since  2023-02-27
#
# @ref_1        r1="https://stackoverflow.com/q/8053900/6505499"
# @ref_2        r2="https://stackoverflow.com/a/8054244/6505499"
# @archived_ref ar="https://web.archive.org/web/20230303221645/" + \
#+                 "https://stackoverflow.com/questions/8053900/" + \
#+                 "how-to-log-everything-that-occurs-in-a-" + \
#+                 "python-interactive-shell-session"
#+  (Yes, it does work for both ref_1 and ref_2)
#
#  Keeps a logfile of the current interactive python terminal (what is given
#+ given to `>>>` and what results). 
# 
# Also useful for timestamps are
# @ref_3           r3  = "https://strftime.org/"
# @archived_ref_3  ar3 = "https://web.archive.org/web/20230211151652/" + \
#+                       "https://strftime.org/"
# @ref_4           r4  = "https://www.programiz.com/python-programming/" + \
                         "datetime/strftime"
# @archived_ref_4  ar4 = "https://web.archive.org/web/20230303224913/" + \
                         "https://www.programiz.com/python-programming/" + \
                         "datetime/strftime"
##############################################################################

import code
import sys

class TeeTerminalLogger(object):
  '''
  The object called to begin logging the console I/O
  
  [no parameters]
  @result  A logfile with the name formatted as given in the instantiation
  
  @usage  >>> sys.stdout = sys.stderr = sys.stdin = \
          ...   TeeTerminalLogger(<filename>, <write-mode)
          # Note that you can use any combination
          # {sys.stdout, sys.stderr, sys.stdin} (one, two, or 3 of them)
          # I'll give two examples.
          #  1) A log that continues to get data each time the
          #+    call is made.
          #+ >>> import TeeTerminalLogger
          #+ >>> sys.stdout = sys.stderr = sys.stdin = \
          #+ ...   TeeTerminalLogger(consolelog.log, 'w')
          #+ # (Same call each time. You must make sure that
          #+ #  `consolelog.log` exists before calling.)
          #  2) A log with only the information from one
          #+   session.
          #+ >>> import datetime
          #+ >>> import strftime
          #+ >>> import TeeTerminalLogger
          #+ >>> sys.stdout = sys.stderr = sys.stdin = \
          #+ ...   
          #
          #
          # NOTE THAT YOU MUST BE IN INTERACTIVE MODE!
          #+ (Wait, maybe not for this one.
          #+  @TODO  test in )
  '''
  
  def __init__(self, log_fname, mode='a'):
    try:
      self.log = open(log_fname, mode)
  
##endof:  class TeeTerinalLogger(object)