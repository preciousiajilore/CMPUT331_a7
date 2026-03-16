#!/usr/bin/env python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2026 Precious Ajilore
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
# ---------------------------------------------------------------

"""
Assignment 7 Problems 2, 3, and 4
"""

from random import sample
import re
from sys import flags


def stringIC(text: str) -> float:
    """
    Compute the index of coincidence (IC) for text
    1. count how many times each letter A-Z appears in text
    2. compute the IC using the formula:
       IC = (sum of n_i * (n_i - 1)) 
       where n_i is the count of letter i and N is the total number of letters in text
    3. Divide the sum by N * (N - 1) to get the final IC value
    4. Return the IC value as a float
    """
    n = len(text)
    if n < 2:
        return 0.0
    
    letter_counts = [0] * 26

    for ch in text:
        letter_counts[ord(ch) - ord('A')] += 1
    
    numerator = 0
    for count in letter_counts:
        numerator += count * (count - 1)

    denominator = n * (n - 1)

    return numerator / denominator



def subseqIC(ciphertext: str, keylen: int) -> float:
    """
    Return the average IC of ciphertext for 
    subsequences induced by a given a key length
    """
    total_ic = 0.0

    #start with 1 because the first subsequence is the 1st letter of each key length set of letters in text
    for i in range(1, keylen + 1):
        #extract the subsequence of letters corresponding to the current key length
        nth_subseq = getNthSubkeysLetters(i, keylen, ciphertext)
        #compute the IC of the subsequence and add it to the total IC
        total_ic += stringIC(nth_subseq)
    
    return total_ic / keylen


def keyLengthIC(ciphertext: str, n: int) -> list:
    """
    Return the top n keylengths ordered by likelihood of correctness
    Assumes keylength <= 20
    """
    #compute the subsedIC for each
    #store both the key length and its score 
    #sort by:
     # higher ic first 
     # if tie, shorter key length first
    # return the top n key lengths
    #assignment says to test key lengths from 1 to 20

    scores = []

    for keylen in range(1, 21):
        average_ic = subseqIC(ciphertext, keylen)
        scores.append((keylen, average_ic))
    
    #sort the scores
    scores.sort(key=lambda x: (-x[1], x[0]))

    return [keylen for keylen, _ in scores[:n]]


def getNthSubkeysLetters(nth: int, keyLength: int, message: str):
    # Returns every nth letter for each keyLength set of letters in text.
    # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'

    # Use a regular expression to remove non-letters from the message:
    message = re.compile('[^A-Z]').sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def test():
    "Run tests"
    assert stringIC("ABA") == 1 / 3
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    assert stringIC("A") == 0.0
    assert stringIC("AA") == 1.0
    assert stringIC("AB") == 0.0
    assert stringIC("ABA") == 1/3

    sample = "PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA"
    assert subseqIC(sample, 3) == 0.03882783882783883
    assert subseqIC(sample, 4) == 0.0601010101010101
    assert subseqIC(sample, 5) == 0.012698412698412698

    sample2 = ("PPQCAXQVEKGYBNKMAZUYBNGBALJONITSZMJYIMVRAG"
               "VOHTVRAUCTKSGDDWUOXITLAZUVAVVRAZCVKBQPIWPOU")
    assert keyLengthIC(sample2, 5) == [8, 16, 4, 12, 6]

# Invoke test() if called via `python3 a7p234.py`
# but not if `python3 -i a7p234.py` or `from a7p234 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
