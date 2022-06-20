from pathlib import Path
import re
from settings import books_dir


extractions_file = Path('extractions.txt')
books_dir = Path(books_dir).expanduser()


def get_extraction_info():
  """
  Return tuple of the form (input_file, pages_list)
  """
  lines = extractions_file.read_text().strip().splitlines()
  last_line = lines[-1]
  if re.match(r'\d+', last_line):
    input_file = books_dir / lines[-2]
    pages = [int(s) for s in last_line.strip().split(' ')]
  else:
    input_file = books_dir / last_line
    pages = []

  if not input_file.exists():
    raise Exception(f'{input_file} does not exist!')
  return input_file, pages
