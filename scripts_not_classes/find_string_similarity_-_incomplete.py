#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
'''
# @ brief A variety of string similarity metrics, to be used for fuzzy match
# @file find_string_similarity.py
# @author David BLACK  @bballdave025
#
#
#@LIST
# #### !!!!!!!!!!!!! @@@@@@@@@@@@ !!!!!!!!!!!!!!!!!!! ############ !!!!!!!
# A very big list of possibilities can be found at the end of this file.
# They're from https://sourceforge.net/projects/simmetrics/
# @@@@@@@@@@ !!!!!!!!!!! ############## @@@@@@@@@@@@@@@ !!!!!!!!!!! @@@@@@

Search for '@LIST' for different possible phonetic representation or string
similarity metrics.

BEFORE USE:
Just tested this as run-alone and made some changes. -DWB 2020-04-02

(Note the `python -m` before the `pip install ...` installs the module for 
the system python. It's sometimes necessary on Windows. You can usually get 
away with just `pip install ...` and you probably need to only use 
`pip install` if you want to use this `find_string_similarity.py` in a
virtual environment -DWB 2020-04-02)

> python -m pip install distance python-Levenshtein fuzzy

If you want `python-Levenshtein` on Windows, you need to install
Microsoft Visual C++ Redistributables and Microsoft Visual Studio Build
Tools 2014

'''
##############################################################################

##--------------------
# IMPORT STATEMENTS
##--------------------
##N.B. all the "Next one needs ... pip install ..." are taken care of with 
##     the setuptools installation, unless you're doing this stand-alone
import os
import sys
import codecs
import difflib
from enum import Enum
import re
import traceback

do_have_python_Levenshtein = True # might change in try/except
do_have_fuzzy = True # might change in try/except

## Next one needs `pip install distance`
import distance
## Next one needs `pip install fuzzy`. Needs VS 2014
## and VS Build Tools 2014
try:
  import fuzzy
except ImportError as ief:
  do_have_fuzzy = False
##endof:  try/except <fuzzy>
## Next one needs `python -m pip install python-Levenshtein
## it's faster than the `difflib` implementation
## Also needs some Microsoft Visual C++/Studo stuff.
try:
  import Levenshtein
except ImportError as ie:
  do_have_python_Levenshtein = False
##endof:  try/except <python-Levenshtein>
## For Python2
# from __future__ import absolute_import

is_stand_alone = True
#@TODO : figure out a good way to test this.

##----------------------
# ACCESSIBLE VARIABLES
##----------------------
class GraphemicSimilarityMetric(Enum):
  '''
  An easy way to choose from the implemented graphemic similarity metrics
  
  References:
  "https://stackoverflow.com/questions/1471153/" + \
  "string-similarity-metrics-in-python"
  (and answers)
  http://www.dcs.shef.ac.uk/~sam/stringmetrics.html
  https://en.wikipedia.org/wiki/String_metric
  
  
  #@LIST
  Possibilities:
  Levenshtein
  Damerau
  Gotoh
  Sorenson-Dice
  Kolmogorov/Compression Distance (NCD, NID?)
  Solomonoff–Kolmogorov–Chaitin (algorithmic complexity)
  Needleman-Wunch/Sellers
  Block (L1)
  Hamming
  Jaro
  Jaro-Winkler
  SMC
  Jaccard/Tanimoto
  Tversky
  Overlap
  Hellinger/Bhattacharyya
  Jensen-Shannon (info radius)
  Tau/Kullback-Leibler
  
  Other stuff I'm putting here, in case
  tf-idf
  Dirichlet
  Chapman
  
  https://abydos.readthedocs.io/en/latest/abydos.distance.html
  
  #@LIST
  !!!!!@@@@@@@!!!!!
  !@! LOOK HERE !@!
  https://sourceforge.net/projects/simmetrics/
  See the end of the file for some more info about what's there
  '''
  
  #@LIST
  NONE_GR = 0
  LEVENSHTEIN_GR = 1  # Classic edit distance
  DAMERAU_GR= 2      # Takes transpositions into account.
  SORENSEN_GR = 3     # More research
  JACCARD_GR = 4      # More research
  
##endof:  class GraphemicSimilarityMetric(Enum)


class PhoneticSimilarityMetric(Enum):
  '''
  An easy way to choose from the implemented phonemic similarity metrics.
  (I don't know if we'll have any of these by themselves. I think we'll
   get a phonetic representation and then use a Graphemic Similarity
   Metric.)
  '''
  
  #@LIST
  NONE_PHM = 0
  
##endof:  class PhoneticSimilarityMetric(Enum)


class GraphemicRepresentation(Enum):
  '''
  An easy way to choose from the implemented graphemic representation metrics
  
  References:
  
  '''
  
  #@LIST
  NONE_GRR = 0
  WORD2VEC_GRR = 1
  
##endof:  class GraphemicRepresentation(Enum)


class PhoneticRepresentation(Enum):
  '''
  An easy way to choose from the implemented phonetic representation metrics
  
  References:
  https://stackabuse.com/phonetic-similarity-of-words-a-vectorized-approach-in-python/
  https://web.archive.org/web/20230305005535/https://stackabuse.com/phonetic-similarity-of-words-a-vectorized-approach-in-python/
  
  
  '''
  
  #@LIST
  NONE_PH = 0
  SOUNDEX_PH = 1
  DMETAPHONE_PH = 2
  NYSIIS_PH = 3
  
  
