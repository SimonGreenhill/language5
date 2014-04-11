"""
Tools for creating string representations of various model create statements.
"""
import gzip
import json
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from website.apps.core.models import Source, Language, Family
from website.apps.lexicon.models import Word, Lexicon



class ABVDImporter(object):
    """Importer for ABVD database exports"""
    def __init__(self, filename, editor=None):
        self.editor = editor
        self.language = None
        self.source = None
        self.read(filename)
    
    def read(self, filename):
        if filename.endswith('.json.gz'):
            with gzip.open(filename, 'rb') as handle:
                self.data = json.loads(handle.read())
        elif filename.endswith('.json'):
            with open(filename, 'r') as handle:
                self.data = json.loads(handle.read())
        else:
            raise IOError("Unhandled filetype: {}".format(filename))
    
    def get_word_slug(self, word):
        """A little helper to catch some words and correct their slugs."""
        w = slugify(word)
        translate = {
            'in-inside': 'in',
            'to-sniff-smell': 'to-smell',
            'correct-true': 'right-correct',
            'fatgrease': 'fat-grease',
            'to-die-be-dead': 'to-die',
            'worm-earthworm' :'worm',
            'to-breathe': 'breathe',
            'earthsoil': 'earth',
            'intestines': 'guts',
            'ash': 'ashes',
            'bad-evil': 'bad',
            'left': 'left-hand',
            'to-cut-hack': 'to-cut',
            'woodsforest': 'woods',
            'to-know-be-knowledgeable': 'to-know',
            'to-live-be-alive': 'to-live',
            'to-pound-beat': 'to-pound',
            'stickwood': 'stick',
            'dull-blunt': 'dull',
            'to-buy': 'to-buy-sell-barter',
            'manmale': 'man',
            'meatflesh': 'meat',
            'thatchroof': 'thatch-roof',
            'heshe': 'he-she',
            'legfoot': 'leg-foot',
            'roadpath': 'road',
            'personhuman-being': 'person',
            'to-tie-up-fasten': 'to-tie',
            'to-stab-pierce': 'to-stab',
            'womanfemale': 'woman',
            'to-open-uncover': 'to-open',
            'to-lie-down': 'to-lie',
            
        }
        if w in translate:
            return translate[w]
        else:
            return w

        
    def install(self):
        self._process_language()
        self._process_source()
        self._process_entries()
    
    def _process_language(self):
        slug = slugify(self.data['language']['language'])
        try:
            self.language = Language.objects.get(slug=slug)
            print(u"Identified Language: {}".format(self.language))
        except Language.DoesNotExist:
            self.language = Language.objects.create(
                language=self.data['language'].get('language', ''), 
                slug=slug,
                dialect=self.data['language'].get('dialect', ''), 
                isocode=self.data['language'].get('isocode', ''), 
                classification=self.data['language'].get('classification', ''),
                information="",
                editor=self.editor
            )
            print(u"Created Language: {}".format(self.language))
        
        # 3. identify family and add to it
        family = self.data['language'].get('classification', '').split(",")[0]
        family_slug = slugify(family).replace("-", "").replace(" ", "")
        try:
            self.family = Family.objects.get(slug=family_slug)
            print(u"Identified Family: {}".format(self.family))
        except Family.DoesNotExist:
            self.family = Family.objects.create(
                family = family,
                slug = family_slug,
                editor = self.editor
            )
            print(u"Created Family: {}".format(self.family))
        self.language.family.add(self.family)
        self.language.save()
        return self.language
        
    def _process_source(self):
        assert 'source' in self.data
        assert 'slug' in self.data['source']
        
        try:
            self.source = Source.objects.get(slug=self.data['source']['slug'])
            print(u"Identified Source: {}".format(self.source))
        except Source.DoesNotExist:
            try:
                year = int(self.data['source'].get('year', None))
            except:
                year = None
            self.source = Source.objects.create(
                year=year,
                author=self.data['source'].get('author', ''),
                slug=self.data['source']['slug'], # MUST have slug
                reference=self.data['source'].get('reference', ''),
                bibtex=self.data['source'].get('reference', ''),
                comment="",
                editor=self.editor
            )
            print(u"Created Source: {}".format(self.source))
            
        return self.source
        
    def _process_entries(self):
        assert self.language is not None
        assert self.source is not None
        assert self.editor is not None
        
        for counter, e in enumerate(self.data['entries'], 1):
            record = self.data['entries'][e]
            # 1. get word -- Should NOT need to create an ABVD swadesh 210 word!
            
            word_slug = self.get_word_slug(record['word'])
            
            try:
                word = Word.objects.get(slug=word_slug)
            except Word.DoesNotExist:
                raise Word.DoesNotExist("No Word Matching Slug={}".format(word_slug))
            
            # 2. process
            loan = True if len(record['loan'].strip()) > 0 else False
            lex = Lexicon.objects.create(
                    language=self.language, 
                    source=self.source,
                    word=word, 
                    entry=record['item'],
                    phon_entry="", 
                    annotation=record['annotation'],
                    loan=loan, 
                    editor=self.editor
            )
            print(u"Created Lexicon #{}: {}-{}".format(counter, word, lex))



