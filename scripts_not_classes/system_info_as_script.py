#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#########################################################################
'''
@file: system_info_as_script.py
@editor:  David Wallace BLACK (GitHub @bballdave025)
@authors: Main one: Stack Overflow: @24_saurabh_sharma
Other StackOverflow Users from
@archived_ref = "https://web.archive.org/web/20240529202404/" + \
                "https://stackoverflow.com/questions/3103178/" + \
                "how-to-get-the-system-info-with-python"

Further edits, info, thoughts to come from David BLACK
@since 2024-05-29 (for @bballdave025)

Other possible references
         ref02 = "https://docs.python.org/3/library/" + \
                 "os.html#miscellaneous-system-information"
archived_ref02 = "https://web.archive.org/web/20240529212940/" + \
                 "https://docs.python.org/3/library/os.html"
archived_ref03 = "https://web.archive.org/web/20240529212142/" + \
                 "https://stackoverflow.com/questions/276052/" + \
                 "how-to-get-current-cpu-and-ram-usage-in-python"
archived_ref04 = "https://web.archive.org/web/20240529220012/" + \
                 "https://stackoverflow.com/questions/64996339/" + \
                 "get-cpu-and-gpu-temp-using-python-without-admin-access-windows"
archived_ref05 = "https://web.archive.org/web/20240529222504/" + \
                 "https://superuser.com/questions/723506/" + \
                 "get-the-video-card-model-via-command-line-in-windows"

@todo : make this a class, 
        get certain parts of the info, 
        get info as done from several Linux/Windows/Mac commands
           (CMD) >systeminfo | findstr "OS"
           (CMD) >systeminfo
          (*NIX) $ uname -a
          ...
        get info about useful and/or problem-specific software
          (*NIX) $ bash --version # | head -n 1
          (*NIX) $ gcc --version # | head -n 1
          (*NIX) $ g++ --version # | head -n 1
          (*NIX) $ make --version # | head -n 2
          (*NIX) $ cmake --version # head -n 1
        get stuff from my standard Windows System query
        
        @result : Prints out a bunch of system info



        
'''
#########################################################################


##----------------
## IMPORTS
##----------------

import psutil
import platform
from datetime import datetime
import cpuinfo  # needs `pip install py-cpuinfo`
import socket
import uuid
import re

can_do_wmi = True # innocent until proven guilty
can_do_torch = True
can_do_tf = True

try:
  import torch
except Exception as e_torch:
  can_do_torch = False
finally:
  pass

try
  import tensorflow as tf
except Exception as e_tf:
  can_do_tf = False
finally:
  pass

# For windows
try:
  import wmi  # needs `pip install wmi`
except Exception as e_wmi:
  can_do_wmi = False
finally:
  pass


def main():
  '''
  An easy-to-remember entrance from the command-line
  '''

  print_system_information()
  
##endof:  main()


def run():
  '''
  An easy-to-remember entrance from the module name.
  '''

  print_system_information()
  
##endof:  run()


def print_system_information():
  '''
  Takes care of printing the system information. Right now, I know just Windows.

  Will take care of it for *NIX, too

  Later, this should have options as in the todo stuff above, as well
  as returning parts of the information. It should also give the option
  to show or not show some of the things commented out here.

  Also refer to my global_parameters functions

  Also later, this should be put into a SystemInformationProvider class.

  @result : prints system information to stdout
  '''

  print()
  print_main_sys_info()
  print()
  print_boot_time()
  print()
  
##endof:  print_system_information()


print_main_sys_info()
  '''
  High-level stuff
  '''
  
  print("#"*25, " System Information ", "#"*25)
  uname = platform.uname()
  print(f"System: {uname.system}")
  print("Node Name: NOT-FOR-NOW")
  #print(f"Node Name: {uname.node}")
  print(f"Release: {uname.release}")
  print(f"Version: {uname.version}")
  print(f"Machine: {uname.machine}")
  print(f"Processor: {uname.processor}")
  print(f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}")
  print("Ip-Address: NOT-FOR-NOW")
  #print(f"Ip-Address: {socket.gethostbyname(socket.gethostname())}")
  print("Mac-Address: NOT-FOR-NOW")
  #print(f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")
##endof:  print_main_sys_info()


def print_boot_time():
  '''
  Gives a timestamp before when this module was run, hopefully
  close to the time when the work is being done.
  '''

  print("#"*25, "#### Boot Time #####", "#"*25)
  
##endof:  print_boot_time()





def print_gpu_graphics_card_info():
  '''
  
  '''

  print("Information on GPU(s)/Graphics Card(s)")
  print(" (if any such information is to be found)")
  print()
  
  if can_do_wmi:
    print("Using  wmi , we get the following  win32_VideoController  names.")
    this_computer = wmi.WMI()
    for so_called_gpu in this_computer.Win32_VideoController():
      print("  ", so_called_gpu.name)
    ##endof:  for so_called_gpu in this_computer.Win32_VideoController()
  else:
    print("Can't use  wmi  to test for GPU/Graphics Card.")
  ##endof:  if can_do_wmi

  if can_do_torch:
    print("Using  PyTorch  and the  torch.cuda.is_available()  method.")
    torch_cuda_is_available = torch.cuda.is_available()
    print("The statement, 'There is CUDA and an appropriate GPU',")
    print("  is ... ", str(torch_cuda_is_available))
  else:
    print("Can't use  PyTorch  to test for (NVidia, CUDA-enabled) GPU.")
  ##endof:  if can_do_torch

  if can_do_tf:
    print("Using  TensorFlow  with several of its methods.")
  else:
    print("Can't use  TensorFlow  to test for GPU.")
  ##endof:  if can_do_tf

  print()
  print("Those are all our chances to find out about any GPU/Graphics Cards.")
  
##endof:  print_gpu_graphics_card_info()


def get_size(n_bytes, suffix="B"):
  '''
  Scale bytes to a nice-looking format, so we don't get any factors
  of 10^5 or of 10^-8, etc. Well, actually just the big positive ones.
  examples:
    @todo : examples

  @param  int n_bytes  :  The number of bytes, which should be converted
                          to something more easily handled.
  @param  string suffix  :  The suffix for the units (the second character(s)
                            I make the default 'bB' instead of 'B' - bballdave025

  @return  string  : the well-formatted string representing the amount of memory
  '''
  cs_standard_pow2_factor = 1024
  
  for prefix in ["", "K", "M", "G", "T", "P"]:
    if n_bytes < cs_standard_pow2_factor:
      return f"{n_bytes:.2f}{prefix}{suffix}"
    ##endof:  if n_bytes < cs_standard_pow2_factor
    
    n_bytes /= cs_standard_pow2_factor
    
  ##endof:  for prefix in ...
##endof:  get_size(n_bytes, suffix="bB")

if __name__ == "__main__":
  ''' The script is called from the command-line '''

  main()

##endof:  if __name__ == "__main__"
