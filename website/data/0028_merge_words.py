#!/usr/bin/env python
from website.apps.lexicon.models import Word, Lexicon
from website.apps.lexicon.management.commands import mergeword


words = """
three
threeone                                 01766 three/one

raw
uncooked                                 00892 uncooked

right-correct                            00157 right (correct)
true                                     00209 true

back
his-back                                 01844 his back

blood
his-blood                                01851 his blood

bone
his-bone                                 01850 his bone

father
his-father                               01852 his father


heart
his-heart                                01849 his heart


stomach
digestive-organ                          01615 digestive organ

to-talk
talkspeech                               01763 talk/speech

to-dream                                 01212 to dream
dream                                    01620 dream

fire                                     00022 fire
fire-firewood                            00830 fire, firewood
firewood                                 01220 firewood

food                                     01642 food
food-things                              01643 food, things

fish                                     00023 fish
fish-sp                                  01221 fish sp.

meat
fish-meat                                01638 fish, meat


to-dig                                   00114 to dig
to-dig-up                                00848 to dig up

to-cook                                  00239 to cook
cook-in-ground-on-hot-stones-mumu        00870 cook (in ground on hot stones), mumu

sugarcane                                sugarcane
sugar-cane                               sugar cane

ant                                      ant
ant-sp                                   ant sp.

arm-hand                                 arm, hand
hand                                     00029 hand
arm                                      arm
forearmhand                              (fore)arm/hand

ashes                                    ashes
ashes-awetu                              ashes *awetu/

forest
woods                                    00204 woods


berry                                    berry
berry-sp                                 berry sp.

to-carry                                 01202 to carry
to-carry-on-shoulder                     01203 to carry on shoulder

to-blow                                  to blow (wind)
blow                                     blow

faeces                                   faeces
excreta                                  excreta
feces                                    feces

dull                                     dull (knife)
blunt                                    blunt

to-speak                                 00217 to speak
speak                                    01752 speak

to-find                                  00251 to find
find                                     01636 find

to-fight                                 00123 to fight
fight                                    01635 fight

to-fear                                  00121 to fear
fear                                     01632 fear
to-be-afraid                             00800 to be afraid

drum                                     00244 drum
drum-tatamu                              01622 drum *tatamu/

to-drink                                 00073 to drink
drink                                    01894 drink

to-come                                  00071 to come
come                                     01599 come

boy                                      00232 boy
boy-male-child                           00876 boy, male child

to-break                                 00864 to break
break                                    01575 break

wet
liquidwet                                01680 liquid/wet

to-burn                                  00070 to burn (intrans.)
burn                                     01581 burn
it-burns                                 01860 it burns

to-catch                                 00906 to catch
catch                                    01891 catch

to-chew                                  00853 to chew
chew                                     01594 chew

to-cough                                 00796 to cough
cough                                    01893 cough

to-cry                                   00240 to cry
cry                                      01606 cry

to-dance                                 00242 to dance
dance                                    01609 dance

to-give                                  00076 to give
give                                     00297 give

to-grow                                  00257 to grow
grow                                     01653 grow

to-hear                                  00077 to hear
hear                                     01655 hear
he-hears                                 01858 he hears

to-hit                                   00136 to hit
hit                                      01656 hit
he-hits                                  01861 he hits

to-hold                                  00137 to hold (in hand)
hold                                     01657 hold

fly-sp                                   01640 fly sp.
housefly                                 01304 housefly
fly                                      00929 fly

to-fly                                   00075 to fly
fly-verb                                 01896 fly (verb)

sago                                     00942 sago
sagofood                                 01729 sago/food

to-sew                                   00166 to sew
sew                                      01733 sew
sew-spear-scratch                        01734 sew, spear, scratch
sew-weave                                01735 sew, weave

to-see                                   00083 to see
see                                      01732 see

shoulder                                 00299 shoulder
shoulder-blade                           01741 shoulder (blade)
his-shoulder                             01845 his shoulder

thumb
his-thumb                                01847 his thumb

shy-ashamed                              01918 shy, ashamed
shame                                    01737 shame

to-sit                                   00084 to sit
sit                                      01748 sit

snake                                    00173 snake
snake-land-sp                            01260 snake (land sp.)
snake-tree-sp                            01261 snake (tree sp.)


right-hand                               00158 right (hand)
righthand                                01724 righthand
right                                    01253 right

to-pull                                  00155 to pull
pull                                     01716 pull

stick                                    00180 stick (wood)
wood

to-split                                 00177 to split
split                                    00284 split
break-wood                               00819 break wood

to-say                                   00082 to say
say                                      01902 say
he-says                                  01857 he says

to-run                                   00838 to run
run                                      01728 run

to-rain                                  00081 to rain
rain                                     00215 rain

to-stand                                 00086 to stand
stand                                    01904 stand
stand-intrans                            01756 stand (intrans.)
stand-trans                              01755 stand (trans.)

to-sleep                                 00085 to sleep
sleep                                    01749 sleep

sun                                      00064 sun
sun-day                                  00816 sun, day
sunshine                                 00288 sunshine

to-sweat                                 01268 to sweat
sweat                                    00957 sweat
to-perspire-sweat                        00887 to perspire, sweat

to-swim                                  00087 to swim
swim                                     01761 swim

taro                                     00824 taro
taro-sp                                  01764 taro sp.

to-throw                                 00190 to throw
throw                                    01768 throw

to-tie                                   00191 to tie
tie                                      01769 tie

to-cut                                   00112 to cut
cut                                      01607 cut
to-cut-off                               01209 to cut off
cuttie                                   01608 cut/tie

to-die                                   00072 to die
die                                      01614 die
he-dies                                  01859 he dies
dead                                     00967 dead

he-she                                   01920 he, she
he
she

wash                                     01783 wash
to-wash                                  00212 to wash
wash-sago                                00337 wash sago

to-climb                                 01911 to climb
to-ascend                                00803 to ascend

road                                     00054 road/path
road-path                                01725 road, path
trail                                    01771 trail
path                                     01248 path

to-pound                                 01916 to pound
pound-sago                               00336 pound sago
to-pound-sago                            01251 to pound sago

pigeon                                   00975 pigeon
pigeon-sp                                01250 pigeon sp.

rafter                                   00998 rafter
rafters                                  01719 rafters

rat                                      00279 rat
rat-mouse                                01720 rat, mouse

to-know                                  00079 to know (facts)
know                                     01898 know

to-laugh                                 00145 to laugh
laugh                                    01899 laugh
he-laughs                                01862 he laughs


left-hand                                00146 left (hand)
lefthand                                 01674 lefthand

leg-foot                                 01675 leg, foot
leg                                      00147 leg
foot                                     00024 foot
his-leg                                  01848 his leg

garden                                   00799 garden
garden-work                              01647 garden, work

loincloth                                01681 loincloth
loincloth-shield                         01682 loincloth, shield

to-lie                                   00080 to lie down
lie                                      01676 lie

limestick                                01678 limestick
limestickpaddle                          01679 limestick/paddle

light                                    00268 light
light-not-heavy                          01677 light (not heavy)

knife                                    00267 knife
knife-small                              01669 knife (small)

to-kill                                  00078 to kill
kill                                     01897 kill

rib                                      00940 rib
ribs                                     01722 ribs

tree                                     00091 tree
tree-wood                                01772 tree, wood

chest                                    00973 chest
chestabdomen                             01593 chest/abdomen

chin-jaw                                 01595 chin, jaw
chin                                     01892 chin
jaw-chin                                 00811 jaw, chin

to-be-hungry                             00225 to be hungry
hungry                                   01663 hungry

to-be-sick                               00226 to be sick
sick                                     01744 sick
to-have-a-cold                           00237 to have a cold

to-urinate                               01281 to urinate
urinate                                  00889 urinate

to-eat                                   00074 to eat
eat                                      01625 eat

no-not                                   00888 no, not
no                                       01856 no

net-bag                                  01854 net bag
netbag                                   01900 netbag

mother                                   00149 mother
mother-ai                                01689 mother *ai,
his-mother                               01853 his mother

meat                                     00041 meat (flesh)
flesh                                    01223 flesh

to-fall                                  00118 to fall (drop rather than topple)
fall                                     01630 fall
fall-down                                01895 fall down

frog                                     00900 frog
frog-sp                                  01226 frog sp.

fat-grease                               01843 fat (grease)
fat                                      00020 fat

if                                       00142 if
if-when                                  00510 if, when ((conditional verb suffix))
if-when-conditional-verb-suffix          00854 if, when (conditional verb suffix)

warm                                     00093 warm/hot
warm-hot                                 01855 warm, hot

to-walk                                  00088 to walk
walk                                     01780 walk

ripe
dry-or-overripe-fruit                    01214 dry or overripe fruit
greenstale                               01651 green/stale

guts                                     00132 guts
internal-organ                           01666 internal organ
internal-organ-sweetfat                  01667 internal organ, sweet/fat
visceral-organ                           01778 visceral organ

dry                                      00015 dry (be dry)
dryhard                                  01623 dry/hard

fur
hair-fur-feathers                        00815 hair, fur, feathers
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
    cmd.handle(destination, source)