##endof:  class PhoneticRepresentationMetric(Enum)


class SimlOrReprImplementation(Enum):
  '''
  An easy way to choose from the implementations
  
  Stands for
  "Similarity Or Representation Implementation"
  (Sim l      Or Repr           Implementation
  '''
  
  #@LIST
  NONE = 0
  DIFFLIB = 1
  PYTHON_LEVENSHTEIN = 2
  DIFFERENCE = 3
  FUZZY = 4
  
  
  SCRATCH = -137 #  These are my attempts to implement to algorithms,
                 #+ mostly to see if I can match and understand.
  
##endof:  class PhoneticSimilarityMetric(Enum)


# Debugging/seeing steps
do_debug_any_steps = True


##------------
# CODE
##------------
def main(str1, str2):
  '''
  I imagine I'll decide on a best combination of compares/similarities
  
  @param str1 : The first  string to be compared.
  @param str2 : The second string to be compared.
  
  @returns    : A measure for the string similarity
  '''
  return run(str1, str2)
  
##endof:  main (str1, str2)


def run(str1, str2):
  '''
  I imagine I'll decide on a best combination of compares/similarities
  
  @param str1 : The first  string to be compared.
  @param str2 : The second string to be compared.
  
  @returns    : A measure for the string similarity
  '''
  try:
    to_return_sim_meas = \
      get_best_similarity_measure(str1, str2)
  except Exception as e:
    print("Something went wrong. The exception string is")
    print(str(e))
    traceback.print_exc()
    print()
  finally:
    pass
  ##endof:  try/except/finally
  
  return to_return_sim_meas
  
##endof:  main (str1, str2)


def get_best_similarity_measure(str1, str2):
  '''
  I imagine I'll decide on a best combination of compares/similarities
  
  @param str1 : The first  string to be compared.
  @param str2 : The second string to be compared.
  
  @returns    : A measure for the string similarity
  '''
  
  # A stand-in, for now.
  if do_have_python_Levenshtein:
    return get_Lev_fast(str1, str2)
  else:
    return 
  ##endof:  if do_have_python_Levenshtein
  
##endof:  get_best_similarity_measure(str1, str2)


def get_linearly_combined_graphemic_similarity(str1, str2):
  '''
  For now, hard-code-in the linear combination and the result compare
  
  cf. https://stackoverflow.com/a/31236472/6505499
  
  @TODO : make this use the Enums
  
  @param str1 : The first  string to be compared.
  @param str2 : The second string to be compared.
  
  @returns    : A measure for the string similarity
  '''
  n_metrics = 0
  
  #@LIST
  seq_matcher = difflib.SequenceMatcher(None, str1, str2).ratio()
  sm_weight = 1
  n_metrics += 1
  
  if do_debug_any_steps:
    print("seq_matcher: " + str(seq_matcher))
    print("sm_weight:   " + str(sm_weight))
  ##endof:  if do_debug_any_steps
  
  if do_have_python_Levenshtein:
    lev_fast = Levenshtein.ratio(str1, str2)
    lev_weight = 1
    n_metrics += 1
    
    if do_debug_any_steps:
      print("lev_fast:   " + str(lev_fast))
      print("lev_weight: " + str(lev_weight))
    ##endof:  if do_debug_any_steps
  else:
    lev_fast = 0
    lev_weight = 0
  ##endof:  if do_have_python_Levenshtein
  
  sorensen = 1 - distance.sorensen(str1, str2)
  sor_weight = 1
  n_metrics += 1
  
  if do_debug_any_steps:
    print("sorensen:   " + str(sorensen))
    print("sor_weight: " + str(sor_weight))
  ##endof:  if do_debug_any_steps
  
  jaccard = 1 - distance.jaccard(str1, str2)
  jac_weight = 1
  n_metrics += 1
  
  if do_debug_any_steps:
    print("jaccard:    " + str(jaccard))
    print("jac_weight: " + str(jac_weight))
  ##endof:  if do_debug_any_steps
  
  lin_comb_metric = (sm_weight * seq_matcher + \
                     lev_weight * lev_fast + \
                     sor_weight * sorensen + \
                     jac_weight * jaccard) / n_metrics
  
  return lin_comb_metric
  
##endof:  get_linearly_combined_graphemic_similarity(str1, str2)


