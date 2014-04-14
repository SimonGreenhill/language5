#!/usr/bin/env python
import reversion
from django.contrib.auth.models import User

# import models
from website.apps.core.models import Source
from website.apps.lexicon.models import Word, Lexicon

data = """
franklin1975 leg-foot  leg, foot
shaw-1973 warm 10  warm
franklin-1973-b warm 9 warm
brown-1973 warm 9  warm
lloyd-1973 warm 12 warm
franklin-and-voorhoeve-1973 warm 7 warm
macdonald-1973 warm 7  warm
wurm-1973 warm 14  warm 
shaw-1973 to-die 10  dies
franklin-1973-b to-die 9 dies
brown-1973 to-die 9  dies
lloyd-1973 to-die 12 dies
franklin-and-voorhoeve-1973 to-die 7 dies
macdonald-1973 to-die 7  dies
wurm-1973 to-die 14  dies
reesink-1976 neck 6      "neck (nape)"
reesink-1976 road 5  "path"
reesink-1976 to-give 5   "give (to me)"
reesink-1976 to-fly 5    "flies"
reesink-1976 to-burn 7   (int.)
reesink-1976 to-kill 5   "kills"
reesink-1976 to-die 7    "dies"
shaw-1973 to-kill 10  kills
franklin-1973-b to-kill 9 kills
brown-1973 to-kill 9  kills
lloyd-1973 to-kill 12 kills
franklin-and-voorhoeve-1973 to-kill 7 kills
macdonald-1973 to-kill 7  kills
wurm-1973 to-kill 14  kills
shaw-1973 to-fly 10  flies
franklin-1973-b to-fly 9 flies
brown-1973 to-fly 9  flies
lloyd-1973 to-fly 12 flies
franklin-and-voorhoeve-1973 to-fly 7 flies
macdonald-1973 to-fly 7  flies
wurm-1973 to-fly 14  flies
shaw-1973 to-know 10  knows
franklin-1973-b to-know 9 knows
brown-1973 to-know 9  knows
lloyd-1973 to-know 12 knows
franklin-and-voorhoeve-1973 to-know 7 knows
macdonald-1973 to-know 7  knows
wurm-1973 to-know 14  knows
thomson1975 to-chop-cut-down 9   "chop wood"
bromley-1967 to-see 1         you saw us
bromley-1967 lips 1           lips
bromley-1967 belly 7  belly (my)
bromley-1967 bone 7   bone (my)
bromley-1967 dry 7    dry (leaf)
bromley-1967 eye 7    egg (my)
bromley-1967 ear 7    ear (my)
bromley-1967 hair 7   (my)
bromley-1967 to-give 7    give (me)!
bromley-1967 head 7   head (my)
bromley-1967 to-kill 7    kill! (2s)
bromley-1967 to-know 15   I know
bromley-1967 louse 8  louse (my)
bromley-1967 meat 7   meat (lean)
bromley-1967 mouth 6  mouth (my)
bromley-1967 neck 7   neck (my)
bromley-1967 nose 7   nose (my)
bromley-1967 seed 7   seed (plant)
bromley-1967 across 8     across (stream)
bromley-1967 gourd-mans 7 gourd (man's)
bromley-1967 navel 6  navel (my)
bromley-1967 animal 7     wild animal
bromley-1967 heart 7      heart (my)
bromley-1967 knee 7       knee (my)
bromley-1967 leg-foot 7   foot (my)
bromley-1967 liver 7      liver (my)
bromley-1967 skin 7       skin (my)
bromley-1967 to-sleep 7       sleep! (2s)
bromley-1967 to-sit 7     sit! (2s)
bromley-1967 to-stand 7   stand! (2s)
bromley-1967 to-swim 8    swim! (2s)
bromley-1967 tongue 7     tongue (my)
bromley-1967 tooth 8      tooth (my)
bromley-1967 tree 7       tree (wood)
bromley-1967 to-walk 8        walk (go!)
bromley-1967 to-bite 6        bite (bit me)
bromley-1967 to-burn 7        burn (me)
bromley-1967 to-come 7        come! (2s)
bromley-1967 to-drink 7       drink! (2s)
bromley-1967 to-eat 7     eat! (2s)
bromley-1967 to-die 8         died (3s)
bromley-1967 to-fly 7     flying
bromley-1967 to-hear 7        I heard
bromley-1967 to-lie-down 7    lie down! 
bromley-1967 to-speak 7       speak! (2s)
bromley-1967 to-look 6        look! (2s)
trefry-1969 rope 2        rope (vine)
trefry-1969 to-lie-down 2     lie
larson-larson-1972 to-give 3   give me
larson-larson-1972 to-kill 4     kill me
larson-larson-1972 not 3     "not, no"
larson-larson-1972 to-walk 3        "walk, go"
larson-larson-1972 to-die 3      "die"
larson-larson-1972 to-know 3     "know"
larson-larson-1972 to-see 3  "see"
larson-larson-1972 to-stand 3    "stand"
larson-larson-1972 to-bite 4     "to bite"
larson-larson-1972 to-sleep 3    "sleep"
miedema-welling-1985 thou 1  "you (sg.)"
miedema-welling-1985 you-pl 11  "you (pl.)"
miedema-welling-1985 you-sg 11   "you (sg.)"
shaw-1986 you 24     "you"
shaw-1986 to-fly 24     "flies"
shaw-1986 to-kill 23 "kills"
foley1986 to-pound 6     "to pound sago"
foley1986 to-wash 6      "to wash sago"
voorhoeve-1975 thou 149  "you (sg.)"
voorhoeve-1975 you 116   "you (pl.)"
voorhoeve-1971 to-walk 19    "walk, go"
voorhoeve-1971 leg-foot 23       "foot, leg"
voorhoeve-1971 fingernail 22     "nail"
voorhoeve-1971 neck 12       "neck (nape)"
voorhoeve-1971 fly-sp 22     "housefly"
voorhoeve-1971 faeces 12         "excreta"
voorhoeve-1971 road 17       "road/path"
thomson1975 dull 9   "blunt"
thomson1975 short-piece-wood 9   "piece of wood"
thomson1975 to-understand 9      "understand (language)"
thomson1975 with 9       "together with"
thomson1975 far 9        "distant"
thomson1975 draw-water-carry 9   "draw water"
thomson1975 to-tie 9     "tie (rope)"
thomson1975 to-cut 9     "cut (rope)"
thomson1975 to-carry 9   "carry on shoulder"
thomson1975 to-put 9     "put down"
thomson1975 boy 9    "young boy"
thomson1975 to-look 9       "look for"
thomson1975 hair 9       "hair of head"
thomson1975 rotten 9     "rotten house"
thomson1975 sore-wound 9     "sore"
thomson1975 road 9       "path"
thomson1975 tail 9       "tail (of dog)"
thomson1975 fur 9    "fur (of dog)"
thomson1975 rope 9   "string, rope"
thomson1975 cloth-clothes 9  "woman's clothes"
thomson1975 to-sing 9    "singsing (v.)"
thomson1975 song 9       "singsing (=song)"
thomson1975 hot 9    "hot (of water)"
thomson1975 cold 9   "cold (of water)"
thomson1975 full 9   "full (of water)"
thomson1975 old 9        "old house"
thomson1975 to-wash 9        "wash oneself"
stokhof-1975 chin-jaw 35 "jaw, chin"
stokhof-1975 face-forehead 38    "forehead, face"
davies_and_comrie1985 fat-grease 22  "fat (grease)"
mcelhanon-1967 cloth-clothes 14  "clothing"

"""

# get editor
ed = User.objects.get(pk=1)

for line in data.split("\n"):
    line = line.strip()
    if len(line) > 0:
        try:
            source_slug, old_word_slug, n, comment = line.split(" ", 3)
        except:
            print("ERROR on LINE: %s" % line)
            raise
        
        comment = comment.strip().strip('"')
        
        SObj = Source.objects.get(slug=source_slug)
        WObj = Word.objects.get(slug=old_word_slug)
        print("%s  -> %s" % (SObj, WObj))
        lexica = Lexicon.objects.filter(source=SObj).filter(word=WObj)
        for lex in lexica:
            with reversion.create_revision():
                # update annotation
                if lex.annotation is None or len(lex.annotation) == 0:
                    lex.annotation = comment 
                    
                # set source gloss
                lex.source_gloss = comment
                
                print('  >> %5d \t %20s \t %20s' % (lex.id, lex.annotation, lex.source_gloss))
                lex.save()
