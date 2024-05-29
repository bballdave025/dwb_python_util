#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################################
'''

@since 2024-05-29  (for GitHub @bballdave025)
@todo : a lot

From the source answer by StackOverflow user, @Karol_Zlot

> It's convenient to put those progress bars in separate 
> process using multiprocessing library.

@ref1 = "https://web.archive.org/web/20240529212132/" + \
        "https://gist.github.com/karolzlot/" + \
        "26864e21e7347ce41f71f87f156ea266"

@ref2 = "https://web.archive.org/web/20240529212142/" + \
        "https://stackoverflow.com/questions/276052/" + \
        "how-to-get-current-cpu-and-ram-usage-in-python"

@result : Cool, refreshing bars showing how much disk and ram are being
          used.

'''
##########################################################################

from tqdm import tqdm
from time import sleep
import psutil

with tqdm(total=100, 
          desc='cpu%', 
          position=1) as cpubar, tqdm(total=100, 
                                      desc='ram%', 
                                      position=0) as rambar:
  while True:
    rambar.n = psutil.virtual_memory().percent
    cpubar.n = psutil.cpu_percent()
    rambar.refresh()
    cpubar.refresh()
    sleep(0.5)
  ##endof:  while true
##endof:  with tqdm ... as cpubar, tqdm ... as rambar
