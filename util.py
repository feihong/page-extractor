from pathlib import Path
import re
from settings import books_dir


extractions_file = Path('extractions.txt')
books_dir = Path(books_dir).expanduser()

class Extraction:
  def __init__(self, line: str):
    self.path = books_dir / line.strip()
    self.pages = None

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
        if re.match(r'\d+([ ]\d+)*', line):
          latest.pages = [int(s) for s in line.strip().split(' ')]
        else:
          yield latest
          latest = Extraction(line)

    if latest is not None:
      yield latest

def get_extraction():
  """
  Return the last Extraction object that has pages
  """
  extractions = [e for e in get_extractions() if e.pages is not None]
  return extractions[-1]
