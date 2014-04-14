#!/usr/bin/env python
import reversion
from django.contrib.auth.models import User

# import models
from website.apps.core.models import Source
from website.apps.lexicon.models import Word, Lexicon

data = """
28755 -> to-say
28865 -> to-say
29156 -> to-say
30057 -> to-say
30058 -> to-say
6075 + skin
6095 + skin
6133 + skin
6077 + to-eat
6098 + to-eat
6136 + to-eat
14987 + to-eat
14988 + to-eat
14989 + to-eat
14990 + to-eat
14991 + to-eat
14992 + to-eat
14993 + to-eat
14994 + to-eat
14995 + to-eat

14987 -> to-drink
14988 -> to-drink
14989 -> to-drink
14990 -> to-drink
14991 -> to-drink
14992 -> to-drink
14993 -> to-drink
14994 -> to-drink
14995 -> to-drink

86149 -> to-be-sick
86423 -> to-be-sick
86697 -> to-be-sick
86971 -> to-be-sick
87245 -> to-be-sick
87519 -> to-be-sick
87793 -> to-be-sick
88067 -> to-be-sick
88341 -> to-be-sick

86216 -> painful
86490 -> painful
86764 -> painful
87038 -> painful
87312 -> painful
87586 -> painful
87860 -> painful
88134 -> painful
88408 -> painful


86257 X //
86258 X //
86531 X //
86532 X //
86805 X //
86806 X //
87079 X //
87080 X //
87353 X //
87354 X //
87627 X //
87628 X //
87901 X //
87902 X //
88175 X //
88176 X //
88449 X //
88450 X //

86179 X //
86180 X //
86453 X //
86454 X //
86727 X //
86728 X //
87001 X //
87002 X //
87275 X //
87276 X //
87549 X //
87550 X //
87823 X //
87824 X //
88097 X //
88098 X //
88371 X //
88372 X //

86133 -> fly-sp
86407 -> fly-sp
86681 -> fly-sp
86955 -> fly-sp
87229 -> fly-sp
87503 -> fly-sp
87777 -> fly-sp
88051 -> fly-sp
88325 -> fly-sp

27200 -> you-sg
27406 -> you-sg
27098 -> you-sg
27510 -> you-sg
34218 -> you-sg
34219 -> you-sg
"""

# LEX ID  (action) gloss
#     + copy to gloss
#     -> move to gloss
#     X // split on "//" -> second half goes to annot.
#     

# get editor
ed = User.objects.get(pk=1)

for line in data.split("\n"):
    line = line.strip()
    if len(line) > 0:
        try:
            lex_id, token, word_slug = line.split(" ")
            lex_id = int(lex_id)
        except:
            print("ERROR on LINE: %s" % line)
            raise
        
        lex = Lexicon.objects.get(pk=lex_id)
        
        if token == '+':
            # COPY TO GLOSS
            with reversion.create_revision():
                WObj = Word.objects.get(slug=word_slug)
                Lexicon.objects.create(
                    language = lex.language, 
                    source = lex.source,
                    word = WObj,
                    entry = lex.entry,
                    source_gloss = lex.source_gloss,
                    annotation = lex.annotation,
                    editor=ed
                )
                print(' %s --> Copied to %s' % (line, WObj))
                lex.save()
        elif token == '->':
            # MOVE TO GLOSS
            with reversion.create_revision():
                WObj = Word.objects.get(slug=word_slug)
                lex.word == WObj
                print(' %s --> Updated Word to %s' % (line, WObj))
                lex.save()
        elif token == 'X':
            # chop entry on //
            assert "//" in lex.entry
            entry, annot = [_.strip() for _ in lex.entry.split("//")]
            with reversion.create_revision():
                lex.entry = entry
                lex.annotation = annot
                print(' %s --> Updated Entry & Annotation to %s | %s' % (line, lex.entry, lex.annotation))
                lex.save()
            