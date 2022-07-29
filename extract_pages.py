"""
Extract page images from comic files according to extractions.txt
"""
import zipfile
from pathlib import Path
import time
import os

import util
import convert

ONE_DAY_IN_SECONDS = 60 * 60 * 24

def main():
  extraction = util.get_last_extraction()

  prefix = extraction.path.stem
  curr_time = time.time() - ONE_DAY_IN_SECONDS

  with zipfile.ZipFile(extraction.path) as zf:
    image_paths = list(get_image_paths(zf))

    for i, page in enumerate(extraction.pages, 1):
      image_path = image_paths[page - 1]
      image_ext = image_path.rsplit('.')[-1]
      image_data = zf.read(image_path)
      output_file_ = Path(f'{prefix} {page:03}.{image_ext}')
      output_file_.write_bytes(image_data)

      output_file, reduction_percent = convert.convert_image_to_webp(output_file_)
      os.remove(output_file_)

      # Change modified time so images appear in the expected order when
      # uploaded to Google Photos
      os.utime(output_file, times=(curr_time, curr_time))
      print(f'Wrote {i}. {output_file} (reduced by {reduction_percent:0.2f}%)')
      curr_time += 10

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