def get_linearly_combined_phonetic_similarity(str1, str2):
  '''
  For now, we'll linearly combine the metrics.
  
  ## @todo : implement this with a `get_phonetic_representation` function
  ##         It's called 
  ## ```python
  ## get_phonetic_repr_for_str(this_str, 
  ##                  phonrepr=PhoneticRepresentation.<one-from-the-enum>,
  ##                  impl=SimlOrReprImplementation.<one-from-the-enum>)
  ## ```
  ##         but,
  ##         for now, it just `pass`es
  
  @param str1 : The first  string to be compared.
  @param str2 : The second string to be compared.
  
  @returns    : A measure for the string similarity
  '''
  
  n_representations = 0
  
  if do_have_fuzzy:
    #@LIST
    soundex_fuzzy_1 = fuzzy.soundex(str1) # returns the strings with the soundex
    soundex_fuzzy_2 = fuzzy.soundex(str2) # representations
    soundex_weight = 1
    n_representations += 1
  ##endof:  if do_have_fuzzy
  
  if do_debug_any_steps and do_have_fuzzy:
    print("soundex_fuzzy_1: " + str(soundex_fuzzy_1))
    print("soundex_fuzzy_2: " + str(soundex_fuzzy_2))
    print("soundex_weight:  " + str(soundex_weight))
  ##endof:  if do_debug_any_steps
  
  if do_have_fuzzy:
    ## Need to research this more, so I can know how to use, e.g. Levenshtein
    ## on these two.
    dmeta_1 = fuzzy.DMetaphone(str1) # returns an array with the DMetaphone
    dmeta_2 = fuzzy.DMetaphone(str2) # representations. @todo : research more!
    dmeta_weight = 0
    #n_representations += 1 # not using for now.
  ##endof:  if do_have_fuzzy
  
  if do_debug_any_steps and do_have_fuzzy:
    print("dmeta_1:       " + str(dmeta_1))
    print("dmeta_2:       " + str(dmeta_2))
    print("dmeta_weight:  " + str(dmeta_weight))
    print("Not even including this now, since I don't know how to")
    print("deal with the array.")
  ##endof:  if do_debug_any_steps
  
  if do_have_fuzzy:
    nysiis_1 = fuzzy.nysiis(str1) # returns a string with the nysiis
    nysiis_2 = fuzzy.nysiis(str2) # representation.
    nysiis_weight = 1
    n_representations += 1
  ##endof:  if do_have_fuzzy
  
  if do_debug_any_steps and do_have_fuzzy:
    print("nysiis_1:       " + str(nysiis_1))
    print("nysiis_2:       " + str(nysiis_2))
    print("nysiis_weight:  " + str(nysiis_weight))
    print("Not even including this now, since I don't know how to")
    print("deal with the array.")
  ##endof:  if do_debug_any_steps
  
  text_similarity_algorithm = GraphemicSimilarityMetric.LEVENSHTEIN
  
  soundex_distance = -1
  dmeta_distance = -1
  nysiis_distance = -1
  
  lin_comb_distance = 0
  
  if text_similarity_algorithm is GraphemicSimilarityMetric.LEVENSHTEIN:
    if do_have_fuzzy:
      soundex_distance=None
      if do_have_python_Levenshtein:
        soundex_distance = Levenshtein.ratio(soundex_fuzzy_1, soundex_fuzzy_2)
      else:
        soundex_distance = distance.nlevenshtein(soundex_fuzzy_1,
                                                 soundex_fuzzy_2)
      ##endof:  if/else do_have_python_Levenshtein
    ##endof:  if do_have_fuzzy
    
    if do_debug_any_steps and do_have_fuzzy:
      print("soundex_distance: " + str(soundex_distance))
      print("soundex_weight:   " + str(soundex_weight))
    ##endof:  if do_debug_any_steps
    
    dmeta_is_implemented = False
    
    if dmeta_is_implemented and do_have_fuzzy:
      dmeta_distance = 2.71828 # I don't know how to implement this, now.
      
      if do_debug_any_steps:
        print("dmeta_distance: " + str(dmeta_distance))
        print("dmeta_weight:   " + str(dmeta_weight))
      ##endof:  if do_debug_any_steps
    ##endof:  if dmeta_is_implemented
    
    if do_have_fuzzy:
      nysiis_distance=None
      if do_have_python_Levenshtein:
        nysiis_distance = Levenshtein.ratio(nysiis_1, nysiis_2)
      else:
        nysiis_distance = distance.nlevenshtein(nysiis_1, nysiis_2)
      ##endof:  if/else do_have_python_Levenshtein
    ##endof:  if do_have_fuzzy
    
    if do_debug_any_steps and do_have_fuzzy:
      print("nysiis_distance: " + str(nysiis_distance))
      print("nysiis_weight:   " + str(nysiis_weight))
    ##endof:  if do_debug_any_steps
    
  ##endof:  if algorithm is Levenshtein
  
  if do_have_fuzzy:
    non_normalized_combination = soundex_weight * soundex_distance + \
                                 nysiis_weight  * nysiis_distance
    
    lin_comb_distance = non_normalized_combination / n_representations
    
    if do_debug_any_steps:
      print("lin_comb_distance: " + str(lin_comb_distance))
    ##endof:  if do_debug_any_steps
    
    return lin_comb_distance
  
  nope_str = "Not doing fuzzy/phonetic similarity for scoring."
  print(nope_str)
  return nope_str
  
##endof:  get_linearly_combined_phonetic_similarity(str1, str2)


def get_phonetic_similarity(str1, str2):
  '''
  Use the representations to find similarity.
  
  @todo : this!
  
  @param str1 : The first  string to be compared.
  @param str2 : The second string to be compared.
  
  @returns    : A measure for the string similarity
  '''
  
  pass
  
##endof:  get_phonetic_similarity(str1, str2)


