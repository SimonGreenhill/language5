# raw entry - slug
# NOTE: Should all be lowercase
# remove ALL  and , find_synonym will nuke these too.

# CAREFUL WITH:
#   'palm' ==> palm-of-hand or the plant?
#   'tear' ==> 'to tear' or 'tears'

SYNONYMS = {
    'bird fly': 'to-fly',
    'bird\'s tail': 'tail',
    'dog tail': 'tail',
    'dog\'s tail': 'tail',
    'housefly': 'fly-sp',
    'person old': 'old',
    'skin swell up': 'to-swell',
    'tree top': 'tree-top',
    'tree trunk': 'trunk',
    'water cold': 'cold',
    'water hot': 'hot',
    'wind blow': 'to-blow',
    'ashes black': 'ashes',
    'bandicoot n': 'bandicoot',
    'bathe itr': 'to-bathe',
    'bathe cf water': 'to-bathe',
    'be afraid': 'afraid',
    'be': 'to-be',
    'be': 'to-be',
    'belly/guts': 'guts',
    'betel nut': 'betelnut',
    'betel pepper vine': 'betelpepper',
    'betelpepper vine': 'betelpepper',
    'betelpepper': 'betelpepper',
    'blow on fire': 'to-blow',
    'blow on': 'to-blow',
    'body-part affix': 'affix-body-part',
    'body-part suffix':'affix-body-part',
    'bowstr': 'bowstring',
    'brain': 'brains',
    'breadfruit n': 'breadfruit',
    'break wood': 'to-break',
    'buy': 'to-buy-sell-barter',
    'cassowary n': 'cassowary',
    'centipede n': 'centipede',
    'chop with axe': 'to-chop',
    'chop': 'to-chop',
    'clay pan': 'pan',
    'coconut n': 'coconut',
    'coconut tree': 'coconut-palm',
    'cooked kaukau': 'cooked',
    'cut with knife': 'to-cut',
    'cut with knife': 'to-cut',
    'dance vi': 'to-dance',
    'day-break': 'daybreak',
    'draw water': 'draw-water-carry',
    'dream v': 'to-dream',
    'excrement': 'faeces',
    'face forehead': 'face-forehead',
    'fall tree': 'to-fall',
    'fall from height': 'to-fall',
    'fall over': 'to-fall',
    'fell a tree': 'fell-tree',
    'fell tree': 'fell-tree',
    'fight, hit': 'to-fight',
    'fill up water': 'to-fill',
    'fill up': 'to-fill',
    'fl.fox': 'flying-fox',
    'fly insect': 'fly-sp',
    'fly n': 'fly-sp',
    'fly v': 'to-fly',
    'fly verb': 'to-fly',
    'fly n': 'fly-sp',
    'fly v': 'to-fly',
    'forest, woods': 'forest',
    'garden n': 'garden',
    'go vi': 'to-go',
    'go down vi': 'to-go-down',
    'grass skirt': 'skirt',
    'green coconut': 'coconut',
    'hand drum': 'drum',
    'how many?': 'how-many',
    'how?': 'how',
    'hungry': 'to-be-hungry',
    'inside-the-house': 'in',
    'intestines': 'guts',
    'jaw/chin': 'chin-jaw',
    'kill person': 'to-kill',
    'kill pig': 'to-kill',
    'kunai grass': 'kunai',
    'alang alang grass': 'kunai',
    'left arm': 'left-arm',
    'left hand': 'left-hand',
    'leg-upper': 'thigh',
    'light of fire': 'firelight',
    'light weight': 'light',
    'look for': 'to-look',
    'lung': 'lungs',
    'make': 'to-do-make',
    'male, man': 'man',
    'man, male': 'man',
    'mountn': 'mountain',
    'neck, back of': 'nape',
    'netbag': 'net-bag',
    'no': 'no-not',
    'old house': 'old',
    'old man': 'old',
    'old of humans': 'old',
    'old of objects': 'old',
    'old person': 'old',
    'paddle n.': 'paddle',
    'piece of wood': 'short-piece-wood',
    'plant v': 'to-plant',
    'possum ground': 'ground-possum',
    'possum tree' : 'tree-possum',
    'pulpul': 'cloth-clothes',
    'right arm': 'right-arm',
    'right hand': 'right-hand',
    'ripe adj': 'ripe',
    'ripe banana adj': 'ripe',
    'ripe coconut': 'coconut',
    'rope-of-bow': 'bowstring',
    's/he': 'he-she',
    'sago n': 'sago',
    'salt sea?': 'salt',
    'saucepan': 'pan',
    'scratch skin': 'to-scratch',
    'see tr': 'to-see',
    'see, watch.ITR': 'to-see',
    'shame': 'ashamed',
    'shrub-tanget': 'tanket',
    'sick': 'to-be-sick',
    'sit down': 'to-sit',
    'sit down': 'to-sit',
    'slowly': 'slow',
    'smell v': 'to-smell',
    'sole': 'sole-of-foot',
    'sore': 'sore-wound',
    'spear n': 'spear-n',
    'stand up': 'to-stand',
    'story n': 'story',
    'string/rope': 'rope',
    'stump of tree': 'stump',
    'stump tree': 'stump',
    'sugar cane': 'sugarcane',
    'swell v.': 'to-swell',
    'swell up': 'to-swell',
    'tail animals': 'tail',
    'tail bird': 'tail',
    'tail birds': 'tail',
    'tail of bird': 'tail',
    'tail of dog': 'tail',
    'tanget': 'tanket',
    'tangget': 'tanket', # WTF
    'tear': 'tears',
    'throw stone': 'to-throw',
    'thundering': 'thunder',
    'to be': 'to-be',
    'to buy': 'to-buy-sell-barter',
    'top of tree': 'tree-top',
    'tree possum, cuscus': 'tree-possum',
    'trunk-of-tree': 'trunk',
    'tree trunk': 'trunk',
    'trunk tree': 'trunk',
    'turn oneself': 'to-turn',
    'turn v.': 'to-turn',
    'upper leg': 'thigh',
    'wash s.t.': 'to-wash',
    'wash tr': 'to-wash',
    'watch itr': 'to-watch',
    'we incl': 'we-incl',
    'weep': 'to-cry',
    'what?': 'what',
    'when?': 'when',
    'where?': 'where',
    'who?': 'who',
    'wing n.': 'wing',
    'woman, female': 'woman',
    'woman/female': 'woman',
    'womens clothes': 'cloth-clothes',
    'wooden plate': 'plate',
    'woods': 'forest',
    'work n': 'work-n',
    'work': 'work-n',
    'yam dioscorea esculenta': 'yam',
    'yesterday/tomorrow': 'yesterday-tomorrow',
    'young boy': 'child',
    'young girl': 'child',
    'young person': 'child',
    
    'breast woman': 'breast',
}

