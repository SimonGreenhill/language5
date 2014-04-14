#!/usr/bin/env python
import reversion
from django.contrib.auth.models import User

# import models
from website.apps.core.models import Source
from website.apps.lexicon.models import Word, Lexicon

data = """
voorhoeve-1970 leg-foot                     leg         --> leg
shaw-1973 arm-hand                          arm         --> arm
franklin-1973-b arm-hand                    arm         --> arm
brown-1973 arm-hand                         arm         --> arm
lloyd-1973 arm-hand                         arm         --> arm
franklin-and-voorhoeve-1973  arm-hand       arm         --> arm
macdonald-1973 arm-hand                     arm         --> arm
wurm-1973 arm-hand                          arm         --> arm
shaw-1973 arm-hand                          arm         --> arm
franklin-1973-b arm-hand                    arm         --> arm
brown-1973 arm-hand                         arm         --> arm
lloyd-1973 arm-hand                         arm         --> arm
franklin-and-voorhoeve-1973 arm-hand        arm         --> arm
macdonald-1973 arm-hand                     arm         --> arm
wurm-1973 arm-hand                          arm         --> arm
miedema-welling-1985 arm-hand               arm         --> arm
thomson1975 arm-hand                        arm         --> arm
trefry-1969 arm-hand                        hand        --> hand
stokhof-1975 arm-hand                       hand        --> hand
trefry-1969 fat-grease                      fat         --> fat
bromley-1967 fat-grease                     fat         --> fat
shaw-1973 fat-grease                        fat         --> fat
franklin-1973-b fat-grease                  fat         --> fat
brown-1973 fat-grease                       fat         --> fat
lloyd-1973 fat-grease                       fat         --> fat
franklin-and-voorhoeve-1973 fat-grease      fat         --> fat
macdonald-1973 fat-grease                   fat         --> fat
wurm-1973 fat-grease                        fat         --> fat
stokhof-1975 fat-grease                     fat         --> fat
trefry-1969 to-rain                         rain        --> rain
bromley-1967 to-rain                        rain        --> rain

trefry-1969 to-plant                        plant       --> plant
trefry-1969 to-close                        close       --> near
bromley-1967 arm-hand                       hand (my)   --> hand
bromley-1967 vagina                         vulva (3s)  --> vulva
trefry-1969 right-correct                   true        --> true
shaw-1973 road                              path      --> path
franklin-1973-b road                        path      --> path
brown-1973 road                             path      --> path
lloyd-1973 road                             path      --> path
franklin-and-voorhoeve-1973 road            path      --> path
macdonald-1973 road                         path      --> path
wurm-1973 road                              path      --> path
shaw-1973 to-rain                           rain      --> rain
franklin-1973-b to-rain                     rain      --> rain
brown-1973 to-rain                          rain      --> rain
lloyd-1973 to-rain                          rain      --> rain
franklin-and-voorhoeve-1973 to-rain         rain      --> rain
macdonald-1973 to-rain                      rain      --> rain
wurm-1973 to-rain                           rain      --> rain
shaw-1973 leg-foot                          leg      --> leg
franklin-1973-b leg-foot                    leg      --> leg
brown-1973 leg-foot                         leg      --> leg
lloyd-1973 leg-foot                         leg      --> leg
franklin-and-voorhoeve-1973 leg-foot        leg      --> leg
macdonald-1973 leg-foot                     leg      --> leg
wurm-1973 leg-foot                          leg      --> leg
shaw-1973 you                               you (sing.)      --> thou
franklin-1973-b you                         you (sing.)      --> thou
brown-1973 you                              you (sing.)      --> thou
lloyd-1973 you                              you (sing.)      --> thou
franklin-and-voorhoeve-1973 you             you (sing.)      --> thou
macdonald-1973 you                          you (sing.)      --> thou
wurm-1973 you                               you (sing.)      --> thou
larson-larson-1972 leg-foot                 foot             --> foot
larson-larson-1972 arm-hand                 hand             --> hand
larson-larson-1972 warm                     hot              --> hot
larson-larson-1972 to-rain                  rain             --> rain
larson-larson-1972 fat-grease               fat              --> fat
miedema-welling-1985 leg-foot               leg              --> leg
shaw-1986 to-rain                           rain             --> rain
shaw-1986 arm-hand                          arm              --> arm
shaw-1986 leg-foot                          leg              --> leg
shaw-1986 fat-grease                        fat              --> fat
shaw-1986 road                              path             --> path
shaw-1986 warm                              hot              --> hot
foley1986 leg-foot                          leg              --> leg
voorhoeve-1975 arm-hand                     arm   --> arm                    
voorhoeve-1975 leg-foot                     leg   --> leg
voorhoeve-1971 fat-grease                   fat   --> fat
voorhoeve-1971 to-rain                      rain --> rain
voorhoeve-1971 chin-jaw                     jaw   --> jaw
wilson-1969 arm-hand                        hand  --> hand
wilson-1969 leg-foot                        foot  --> foot
wilson-1969 to-rain                         rain  --> rain
thomson1975 face-forehead                   forehead --> forehead
thomson1975 leg-foot                        leg   --> leg
thomson1975 chin-jaw                        jaw   --> jaw
thomson1975 fat-grease                      fat   --> fat
reesink-1976 arm-hand                       arm   --> arm
reesink-1976 warm                           hot   --> hot
reesink-1976 leg-foot                       leg   --> leg
reesink-1976 fat-grease                     fat   --> fat
reesink-1976 to-rain                        rain  --> rain
                                            
heeschen-1978 leg-foot                      foot  --> foot
heeschen-1978 fat-grease                    fat   --> fat
heeschen-1978 green                         green, unripe --> unripe
heeschen-1978 arm-hand                      hand  --> hand
salisbury-1956 arm-hand                     hand  --> hand
salisbury-1956 fat-grease                   fat   --> fat
salisbury-1956 leg-foot                     leg   --> leg

davies_and_comrie1985 arm-hand              hand   --> hand
davies_and_comrie1985 face-forehead         his forehead --> forehead
davies_and_comrie1985 leg-foot              his leg    --> leg
scott1978 arm-hand                          hand   --> hand
scott1978 chin-jaw                          chin  --> chin
scott1978 face-forehead                     forehead --> forehead
scott1978 fat-grease                        fat   --> fat
saville1912 arm-hand                        hand   --> hand
taber1993 arm-hand                          hand --> hand
lang-1973 arm-hand                          hand --> hand
lang-1973 shy-ashamed                       shame --> ashamed
voorhoeve1982 arm-hand                      hand --> hand
visser-and-voorhoeve1987 arm-hand           hand --> hand
visser-and-voorhoeve1987 shy-ashamed        shame --> ashamed
pikkert-et-al1994 arm-hand                  hand  --> hand
xiao-1990 arm-hand                          hand --> hand
xiao-1990 leg-foot                          leg --> leg
franklin1975 arm-hand                       hand  --> hand
franklin1975 chin-jaw                       chin --> chin
franklin1975 face-forehead                  forehead --> forehead
franklin1975 painful-sick                   pain --> painful
mcelhanon-1967 fat-grease                   (its) fat --> fat
mcelhanon-1967 leg-foot                     (its) foot --> foot
"""