def get_phonetic_repr_for_str(this_str, 
                              phonrepr=PhoneticRepresentation.SOUNDEX_PH,
                              impl=SimlOrReprImplementation.FUZZY):
  '''
  Uze the different phonetic representations.
  
  @param : this_string  the input string
  @param : phonrepr     A phonetic representation from the
                        PhoneticRepresenation Enum.
  @param : impl         The implementing package, function, whatever, from
                        the SimlOrReprImplementation Enum. (That stands
                        for Similarity or Representation Implementation)
  @returns :            some kind of representation. I'll need to study.
  '''
  
  #@TODO : Logic for returning the correct phonetic representation,
  #        using Enums.
  
  pass
  
##endof:  get_phonetic_repr_for_str(this_str)


def get_graphemic_repr_for_str(this_str, 
                           grafrepr=GraphemicSimilarityMetric.LEVENSHTEIN_GR,
                           impl=SimlOrReprImplementation.PYTHON_LEVENSHTEIN):
  '''
  Uze the different phonetic representations.
  
  @param : this_string  the input string
  @param : grafrepr     A graphemic representation from the
                        GraphemicRepresenation Enum.
  @param : impl         The implementing package, function, whatever, from
                        the SimlOrReprImplementation Enum. (That stands
                        for Similarity or Representation Implementation)
  @returns :            some kind of representation. I'll need to study.
  '''
  
  #@TODO : Logic for returning the correct graphemic representation.
  #        using Enums
  
  pass
  
##endof:  get_graphemic_repr_for_str(this_str)


def get_Lev_fast(str1, str2):
  '''
  Returns the Levenshtein distance between the 2 strings using python-Lev..
  
  Supposedly much faster than other implementations, cf. <stackoverflow>
  
  @param str1 : The first  string to be compared.
  @param str2 : The second string to be compared.
  
  @returns    : A measure for the string similarity
  '''
  
  if do_have_python_Levenshtein:
    return Levenshtein.ratio(str1, str2)
  else:
    print("python-Levenshtein not available.")
    return get_other_Lev(str1, str2, this_method=1)
  ##endof:  if do_have_python_Levenshtein
##endof:  get_Lev_fast(str1, str2)


def get_other_Lev(str1, str2, this_method=1):
  '''
  Returns the Levenshtein distance ratio using the distance package.
  
  
  
  Hamming and Levenshtein distance can be normalized, so that the results of several distance measures can be meaningfully compared. Two strategies are available for Levenshtein: either the length of the shortest alignment between the sequences is taken as factor, or the length of the longer one. Example uses:

  >>> distance.hamming("fat", "cat", normalized=True)
  0.3333333333333333
  >>> distance.nlevenshtein("abc", "acd", method=1)  # shortest alignment
  0.6666666666666666
  >>> distance.nlevenshtein("abc", "acd", method=2)  # longest alignment
  0.5
  
  With `method=1` we get the same result as get_Lev_fast, i.e. the same as the
  python-Levenshtein package's Levenshtein.ratio(str1, str2)
  
  Somewhere, I read that this is different from the standard, but I'm not sure.
    -DWB 2020-05-18
  
  @param str1 : The first  string to be compared.
  @param str2 : The second string to be compared.
  @param this_method : Whether to use the shortest alignmetn (1) or the 
                       longest alignment (2) for the ratio.
                       Must be an int with value of 1 or 2
  
  @returns    : A measure for the string similarity
  
  '''
  
  return distance.nlevenshtein(str1, str2, method=this_method)
  
##endof:  get_other_Lev(str1, str2)


## For the next two functions, heavily cf.
##"https://medium.com/@yash_agarwal2/" + \
##"soundex-and-levenshtein-distance-in-python-8b4b56542e9e"


