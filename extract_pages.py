"""
Extract page images from comic files according to extractions.txt
"""
import zipfile
from pathlib import Path
import time
import os

from settings import books_dir
import util
import convert

ONE_DAY_IN_SECONDS = 60 * 60 * 24

def main():
  extraction = util.get_extraction()
  if extraction.is_kepub():
    input_file = convert.convert(extraction.path)

  prefix = extraction.path.stem
  curr_time = time.time() - ONE_DAY_IN_SECONDS

  with zipfile.ZipFile(input_file) as zf:
    image_paths = list(get_image_paths(zf))

    for i, page in enumerate(extraction.pages, 1):
      image_path = image_paths[page - 1]
      image_ext = image_path.rsplit('.')[-1]
      image_data = zf.read(image_path)
      output_file = Path(f'{prefix} {page:03}.{image_ext}')
      output_file.write_bytes(image_data)
      os.utime(output_file, times=(curr_time, curr_time))
      print(f'Wrote {i}. {output_file}')
      curr_time += 60

def get_image_paths(zf: zipfile.ZipFile):
  """
  Return the paths of all jpg/png files inside the given zipfile
  """
  for path in zf.namelist():
    ext = path.rsplit('.')[-1].lower()
    if ext in ['jpg', 'png']:
      yield path

if __name__ == '__main__':
  main()
