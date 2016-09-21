from preprocess_bwt import _get_first_occurence_fn, _get_count_fn

# helper function to rotate a string
def rotate(l,n):
    return l[n:] + l[:n]

# THIS IS A STUB, YOU NEED TO IMPLEMENT THIS
#
# Construct the Burrows-Wheeler transform for given text
# also compute the suffix array
#
# Input:
#   text: a string (character `$` assumed to be last character)
#
# Output:
#   a tuple (bwt, suffix_array):
#       bwt: string containing the Burrows-Wheeler transform of text
#       suffix_array: the suffix array of text
def _construct(text):
    rotations = []                       # store the rotations of text
    bwt_string = ''                      # string containing bwt(text)
    pos = {}                             # dic containing pos of substring
    suffix_array = []                    # suffix array 
    
    for i in range(len(text)):          
        rotations.append(rotate(text,i)) # add each rotation
        pos[text[i:]] = i                # add each pos

    rotations = sorted(rotations)        # sort rotations lexicographically

    for word in rotations:               # add the last char in each word
        bwt_string += word[-1]
        
    for key, value in sorted(pos.items()):
        suffix_array.append(str(value))

    return bwt_string, suffix_array

# wrapper for the processing functions used to compute
# auxiliary data structures for efficient BWT matching
# see file `preprocess_bwt.py`
def _preprocess_bwt(bwt):
    first_occurence = _get_first_occurence_fn(bwt)
    count = _get_count_fn(bwt)
    return first_occurence, count

# class encapsulating exact matching with Burrows-Wheeler transform
#
# Fields:
#   _text: string, the target string
#   _bwt: string, the burrows-wheeler transform of target string
#   _suffix_array: [int], suffix array of target string
#   first_occurence: function returning first occurence of each symbol in
#                     first column of sorted rotation table for bwt, see below
#   count: function returning number of occurences of each symbol up to
#           a given position, see below
#
# Notes:
#   After initializing: `bwt = BWT(target)`:
#
#   `bwt.first_occurence(symbol)` returns the row in which symbol occurs first
#       in the first column of the sorted rotation table corresponding to the BWT
#       of target string
#
#   `bwt.count(symbol, position)` returns the number of occurrences of symbol
#       up to given position in BWT of target string
class BWT:
    def __init__(self, target):
        self._text = target
        self._bwt, self._suffix_array = _construct(self._text)
        self.first_occurence, self.count = _preprocess_bwt(self._bwt)
            
    # THIS IS A STUB, YOU NEED TO IMPLEMENT THIS
    #
    # return indices for positions in target string that match
    # query exactly
    #
    # Input:
    #   pattern: string, query string
    #
    # Output:
    #   [int], array of indices of exact matches of query in target
    #          array is empty if no exact matches found
    def get_matches(self, pattern):
        top, bottom = self._get_matching_rows(pattern)

        if top == -1:
            return []
        
        # return matching indices based on top and bottom pointers
        # YOU NEED TO FILL THIS IN
        indices = []
        for i in range(top, bottom+1):
            indices.append(int(self._suffix_array[i]))
            
        return indices

    # THIS IS A STUB, YOU NEED TO IMPLEMENT THIS
    #
    # return top, bottom pointers for rows of sorted rotations table
    # that start with query
    #
    # Input:
    #   pattern: string, query string
    #
    # Output:
    #   tuple (top, bottom): top and bottom pointers for consecutive rows in
    #       sorted rotations table that start with exact matches to query string
    #       returns (-1, -1) if no matches are found
    def _get_matching_rows(self, pattern):
        rev_pattern = pattern[::-1] # reverse pattern string
        sorted_bwt = sorted(self._bwt)

        # get the first occurence
        top = self.first_occurence(rev_pattern[0])

        # if the length of the string is 1, means rotations = 1
        # then just return the single
        if len(sorted_bwt) == 1:
            return top, top

        # set the bottom pointer to the last occurence in the consecutive rows
        bottom = 0
        for i in range(top, len(sorted_bwt)):
                if i == len(sorted_bwt)-1 or sorted_bwt[i+1] != sorted_bwt[top]:
                    bottom = i
                    break;
        # if the pattern has more than 1 char
        if len(pattern) > 1:
            # set B and E based on the concept from class/slides
            # get the count from the table
            B = self.count(rev_pattern[1], top)
            E = self.count(rev_pattern[1], bottom+1) # add 1 to bottom pointer to get right value
        # else return pointers around the 1 char
        else:
            return top, bottom

        # iterate through steps 3 & 4
        # updating top, bottom, B, and E
        for i in range(1,len(rev_pattern)):
            top = self.first_occurence(rev_pattern[i]) + B
            bottom = top - B + E - 1

            # if not reached end, keep going
            if (i != len(rev_pattern)-1):
                B = self.count(rev_pattern[i+1], top)
                E = self.count(rev_pattern[i+1], bottom+1)
            # else set the final pointers
	    else:
		top = self.first_occurence(rev_pattern[i]) + B
		bottom = top - B + E - 1

        # this accounts for the offset of 1 for the bottom pointer
        # since the bottom adjustment is hardcoded and this would
        # be a quick fix while maintaining the functionality/concept
	if top > bottom:    
            return top, top

        # otherwise return as normal
        return (top, bottom)

        # not necessary since empty list will be returned from get_matches if
        # not found anyway
        #return (-1, -1)









