from plone.app.imaging.utils import getAllowedSizes
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory

from plone import api

from zope.i18nmessageid import MessageFactory


_ = MessageFactory('medialog.simpleslider')


def format_size(size):
    return "".join(size).split(' ')[0]


def ImageSizeVocabulary(context):
    sizes = getAllowedSizes()
    #default vocabulary if everything else fails
    terms = [
            SimpleTerm('mini', 'mini', u'Mini'),
            SimpleTerm('preview', 'preview', u'Preview'),
            SimpleTerm('large', 'large', u'Large'),
            SimpleTerm('original', 'original', u'Original'),
        ]
        
    if sizes:
        if not 'original' in sizes:
        	sizes.update({'original': 'original'})
        terms = [ SimpleTerm(value=format_size(pair), token=format_size(pair), title=pair) for pair in sizes ]
      
    return SimpleVocabulary(terms)

 