#!/usr/bin/env python
from website.apps.lexicon.models import Word, Lexicon
from website.apps.lexicon.management.commands import mergeword


words = """
medial-sequential-suffix
having-finished-that-and-then-medial-sequential-suffix

brother
brother-1
brother-2
brother-same-sex
brother-elder

sister
sister-1
sister-2
sister-of-woman
sister-elder

brother-law
brother-in-law-same-sex
brother-in-law-to-woman

sister-law
sister-in-law-to-man
sister-in-law-to-woman

vagina
vulva

predicative-possessive-suffix
predictive-possessive-suffix

rope
vine-rope-string

root
rootspider

interrogative-particle
interrogative-particle-generally-suffixed-to-subject

face-forehead                            01629 face, forehead
face                                     00928 face
forehead                                 01645 forehead
forehead-face                            00828 forehead, face
his-forehead                             01846 his forehead
"""

def parse_words(words):
    
    def get_slug(s): return s.split(" ",1)[0].strip()
    
    out = []
    words = words.split("\n\n")
    for chunk in words:
        chunk = chunk.strip().split("\n")
        assert len(chunk) > 1
        destination = get_slug(chunk.pop(0))
        for source in chunk:
            source = get_slug(source)
            out.append((destination, source))
    return out

for destination, source in parse_words(words):
    print("%s <- %s" % (destination, source))
    # update annotation
    old = Word.objects.get(slug=source)
    for entry in old.lexicon_set.all():
        if not entry.annotation:
            entry.annotation = old.word
            entry.save()
        print "\t", repr(entry).ljust(30), entry.annotation
        
    # MOVE
    cmd = mergeword.Command()
    cmd.handle(destination, source, save=True)