def _check(args):
    for k, v in args.iteritems():
        if isinstance(v, basestring) and '"' in v:
            raise ValueError('{0} has an unescaped "'.format(k))
    return True
    
def create_source(varname,
                  year="", 
                  author="", 
                  slug="", 
                  reference="", 
                  bibtex="", 
                  comment="",
                  editor=""):
    
    _check(locals())    
    return """
    {varname} = Source.objects.create(
                            year={year}, 
                            author="{author}", 
                            slug="{slug}",
                            reference="{reference}", 
                            bibtex="{bibtex}", 
                            comment="{comment}",
                            editor={editor}
    )
    """.format(**locals())
    
def create_language(varname,
                  language="", 
                  dialect="", 
                  slug="", 
                  isocode="", 
                  classification="", 
                  information="",
                  editor=""):
    
    _check(locals())    
    return """
    {varname} = Language.objects.create(
                            language="{language}", 
                            slug="{slug}",
                            dialect="{dialect}", 
                            isocode="{isocode}", 
                            classification="{classification}",
                            information="{information}"
                            editor={editor}
    )
    """.format(**locals())
    
def create_word(varname,
                  word="", 
                  slug="", 
                  full="", 
                  comment="", 
                  quality="",
                  editor=""):
    
    _check(locals())    
    return """
    {varname} = Word.objects.create(
                            word="{word}", 
                            slug="{slug}",
                            full="{full}", 
                            comment="{comment}", 
                            quality="{quality}",
                            editor={editor}
    )
    """.format(**locals())

def create_lexicon(varname,
                  language="", 
                  source="", 
                  word="", 
                  entry="", 
                  phon_entry="",
                  annotation="",
                  loan="",
                  loan_source="",
                  source_gloss="",
                  editor=""):
    
    _check(locals())    
    return """
    {varname} = Lexicon.objects.create(
                            language={language}, 
                            source={source},
                            word={word}, 
                            loan_source={loan_source},
                            entry="{entry}", 
                            phon_entry="{phon_entry}", 
                            annotation="{annotation}", 
                            loan="{loan}", 
                            source_gloss="{source_gloss}",
                            editor={editor}
    )
    """.format(**locals())

def create_cognate_set(varname,
                  protoform="", 
                  gloss="", 
                  comment="", 
                  source="", 
                  quality="",
                  editor=""):
    
    _check(locals())    
    return """
    {varname} = CognateSet.objects.create(
                            source={source}, 
                            protoform="{protoform}", 
                            gloss="{gloss}",
                            comment="{comment}", 
                            quality="{quality}",
                            editor={editor}
    )
    """.format(**locals())

def create_cognate(varname,
                  lexicon="", 
                  cognateset="", 
                  source="", 
                  comment="", 
                  flag="",
                  editor=""):
    
    _check(locals())    
    return """
    {varname} = Cognate.objects.create(
                            lexicon={lexicon}, 
                            cognateset={cognateset}, 
                            source={source},
                            comment="{comment}", 
                            flag="{flag}",
                            editor={editor}
    )
    """.format(**locals())

def create_correspondence_set(varname,
                  source="", 
                  comment="", 
                  editor=""):
    
    _check(locals())    
    return """
    {varname} = CorrespondenceSet.objects.create(
                            source={source}, 
                            comment="{comment}", 
                            editor={editor}
    )
    """.format(**locals())


def create_correspondence(varname,
                  language="", 
                  corrset="", 
                  rule="", 
                  editor=""):
    
    _check(locals())    
    return """
    {varname} = Correspondence.objects.create(
                            language={language}, 
                            corrset={corrset}, 
                            rule="{rule}", 
                            editor={editor}
    )
    """.format(**locals())


if __name__ == '__main__':
    print create_source('source',
                      year="year", 
                      author="author", 
                      slug="slug", 
                      reference="reference", 
                      bibtex="bibtex", 
                      comment="comment",
                      editor="editor_obj")
    
    print create_language('language',
                  language="language", 
                  dialect="dialect", 
                  slug="slug", 
                  isocode="iso", 
                  classification="classif", 
                  information="info",
                  editor="editor_obj")
    
    print create_word('word',
                  word="word", 
                  slug="slug", 
                  full="full", 
                  comment="comment", 
                  quality="quality",
                  editor="editor_obj")
    
    print create_lexicon('lexicon',
                  language="language_obj", 
                  source="source_obj", 
                  word="word_obj", 
                  entry="entry", 
                  phon_entry="phon_entry",
                  annotation="annotation",
                  loan="loan",
                  loan_source="loan_obj",
                  editor="editor_obj")
    
    print create_cognate_set('cogset',
                  protoform="protoform", 
                  gloss="gloss", 
                  comment="comment", 
                  source="source_obj", 
                  quality="quality",
                  editor="editor_obj")
    
    print create_cognate('cog',
                  lexicon="lexicon_obj", 
                  cognateset="cognateset_obj", 
                  source="source_obj", 
                  comment="comment", 
                  flag="flag",
                  editor="editor_obj")
    
    print create_correspondence_set('corrset',
                  source="source_obj", 
                  comment="comment", 
                  editor="editor_obj")
    
    print create_correspondence('corr',
                  language="language_obj", 
                  corrset="corrset_obj", 
                  rule="rule", 
                  editor="editor_obj")