# get editor
ed = User.objects.get(pk=1)

for line in data.split("\n"):
    line = line.strip()
    if len(line) > 0:
        try:
            head, tail = line[0:40].strip(), line[40:].strip()
            source_slug, old_word_slug = head.split()
            comment, new_word_slug = [_.strip() for _ in tail.split("-->")]
        except:
            print("ERROR on LINE: %s" % line)
            raise
        
        print source_slug, old_word_slug, new_word_slug, comment
        SObj = Source.objects.get(slug=source_slug)
        oldWObj = Word.objects.get(slug=old_word_slug)
        try:
            newWObj = Word.objects.get(slug=new_word_slug)
        except Word.DoesNotExist:
            newWObj = Word.objects.create(
                word=new_word_slug,
                slug=new_word_slug,
                editor=ed
            )
            print("Created New Word: {}".format(newWObj))
            
        lexica = Lexicon.objects.filter(source=SObj).filter(word=oldWObj)
        for lex in lexica:
            with reversion.create_revision():
                # update annotation
                if lex.annotation is None or len(lex.annotation) == 0:
                    lex.annotation = comment 
                    
                # set source gloss
                lex.source_gloss = comment
                # update word
                lex.word = newWObj
                
                print 'Updated: >>', lex.id, lex.word
                lex.save()
                assert lex.word == newWObj

