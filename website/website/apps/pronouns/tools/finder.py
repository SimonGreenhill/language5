
try:
    import Levenshtein
except ImportError:
    raise ImportError("Please install python-levenstein: https://github.com/miohtama/python-Levenshtein/tree/")

SCORE_IDENTITY = 1.0             # the score for total identity
SCORE_SUBSTRING = 0.9            # the score for prefixes or suffixes
SCORE_SIMILARITY_THRESHOLD = 0.6 # maximum value that we can give to similar things
SCORE_EMPTY = 0.0                # the score for a missing entry

class PronounFinder(object):
    
    def splitword(self, word):
        """Splits combined words into lists"""
        return [w.strip() for w in word.split(",")]
        
    def distance(self, s1, s2):
        """
        Calculates distance between two strings.
        """
        # empty strings in either side score SCORE_EMPTY
        if len(s1) == 0 or len(s1) == 0:
            return SCORE_EMPTY
        # complete identity gets SCORE_IDENTITY
        elif s1 == s2:
            return SCORE_IDENTITY
        
        # substrings score SCORE_SUBSTRING
        elif s1.startswith(s2) or s2.startswith(s1):
            return SCORE_SUBSTRING
        
        else:
            # otherwise a value between 0.0 and SCORE_SIMILARITY_THRESHOLD
            score = Levenshtein.distance(s1, s2)
        
            # normalise by the longest word
            wlen = max(len(s1), len(s2))
            score = float(score) / float(wlen)
            # convert to similarity rather than distance
            score = 1 - score
            return score * SCORE_SIMILARITY_THRESHOLD
        
        
    def compare(self, string1, string2):
        """Compares two strings. Returns the maximum similarity"""
        # empty strings in either side score SCORE_EMPTY
        if len(string1) == 0 or len(string2) == 0:
            return SCORE_EMPTY
        
        string1, string2 = self.splitword(string1), self.splitword(string2)
        
        similarities = []
        for s1 in string1:
            for s2 in string2:
                d = self.distance(s1, s2)
                similarities.append(self.distance(s1,s2))
        return max(similarities)
