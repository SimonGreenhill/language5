"""
Tools for creating string representations of various model create statements.
"""

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
                  language="lexicon_obj", 
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