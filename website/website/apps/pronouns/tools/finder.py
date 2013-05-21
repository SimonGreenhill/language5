
try:
    import Levenshtein
except ImportError:
    raise ImportError("Please install python-levenstein: https://github.com/miohtama/python-Levenshtein/tree/")

class PronounFinder(object):
    
    def compare(self, string1, string2):
        if string1 == string2:
            # complete identity
            return 1.0
        if string1.startswith(string2) or string2.startswith(string1):
            # substrings score 0.8
            return 0.8
        
        # otherwise a value between 0.0 and 0.6
        score = Levenshtein.distance(string1, string2)
        
        # normalise by the longest word
        wlen = max(len(string1), len(string2))
        score = float(score) / float(wlen)
        
        # convert to similarity rather than distance
        score = 1 - score
        
        return score * 0.6