def dwb_scratch_levenshtein(str1, str2):
  '''
  Levenshtein distance (edit distance) as Dave tries to implement it.
  
  I'm going to be outputting the crap out of this, so I understand the
  algorithm better.
  
  @ref: extended (quite a bit) from
  "https://medium.com/@yash_agarwal2/" + \
  "soundex-and-levenshtein-distance-in-python-8b4b56542e9e"
  
  @param str1 : The first  string to be compared.
  @param str2 : The second string to be compared.
  
  @returns    : A measure for the string similarity
  '''
  # debugging or just seeing the steps.
  do_show_beginning_and_end_matr = True
  do_show_steps = True
  do_show_running_edit_distance = True
  do_show_edit_distance_end = True
  do_show_innards = True
  
  pprint_is_imported = False
  
  ## to lower case
  if not is_stand_alone:
    str1 = ep.robust_to_lower(str1)
    str2 = ep.robust_to_lower(str2)
  else:
    str1 = str1.lower()
    str2 = str2.lower()
  ##endof:  if not is_stand_alone
  
  ## Make the matrix.
  height_with_str2 = len(str2)
  width_with_str1 = len(str1)
  
  ## zero it out
  lev_matrix = \
    [[(0, '  ') for letter in range(width_with_str1 + 1)] \
                     for letter in range(height_with_str2 + 1)]
  
  for index_x in range(1, width_with_str1 + 1):
    lev_matrix[0][index_x] = (index_x, ' ' + str1[index_x - 1])
  ##endof:  for index_x
  
  for index_y in range(1, height_with_str2 + 1):
    lev_matrix[index_y][0] = (index_y, str2[index_y - 1] + ' ')
  ##endof:  for index_y
  
  if do_show_beginning_and_end_matr:
    print()
    print("Beginning matrix:")
    import pprint
    pprint_is_imported = True
    pprint.pprint(lev_matrix)
    print()
  ##endof:  if do_show_beginning_and_end_matr
  
  ## For each zero in the matrix, we compare 
  ## 1) the value (number) to the left of where we are (index_x - 1)<-number
  ## 2) the value (number) above where we are (index_y - 1)<-number
  ## 3) a value depending on the two letters corresponding to our position
  ##   i. If the characters match, we use the number to the immediate top-left
  ##  ii. If the characters don't match, we use 1 plus the number to the
  ##      immediate top-left
  ##
  ## We compare those three values (numbers) and take the minimum for the
  ## value (number) at our position.
  
  if do_show_steps:
    print()
    print("Steps:")
    if not pprint_is_imported:
      import pprint
      pprint_is_imported = True
      pprint.pprint(lev_matrix)
      print()
    ##endof:  if not pprint_is_imported
  ##endof:  if do_show_steps
  
  for index_x in range(1, width_with_str1 + 1):
    for index_y in range(1, height_with_str2 + 1):
      num_for_position = 0 # needs to be calculated, but now 0
      y_str = str2[index_y - 1]
      x_str = str1[index_x - 1]
      str_for_position = y_str + x_str
      
      to_the_left_num = lev_matrix[index_y][index_x - 1][0]
      above_num = lev_matrix[index_y - 1][index_x][0]
      third_num_pre_upleft = lev_matrix[index_y - 1][index_x - 1][0]
      
      if do_show_innards:
        print()
        print("Current calculation info:")
        print("index_y: " + str(index_y) + ", index_x: " + str(index_x))
        print("  str_y: " + y_str        + ",   str_x: " + x_str)
        print("------------")
        print("                  to the left: " + \
                             str(to_the_left_num) + \
              "\nFOR COMPARISON      add one: " + \
                             str(to_the_left_num + 1) + \
              "\n                      above: " + str(above_num) + \
              "\nFOR COMPARISON      add one: " + \
                             str(above_num + 1) + \
              "\n    immediately up and left: " +  str(third_num_pre_upleft))
      ##endof:  if do_show_innards
      
      to_the_left_num += 1
      above_num += 1
      
      compare_str = " equal"
      
      if y_str != x_str:
        third_num_pre_upleft += 1
        compare_str = " not equal"
      ##endof:  if y_str == x_str
      
      third_num = third_num_pre_upleft
      
      if do_show_innards:
        print("  the strings are" + compare_str)
        print("FOR COMPARISON  third: " + str(third_num))
        print()
        print("compared for minimum: " + str(to_the_left_num) + \
              ", " + str(above_num) + ", " + str(third_num))
        print()
      ##endof:  do_show_innards
      
      num_for_position = min(to_the_left_num,
                             above_num,
                             third_num)
      
      lev_matrix[index_y][index_x] = (num_for_position, str_for_position)
      
      if do_show_steps:
        pprint.pprint(lev_matrix)
        print()
      ##endof:  if do_show_steps
      
      if do_show_running_edit_distance:
        print("Running edit distance: " + str(num_for_position))
        print()
      ##endof:  if do_show_running_edit_distance
      
    ##endof:  for index_y
  ##endof:  for index_x
  
  if do_show_steps:
    print("Last of steps above.")
    print()
  ##endof:  do_show_steps
  
  if do_show_beginning_and_end_matr:
    print()
    print("End matrix:")
    pprint.pprint(lev_matrix)
    print()
  ##endof:  if do_show_beginning_and_end_matr
  
  edit_distance = lev_matrix[len(str2)][len(str1)][0]
  
  if do_show_edit_distance_end:
    print("The complete edit distance: " + str(edit_distance))
  ##endof:  if do_show_edit_distance_end
  
  if do_show_steps:
    print()
    print("Maybe, someday, I'll get back here to do the traceback -DWB")
    print()
  ##endof:  if do_show_steps
  
  return edit_distance
  
##endof:  dwb_scratch_levenshtein(str1, str2)


