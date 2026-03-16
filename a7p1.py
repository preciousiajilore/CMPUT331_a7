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
Assignment 7 Problem 1
"""

from sys import flags

def vigenereEncrypt(key: str, plaintext: str) -> str:
    """
    Encrypt the plaintext using the Vigenere cipher with the given key
    """
    ciphertext = ""
    for i, c in enumerate(plaintext):
        if c.isalpha():
            #c = (p + k) % 26
            #shift is the amount we need to shift the plaintext character to get the ciphertext character
            shift = ord(key[i % len(key)].upper()) - ord('A')

            encrypted_char = chr((ord(c.upper()) - ord('A') + shift) % 26 + ord('A'))
            ciphertext += encrypted_char
        else:
            ciphertext += c
    return ciphertext

def firstRepeatedTrigramIndex(s: str, start: int = 0) -> int:
    """
    Return the index of the first repeated trigram in the string s
    If there are no repeated trigrams, return -1
    """
    for i in range(start, len(s) - 2):
        trigram = s[i:i+3]
        if s.find(trigram, i + 1) != -1:
            return i
    return -1

def hasRepeatedTrigram(s: str) -> bool:
    for i in range(len(s) - 2):
        trigram = s[i:i+3]
        if s.find(trigram, i + 1) != -1:
            return True
    return False

 

def antiKasiski(key: str, plaintext: str) -> str:
    """
    given a key and plaintext, insert X characters into the plaintext so
    that after encryption there are no repeated trigrams in the ciphertext
    then return the ciphertext

    idea:
    if a trigram appears multiple times, insert an X right after the first occurrence of the trigram in the plaintext
    you inserted after a trigram starting at index i, do not go back and do insertions 
    for repeated subsequences whose first occurrence is before i
    Thwart Kasiski examination 
    """
    """
    Loop:
    1. Encrypt the plaintext using the key
    2. Find the first repeated trigram in the ciphertext
    3. Insert an X right after the first occurrence of the repeated trigram in the plaintext
    4. Re-encrypt
    5. Repeat until there are no repeated trigrams in the ciphertext
    """

    modified_plaintext = plaintext
    start_index = 0

    while True:
        #encrypt the modified plaintext
        ciphertext = vigenereEncrypt(key, modified_plaintext)
        #find the first repeated trigram in the ciphertext
        index = firstRepeatedTrigramIndex(ciphertext, start_index)
        if index == -1:
            #no repeated trigrams, we are done
            return ciphertext
        
        insert_index = index + 3 #insert after the first occurrence of the repeated trigram
        modified_plaintext = (
            modified_plaintext[:insert_index] + 'X' + modified_plaintext[insert_index:]
        )

        start_index = index



def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    # helper tests
    assert vigenereEncrypt("A", "HELLO") == "HELLO"
    assert vigenereEncrypt("B", "ABC") == "BCD"
    assert vigenereEncrypt("ABC", "THE") == "TIG"

    assert firstRepeatedTrigramIndex("ABCDEFG", 0) == -1
    assert firstRepeatedTrigramIndex("ABCDEFGABC", 0) == 0
    assert firstRepeatedTrigramIndex("TIGTIGXYZ", 0) == 0

    # exact sample test from assignment
    result1 = antiKasiski("ABC", "THETESTCASETHATHASTHEREPEAT")
    assert result1 == "TIGXUGSUEATGTICXUJATVHFTEQGAU"

    result2 = antiKasiski("ABC", "THECATTHEMOUSETHEDOG")
    assert result2 == "TIGXYEAUVHFOOVUEUJEEQG"

    # property checks
    assert not hasRepeatedTrigram(result1)
    assert not hasRepeatedTrigram(result2)

# Invoke test() if called via `python3 a7p1.py`
# but not if `python3 -i a7p1.py` or `from a7p1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