# VERBS
SYNONYMS.update({
    'be afraid': 'afraid',
    'be sick': 'to-be-sick',
    'boil': 'to-boil',
    'break across': 'to-break',
    'burn': 'to-burn',
    'bury': 'to-bury',
    'call out': 'to-call-out',
    'come': 'to-come',
    'cry': 'to-cry',
    'dance': 'to-dance',
    'die': 'to-die',
    'dig': 'to-dig',
    'eat': 'to-eat',
    'give': 'to-give',
    'go down': 'to-go-down',
    'go up': 'to-go-up',
    'hear': 'to-hear',
    'hold': 'to-hold',
    'jump': 'to-jump',
    'kill': 'to-kill',
    'laugh': 'to-laugh',
    'pour out': 'to-pour-out',
    'pull': 'to-pull',
    'push': 'to-push',
    'put': 'to-put',
    'roast': 'to-roast',
    'run': 'to-run',
    'sharpen': 'to-sharpen',
    'shoot': 'to-shoot',
    'sleep': 'to-sleep',
    'smell': 'to-smell',
    'split': 'to-split',
    'stand': 'to-stand',
    'swallow': 'to-swallow',
    'sweat': 'to-sweat',
    'swell': 'to-swell',
    'take': 'to-take',
    'think': 'to-think',
    'throw': 'to-throw',
    'to chop, cut down': 'to-chop',
    'to be afraid': 'afraid',
    'to chop cut down': 'to-chop',
    'vomit': 'to-vomit',
    'walk': 'to-walk',
    'stomach/guts': 'guts',
    'stomach-guts': 'guts',
    'stomach (guts)': 'guts',
})