def dwb_scratch_soundex(this_str,
                        do_extend_to_sql=False):
  '''
  Returns the soundex representation of the string. My attempt DOESN'T WORK!
  (yet)
  
  RIGHT NOW, THIS DOESN'T DO THINGS ALL THE WAY CORRECTLY!
  I NEED TO TAKE CARE OF TWO 'PLACE OF ENUNCIATION' NUMBERS
  BEING SEPARATED BY A VOWEL BOTH APPEARING.
  It fails the "Tymczak test", and I haven't gone through any of
  the other wiki examples of input and output.
  
  Wikipedia ( https://en.wikipedia.org/wiki/Soundex )
  
  @archived_reference = "https://web.archive.org/web/" + \
  "20180528194518/" + \
  "https://en.wikipedia.org/wiki/Soundex"
  
  The Soundex code for a name consists of a letter followed by three
  numerical digits: the letter is the first letter of the name, and the
  digits encode the remaining consonants. Consonants at a similar place 
  of articulation share the same digit so, for example, the labial 
  consonants B, F, P, and V are each encoded as the number 1.
  
  The correct value can be found as follows:
  
  1. Retain the first letter of the name and drop all other 
  occurrences of 
    a, e, i, o, u, y, h, w.
  
  2. Replace consonants with digits as follows (after the first letter):
    b, f, p, v -> 1
    c, g, j, k, q, s, x, z -> 2
    d, t -> 3
    l -> 4
    m, n -> 5
    r -> 6
  If two or more letters with the same number are adjacent in the 
  original name (before step 1), only retain the first letter; also 
  two letters with the same number separated by 'h' or 'w' are coded 
  as a single number, whereas such letters separated by a vowel are
  coded twice. This rule also applies to the first letter.

  If you have too few letters in your word that you can't assign three
  numbers, append with zeros until there are three numbers. If you have
  more than 3 letters, just retain the first 3 numbers.
  
  Using this algorithm, both "Robert" and "Rupert" return the same string 
  "R163" while "Rubin" yields "R150". "Ashcraft" and "Ashcroft" both yield 
  "A261" and not "A226" (the chars 's' and 'c' in the name would receive a 
  single number of 2 and not 22 since an 'h' lies in between them). 
  "Tymczak" yields "T522" not "T520" (the chars 'z' and 'k' in the name 
  are coded as 2 twice since a vowel lies in between them). "Pfister" 
  yields "P236" not "P123" (the first two letters have the same number and 
  are coded once as 'P'), and "Honeyman" yields "H555".
  
  @param : this_string  the input string
  @returns :            some kind of representation.
  '''
  
  #debugging or seeing the algorith.
  do_debug_under_the_hood = True
  have_not_fixed_tymczak_yet = True
  
  class ThreeTypeLetter(Enum):
    '''
    The three types of letters for soundex keep vs. remove
    
    Note that there are two types of letters under to "remove" label.
    Vowels can still serve as a separator, allowing two letters with
    the same place of enunciation to both be represented.
    Vowel-ish are removed and don't serve as a separator.
    '''
    
    CONSONANT_TO_KEEP = 1
    VOWEL_TO_REMOVE_BUT_SEPARATOR = 2
    VOWEL_ISH_TO_REMOVE = 3
  
  ##endof:  ThreeTypeLetter(Enum)
  
  class PlaceOfEnunciation(Enum):
    '''
    Keeping track of the places of enunciation that get assigned numbers.
    '''
    
    BILABIAL = 1
    PALATE_ISH = 2
    INTERDENTAL = 3
    LATERAL_LIQUID = 4
    NASAL = 5
    RHOTAL_LIQUID = 6
    
  ##endof:  PlaceOfEnunciation(Enum)
  
  if do_debug_under_the_hood:
    print("original string: '" + this_str + "'")
  ##endof:  if do_debug_under_the_hood
  
  ## to lower case
  if not is_stand_alone:
    this_str = ep.robust_to_lower(this_str)
  else:
    this_str = this_str.lower()
  ##endof:  if/else not is_stand_alone
  
  # Get first letter
  try:
    this_first_letter = this_str[0]
  except Exception as ex:
    sys.stdout.write("\nYou probably didn't pass in a string ")
    sys.stdout.write("to\n" + 
           "utils.find_string_similarity.dwb_scratch_soundex")
    sys.stdout.write("\nbut here's the exception string:")
    sys.stdout.write("\n" + str(ex))
    sys.stdout.write("\nRaising.")
    raise
  finally:
    pass
  ##endof:  try/catch/finally
  
  soundex_str = this_first_letter
  
  other_letters = this_str[1:]
  
  if do_debug_under_the_hood:
    print("this_first_letter: '" + this_first_letter + "'")
    print("other_letters:     '" + other_letters + "'")
  ##endof:  if do_debug_under_the_hood
  
  if other_letters == '':
    soundex_str = fill_out_soundex_str(soundex_str)
    if do_debug_under_the_hood:
      print("(getting returned) soundex_str: '" + soundex_str + "'")
    ##endof:  if do_debug_under_the_hood
    return soundex_str
  ##endof:  if other_letters == ''
  
  
  ### <FIXING> ###
  
  # # # ## Thinking this will be more complex than regex matches.
  # # # def Surroundings(Enum):
    # # # '''
    # # # Allow for the rule that two of the same digit can stay 
    # # # if they are separated by a vowel
    # # # '''
    
    # # # NONE_CURR_NONE = 0
    # # # VOWL_CURR_NONE = 1
    # # # CONS_CURR_NONE = 2
    # # # NONE_CURR_VOWL = 3
    # # # VOWL_CURR_VOWL = 4
    # # # CONS_CURR_VOWL = 5
    
  # # # ##endof:  Surroundings(Enum)
  
  # # # letters_to_keep = set('bcdfgjklmnpqrstvxzBCDFGJKLMNPQRSTVXZ')
  # # # vowels_to_remove = set('aeiouyAEIOUY')
  # # # vowel_ish_to_remove = set('hwHW')
  
  letters_to_keep = 'bcdfgjklmnpqrstvxz'
  vowels_to_remove = 'aeiouy'
  vowel_ish_to_remove = 'hw'
  
  letters_to_keep_set = set(letters_to_keep)
  vowels_to_remove_set = set(vowels_to_remove)
  vowel_ish_to_remove_set = set(vowel_ish_to_remove)
  
  letters_to_keep_group = r"[" + letters_to_keep + r"]"
  vowels_to_remove_group = r"[" + vowels_to_remove + r"]"
  vowel_ish_to_remove_group = r"[" + vowel_ish_to_remove + r"]"
  
  split_up_3_regex = letters_to_keep_group     + r"*" + r"|" + \
                     vowels_to_remove_group    + r"*" + r"|" + \
                     vowel_ish_to_remove_group + r"*"
  
  split_in_3_groups_array = re.findall(split_up_3_regex,
                                       other_letters,
                                       flags=re.I)
  
  if not is_stand_alone:
    split_in_3_groups_array = [my_str.lower() \
                               for my_str in split_in_3_groups_array \
                                                            if my_str != '']
  else:
    split_in_3_groups_array = [ep.robust_to_lower(my_str) \
                               for my_str in split_in_3_groups_array \
                                                            if my_str != '']
  ##endof:  if not is_stand_alone
  
  if do_debug_under_the_hood:
    print(str(split_in_3_groups_array))
  ##endof:  if do_debug_under_the_hood
  
  remaining_consonants_and_groups_array = [0] * len(split_in_3_groups_array)
                                          #split_in_3_groups_array[:]
  
  for i, str_or_set in enumerate(split_in_3_groups_array):
    take_out_vowels_filter = \
      ''.join(filter(vowels_to_remove_set.__contains__, str_or_set))
    take_out_vowel_ish_filter = \
      ''.join(filter(vowel_ish_to_remove_set.__contains__, str_or_set))
    if take_out_vowels_filter != '':
      remaining_consonants_and_groups_array[i] = \
                           ThreeTypeLetter.VOWEL_TO_REMOVE_BUT_SEPARATOR
    elif take_out_vowel_ish_filter != '':
      remaining_consonants_and_groups_array[i] = \
                           ThreeTypeLetter.VOWEL_ISH_TO_REMOVE
    else:
      # leave the consonant (or consonant cluster)
      pass
    ##endof:  ##endof:  if/elif/else <the filters left nothing>
  ##endof:  for i,str_or_set in <what-will-be-consonants-and-groups-array>
  
  if do_debug_under_the_hood:
    print(str(remaining_consonants_and_groups_array))
  ##endof:  if do_debug_under_the_hood
  
  # lett_by_lett_array
  
  
  #### </FIXING>
  
  if have_not_fixed_tymczak_yet:
    # Fails the Tymczak test
    letters_to_keep_set_1 = set('bcdfgjklmnpqrstvxzBCDFGJKLMNPQRSTVXZ')
    
    other_letters = \
        ''.join(filter(letters_to_keep_set_1.__contains__, other_letters))
    
    other_letters_str = other_letters
    
    # Make an array out of it
    other_letters = [char for char in other_letters]
  ##endof: if have_not_fixed_tymczak_yet
  
  if do_debug_under_the_hood:
    print("After removing and converting to an array:")
    print("other_letters: " + str(other_letters))
  ##endof:  if do_debug_under_the_hood
  
  
  if len(other_letters) == 0:
    fill_out_soundex_str(soundex_str)
  ##endof:  if len(other_letters) == 0
  
  bilabials_tup = ('b', 'f', 'p', 'v')
  palate_ish_tup = ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z')
  interdentals_tup = ('d', 't')
  lateral_liquid_tup = ('l')
  nasals_tup = ('m', 'n')
  rhotal_liquid_tup = ('r')
  
  # dictionary with group and value for consonant mapping
  replacement_dict = {bilabials_tup:      1,
                      palate_ish_tup:     2,
                      interdentals_tup:   3,
                      lateral_liquid_tup: 4,
                      nasals_tup:         5,
                      rhotal_liquid_tup:  6}
  
  ## This is from 
  ##"https://medium.com/@yash_agarwal2/" + \
  ##"soundex-and-levenshtein-distance-in-python-8b4b56542e9e"
  ## I'll have to study it. -DWB
  this_first_letter = [value if this_first_letter else first_letter \
                         for group, value in replacement_dict.items() \
                           if this_first_letter in group]
  
  other_letters = [value if char else char \
                     for char in other_letters \
                       for group, value in replacement_dict.items() \
                         if char in group]
  
  if do_debug_under_the_hood:
    print("Before the 'Tymczak problem':")
    print("this_first_letter: " + str(this_first_letter))
    print("other_letters:     " + str(other_letters))
  ##endof:  if do_debug_under_the_hood
  
  ## Here is the Tymczak problem. Doesn't take vowel-separation into account
  # get rid of adjacent same digits with one digit
  other_letters = [char for ind, char in enumerate(other_letters) \
                     if ( ind == len(other_letters) - 1 or \
                       (ind + 1 < len(other_letters) and \
                         char != other_letters[ind + 1]) )]
  
  if do_debug_under_the_hood:
    print("After the 'Tymczak problem' (getting rid of consecutives " + \
          "without checking for vowel between):")
    print("this_first_letter: " + str(this_first_letter))
    print("other_letters:     " + str(other_letters))
  ##endof:  if do_debug_under_the_hood
  
  # If the saved letter's digit is the same as the resulting
  # first digit, remove the digit, keeping the letter
  # The code makes more sense than the explanation.
  if this_first_letter == other_letters[0]:
    other_letters[0] = this_str[0]
  else:
    other_letters.insert(0, this_str[0])
  ##endof:  if this_first_letter == other_letters[0]
  
  if do_debug_under_the_hood:
    print("Before possible 0 appending:")
    print("this_first_letter: " + str(this_first_letter))
    print("other_letters:     " + str(other_letters))
  ##endof:  if do_debug_under_the_hood
  
  # Append 3 zeros if the result contains less than 3 digits.
  # Remove all except the first letter and 3 digits after it.
  this_first_letter = other_letters[0]
  other_letters = other_letters[1:]
  
  other_letters = [char for char in other_letters \
                     if isinstance(char, int)][0:3]
  
  while len(other_letters) < 3:
    other_letters.append(0)
  ##endof:  while len(other_letters) < 3
  
  other_letters.insert(0, this_first_letter)
  
  if do_debug_under_the_hood:
    print("Just before return string is ready:")
    print("this_first_letter: " + str(this_first_letter))
    print("other_letters:     " + str(other_letters))
  ##endof:  if do_debug_under_the_hood
  
  returned_soundex_str = ''.join([str(letter) for letter in other_letters])
  
  if do_debug_under_the_hood:
    print("returned_soundex_str: " + str(returned_soundex_str))
  ##endof:  if do_debug_under_the_hood
  
  return returned_soundex_str
  
