from collections import defaultdict
import numpy as np

# THIS IS A STUB YOU NEED TO COMPLETE THIS IMPLEMENTATION
#
# Find first occurence of each symbol in
# the first column of the sorted rotation matrix
# corresponding to bwt
#
# Input:
#   bwt: string with Burrows-Wheeler transform
#
# Output:
#   a function f such that f(symbol) is the index of the first
#   location of symbol in first column of rotation matrix for bwt
def _get_first_occurence_fn(bwt):
    first_occurences = dict()
    # find first occurrence of each symbol in the
    # first column of rotation table

    # YOU NEED TO FILL THIS IN
    
    sorted_bwt = sorted(bwt) # sort to get the first column of table
    
    for symbol in sorted_bwt:
        first_occurences[symbol] = sorted_bwt.index(symbol)
    
    # return function that returns first occurrence
    # for a given symbol
    def fn(symbol):
        return first_occurences[symbol]
    return fn

# THIS IS A STUB, YOU NEED TO COMPLETE THIS IMPLEMENTATION
#
# compute the count table for given BWT
#
# Input:
#   bwt: string with Burrows-Wheeler transform
#
# Output:
#   a function f that returns pre-computed occurrence count
#   such that f(symbol, position) gives the number of occurences
#   of symbol up to given position in bwt
def _get_count_fn(bwt):
    # figure out symbols occuring in bwt
    counter = defaultdict(int)
    for c in bwt:
        counter[c] += 1
    symbols = counter.keys()

    # allocate count table
    count = np.zeros((len(bwt)+1, len(symbols)), dtype=np.int32)

    # fill in count table with running count
    # of occurence counts, at the end
    # count[position, index] has the number of
    # occurrences in bwt up to `position` of symbol
    # corresponding to column `index`, see below

    # YOU NEED TO FILL THIS IN
    for i in range(len(bwt)):
        n = i+1 # use n since rows are offset by 1 to include a zero row on top
        
        # set this row's count to previous rows before incrementing
        for j in range(len(symbols)):   
            count[n][j] = count[n-1][j]

            # add count for symbol to index in this row 
            count[n][symbols.index(bwt[i])] = count[n-1][symbols.index(bwt[i])] + 1
            

    # set last row of table 
    for j in range(len(symbols)):   
            count[-1][j] = count[-2][j]

    # return function that return precomputed count
    # i.e., number of occurrences of `symbol`
    # up to `position` in bwt
    def fn(symbol, position):
        index = symbols.index(symbol)
        return count[position, index]
    return fn