# KIN TERMS
SYNONYMS.update({
    
    # age only
    'older sibling': 'sibling-older',
    'younger sibling': 'sibling-younger',
    
    # opposite sex
    'cross-sibling':'sibling-opposite-sex',
    'cross-sibling, younger':  'sibling-opposite-sex-younger',
    'sibling-ds-younger': 'sibling-opposite-sex-younger',
    'older cross-sibling': 'sibling-opposite-sex-older',
    'older o.s. sibling': 'sibling-opposite-sex-older',
    'sib.x.s. older': 'sibling-opposite-sex-older',
    'sibling os': 'sibling-opposite-sex',
    'older cross-sex sib': 'sibling-opposite-sex-older',
    'sibling ds older': 'sibling-opposite-sex-older',

    # same sex
    'old sssib': 'sibling-same-sex-older',
    'sibling-ss-older': 'sibling-same-sex-older',
    'sibling, older same-sex': 'sibling-same-sex-older',
    'older s.s. sibling': 'sibling-same-sex-older',
    'older sss': 'sibling-same-sex-older',
    'sib.s.s. older': 'sibling-same-sex-older',
    'sib.s.s. younger': 'sibling-same-sex-younger',
    'sibling ss younger': 'sibling-same-sex-younger',
    'sib.s.s.': 'sibling-same-sex',
    'sibling ss': 'sibling-same-sex',
    'yngr sss': 'sibling-same-sex-younger',
    'younger s.s. sibling': 'sibling-same-sex-younger',
})




# PRONOUNS
SYNONYMS.update({
    # 1SG
    '1sg free': 'i',
    '1sg.free': 'i',
    '1st person singular': 'i',
    'd:1s': 'i',
    
    # 1 PL: we
    '1pl free': 'we', 
    'd:1p': 'we',
    '1st person plural': 'we',
    
    # 2 SG: you -- thou
    'd:2s': 'you',
    '2sg free': 'you',
    '2 sing. subject': 'you',
    '2sg': 'you',
    'you 2sg': 'you',
    '2sg pron': 'you',
    
    # 2 SG POSS: your
    '2 sing. poss.': 'your-sg',
    
    # 2 PL: you
    '2pl free': 'you-pl',
    'd:2p': 'you-pl',
    'ye': 'you-pl',
    
    # 3 SG: he/she/it
    '3sg': 'he-she',
    '3sg free': 'he-she',
    '3sg.free': 'he-she',
    'd:3s': 'he-she',
    '3rd person singular subj.': "he-she",
    
    # 3 SG POSS: his/hers
    '3sg poss.': 'his',
    '3rd singular possessive': 'his',
    '3rd singular possessive': 'his',
    
    # 3 PL: they
    '3pl free': 'they',
    '3pl.free': 'they',
    'd:3p': 'they',
    
})


SYNONYMS.update({
    
    # to-carry
    'carry on shoulder': 'to-carry',
    'carry on back': 'to-carry',
    'carry on shoulder': 'to-carry',
    
    # drum types:
    'drum signal': 'drum',
    'drum hand': 'drum',
    'handdrum': 'drum',
    'hand drum': 'drum',
    'signal drum': 'drum',
    
    # talk
    'talk to s\'one': 'to-talk',
    'talk v.': 'to-talk',
    'talk to tr': 'to-talk',
    'talk itr': 'to-talk',
    'talk tr': 'to-talk',
    
})

SYNONYMS.update(
    dict([
        (k.replace(" ", "-"),v) for (k,v) in SYNONYMS.items() if k.replace(" ", "-") not in SYNONYMS
        ])
)

def find_synonym(var):
    # simple match
    if var in SYNONYMS:
        return SYNONYMS[var]
    # check cleaned
    for k in '(),':
        var = var.replace(k, "")
    
    if var in SYNONYMS:
        return SYNONYMS[var]
    # check slugified
    var = var.replace(" ", "-")
    if var in SYNONYMS:
        return SYNONYMS[var]
    
    # nothing
    return None
