from pathlib import Path
import re
from settings import books_dir


extractions_file = Path('extractions.txt')
books_dir = Path(books_dir).expanduser()

class Extraction:
  def __init__(self, line: str):
    self.path = books_dir / line.strip()
    self.pages = None

class Page:
  def __init__(self, s):
    if s.endswith('c'):
      self.crop = True
      s = s[:-1]
    else:
      self.crop = False

    self.value = int(s)

def get_extractions():
  """
  Parse the extractions file and return a sequence of Extraction objects
  """
  with extractions_file.open() as fp:
    latest = None

    for line in fp:
      if latest is None:
        latest = Extraction(line)
      else:
        if re.match(r'\d+c?([ ]\d+c?)*', line):
          latest.pages = [Page(s) for s in line.strip().split(' ')]
        else:
          yield latest
          latest = Extraction(line)

    if latest is not None:
      yield latest

def get_last_extraction():
  """
  Return the last Extraction object
  """
  extractions = list(get_extractions())
  return extractions[-1]
