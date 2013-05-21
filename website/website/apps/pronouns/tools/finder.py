
try:
    import Levenshtein
except ImportError:
    raise ImportError("Please install python-levenstein: https://github.com/miohtama/python-Levenshtein/tree/")

SCORE_IDENTITY = 1.0             # the score for total identity
SCORE_SUBSTRING = 0.9            # the score for prefixes or suffixes
SCORE_SIMILARITY_THRESHOLD = 0.6 # maximum value that we can give to similar things
SCORE_EMPTY = 0.0                # the score for a missing entry

class PronounFinder(object):
    
    def compare(self, string1, string2):
        
        # empty strings in either side score SCORE_EMPTY
        if len(string1) == 0 or len(string2) == 0:
            return SCORE_EMPTY
        
        # complete identity gets SCORE_IDENTITY
        if string1 == string2:
            return SCORE_IDENTITY
        
        # substrings score SCORE_SUBSTRING
        if string1.startswith(string2) or string2.startswith(string1):
            return SCORE_SUBSTRING
        
        # otherwise a value between 0.0 and SCORE_SIMILARITY_THRESHOLD
        score = Levenshtein.distance(string1, string2)
        
        # normalise by the longest word
        wlen = max(len(string1), len(string2))
        score = float(score) / float(wlen)
        
        # convert to similarity rather than distance
        score = 1 - score
        
        return score * SCORE_SIMILARITY_THRESHOLD
