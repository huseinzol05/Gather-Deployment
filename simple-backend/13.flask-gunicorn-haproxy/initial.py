from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons
from ekphrasis.classes.spellcorrect import SpellCorrector

text_processor = TextPreProcessor(
    normalize = [
        'url',
        'email',
        'percent',
        'money',
        'phone',
        'user',
        'time',
        'url',
        'date',
        'number',
    ],
    annotate = {
        'hashtag',
        'allcaps',
        'elongated',
        'repeated',
        'emphasis',
        'censored',
    },
    fix_html = True,
    segmenter = 'twitter',
    corrector = 'twitter',
    unpack_hashtags = True,
    unpack_contractions = True,
    spell_correct_elong = False,
    tokenizer = SocialTokenizer(lowercase = True).tokenize,
    dicts = [emoticons],
)

sp = SpellCorrector(corpus = 'english')
