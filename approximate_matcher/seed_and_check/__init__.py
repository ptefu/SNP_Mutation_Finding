# THIS IS A STUB, YOU NEED TO IMPLEMENT THIS
#
# divide pattern into non-overlapping seed k-mers, such that
# exact matches of each seed, would yield a candidate approximate
# match within d mismatches.
#
# Input:
#   pattern: a query string
#   d: maximum number of mismatches to allow in approximate match
#
# Output:
#   tuple (seeds, k):
#       seeds: array of strings, contains seed non-overlapping k-mers obtained from pattern
#       k: overlapping k-mer length
def _make_seeds(pattern, d):
    k = (len(pattern)/(d+1))
    strings = []

    # add d seeds of length k to strings list
    for i in range(d):
        j = i*k
        strings.append(pattern[j:j+k])

    # add last seed of length >= k to position d+1 in strings list
    strings.append(pattern[d*k:])

    return strings, k

# THIS IS A STUB, YOU NEED TO IMPLEMENT THIS
#
# checks if pattern is within d mismatches of target
#
# Input:
#   pattern: string, query string
#   target: string, target string
#   d: minimum number of mismatches
def _within_edit_distance(pattern, target, d):
    if len(pattern) > len(target):  # false if len(pattern)>len(target)
        return False
    mismatches = 0                  # count mismatch
    for i in range(len(pattern)):   # check each pos for mismatch
        if pattern[i] != target[i]:
            mismatches += 1         # inc if mismatch
    if mismatches > d:              # return appropriate boolean
        return False
    else:
        return True

# class encapsulating the seed-and-check strategy
# for approximate matching
#
# Fields:
#   _seeds: [str], list of seeds created given minimum number of mismatches d
#   _k: int, seed k-mer length
#   _candidates: [int], indices of candidate approximate matches
#   _d: int, minimum edit distance for approximate matches
#   _pattern: str, the query string
class SeedChecker:
    def __init__(self, pattern, d):
        self._seeds, self._k = _make_seeds(pattern, d)
        self._candidates = set(list())
        self._d = d
        self._pattern = pattern

    # generator for seed enumeration, yields (seed, seed_index)
    def enumerate(self):
        for i in xrange(len(self._seeds)):
            yield (self._seeds[i], i)

    # updates the array of candidate approximate matches
    # given exact matches for a given seed
    def add_candidates(self, matches, seed_index):
        # find where in the pattern the seed at given
        # seed index starts
        seed_start_position = seed_index * self._k
        # now offset each match accordingly so candidate match
        # corresponds to location where approximate match would start

        for match in matches:
            candidate_start_position = match - seed_start_position
            self._candidates.add(candidate_start_position)

    def filter_candidates(self, target):
        candidates = filter(lambda index: _within_edit_distance(self._pattern, target[index:], self._d),
                            self._candidates)

        return candidates