##endof:  dwb_scratch_soundex(this_str, do_extend_to_sql=False)


def fill_out_soundex_str(in_str):
  '''
  Put zeros on the end of the string as needed.
  '''
  
  out_str = in_str

  # for some reason, this had `while len(in_str) < 4`
  while len(out_str) < 4:
    out_str += '0'
  ##endof:  while len(out_str) < 4
  
  return out_str
  
##endof:  fill_out_soundex_str(this_str)


if __name__ == "__main__": # Gets executed if the file is run as a script
  '''
  Takes all the command line arguments and dumps them as parameters to the
  main() method, implemented at the top of this Python file.
  '''
  
  main(sys.argv[1:])

##endof:  if __name__ == "__main__"







#
# Other sources, maybe:
#
# "https://www.c-sharpcorner.com/uploadfile/acinonyx72/" + \
# "calculating-the-normalized-compression-distance-between-two-strings/
#
#@LIST
# SIMMETRICS_SRC_V1_6_2_D07_02_07\SRC\UK\AC\SHEF\WIT\SIMMETRICS\SIMILARITYMETRICS
# |   AbstractStringMetric.java
# |   BlockDistance.java
# |   BlockDistanceTest.java
# |   CandidatesTest.java
# |   ChapmanLengthDeviation.java
# |   ChapmanLengthDeviationTest.java
# |   ChapmanMatchingSoundex.java
# |   ChapmanMatchingSoundexTest.java
# |   ChapmanMeanLength.java
# |   ChapmanMeanLengthTest.java
# |   ChapmanOrderedNameCompoundSimilarity.java
# |   ChapmanOrderedNameCompoundSimilarityTest.java
# |   CosineSimilarity.java
# |   CosineSimilarityTest.java
# |   DiceSimilarity.java
# |   DiceSimilarityTest.java
# |   EuclideanDistance.java
# |   EuclideanDistanceTest.java
# |   InterfaceStringMetric.java
# |   JaccardSimilarity.java
# |   JaccardSimilarityTest.java
# |   Jaro.java
# |   JaroTest.java
# |   JaroWinkler.java
# |   JaroWinklerTest.java
# |   Levenshtein.java
# |   LevenshteinTest.java
# |   MatchingCoefficient.java
# |   MatchingCoefficientTest.java
# |   MongeElkan.java
# |   MongeElkanTest.java
# |   NeedlemanWunch.java
# |   NeedlemanWunchTest.java
# |   OverlapCoefficient.java
# |   OverlapCoefficientTest.java
# |   package.html
# |   QGramsDistance.java
# |   QGramsDistanceTest.java
# |   SmithWaterman.java
# |   SmithWatermanGotoh.java
# |   SmithWatermanGotohTest.java
# |   SmithWatermanGotohWindowedAffine.java
# |   SmithWatermanGotohWindowedAffineTest.java
# |   SmithWatermanTest.java
# |   Soundex.java
# |   SoundexTest.java
# |   TagLink.java
# |   TagLinkTest.java
# |   TagLinkToken.java
# |   TagLinkTokenTest.java
# |   TestSuite.java
# |
# +---costfunctions
# |   |   AbstractAffineGapCost.java
# |   |   AbstractSubstitutionCost.java
# |   |   AffineGap1_1Over3.java
# |   |   AffineGap1_1Over3Test.java
# |   |   AffineGap5_1.java
# |   |   AffineGap5_1Test.java
# |   |   InterfaceAffineGapCost.java
# |   |   InterfaceSubstitutionCost.java
# |   |   package.html
# |   |   SubCost01.java
# |   |   SubCost01Test.java
# |   |   SubCost1_Minus2.java
# |   |   SubCost1_Minus2Test.java
# |   |   SubCost5_3_Minus3.java
# |   |   SubCost5_3_Minus3Test.java
# |   |   TestSuite.java
# |   |
# |   \--- ### PACKAGING STUFF
# |
# \--- ### PACKAGING STUFF
#
#
