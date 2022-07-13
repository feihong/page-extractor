"""
Convert extractions that don't yet have pages
"""
import util
import convert

extractions = util.get_extractions()

for extraction in (extraction for extraction in extractions if extraction.pages is None):
  if extraction.pages is None and extraction.is_kepub():
    convert.convert(extraction.path)
