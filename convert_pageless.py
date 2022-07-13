"""
Convert extractions that don't yet have pages
"""
import util
import convert

extractions = util.get_extractions()

for extraction in (extraction for extraction in extractions if extraction.pages is None):
  if extraction.pages is None and extraction.path.name.endswith('.kepub.epub'):
    convert.convert(extraction.path)
