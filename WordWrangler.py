# http://www.codeskulptor.org/#user42_fw1aSjptK6_11.py

"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"
codeskulptor.set_timeout(100)

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    result = []
    
    for word in list1:
        if word not in result:
            result.append(word)
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    
    for word in list1:
        if word in list2:
            result.append(word)
    return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    result = []
    copy1, copy2 = list1[:], list2[:]
    
    while min(copy1, copy2):
        if copy1[0] < copy2[0]:
            result.append(copy1[0])
            copy1.pop(0)
        else:
            result.append(copy2[0])
            copy2.pop(0)
            
    if copy1:
        result += copy1
    elif copy2:
        result += copy2
            
    return result
              
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    
    mid_point = int(len(list1)/2)
    
    return merge(merge_sort(list1[:mid_point]), merge_sort(list1[mid_point:]))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if not word:
        return [""]
    
    all_strings = []
    for string in gen_all_strings(word[1:]):
        for letter_idx in range(len(string) + 1):
            all_strings.append(string[letter_idx:] + word[0] + string[:letter_idx])
    
    return gen_all_strings(word[1:]) + all_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    word_file = urllib2.urlopen(url)
    
    all_words = []
    for line in word_file.readlines():
        all_words.append(line.strip())
    
    
    return all_words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()

##############################
"""
Provided code for Word Wrangler game
"""

import poc_wrangler_gui

class WordWrangler:
    """
    Game class for Word Wrangler
    """
    
    def __init__(self, word_list, remdup, intersect, mergesort, substrs):
        self._word_list = word_list
        self._subset_strings = []
        self._guessed_strings = []

        self._remove_duplicates = remdup
        self._intersect = intersect
        self._merge_sort = mergesort
        self._substrs = substrs

    def start_game(self, entered_word):
        """
        Start a new game of Word Wrangler
        """
        if entered_word not in self._word_list:
            print "Not a word"
            return
        
        strings = self._substrs(entered_word)
        sorted_strings = self._merge_sort(strings)
        all_strings = self._remove_duplicates(sorted_strings)
        self._subset_strings = self._intersect(self._word_list, all_strings)
        self._guessed_strings = []        
        for word in self._subset_strings:
            self._guessed_strings.append("*" * len(word))
        self.enter_guess(entered_word)           
        
    def enter_guess(self, guess):
        """
        Take an entered guess and update the game
        """        
        if ((guess in self._subset_strings) and 
            (guess not in self._guessed_strings)):
            guess_idx = self._subset_strings.index(guess)
            self._guessed_strings[guess_idx] = self._subset_strings[guess_idx]

    def peek(self, peek_index):
        """
        Exposed a word given in index into the list self._subset_strings
        """
        self.enter_guess(self._subset_strings[peek_index])
        
    def get_strings(self):
        """
        Return the list of strings for the GUI
        """
        return self._guessed_strings
    

def run_game(wrangler):
    """
    Start the game.
    """
    poc_wrangler_gui.run_gui(wrangler)
    
    
    

