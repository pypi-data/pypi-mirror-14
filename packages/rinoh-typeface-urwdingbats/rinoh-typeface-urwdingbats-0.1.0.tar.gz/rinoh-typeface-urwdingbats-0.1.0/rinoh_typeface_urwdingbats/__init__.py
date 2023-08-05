from os import path

from rinoh.font import Typeface
from rinoh.font.mapping import UNICODE_TO_DINGBATS_NAME
from rinoh.font.style import REGULAR
from rinoh.font.type1 import Type1Font


__all__ = ['typeface']


typeface = Typeface('URW Dingbats',
                    Type1Font(path.join(path.dirname(__file__), 'd050000l'),
                              weight=REGULAR,
                              unicode_mapping=UNICODE_TO_DINGBATS_NAME))
