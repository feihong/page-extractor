
import zipfile
from pathlib import Path

from settings import books_dir
import util
import convert

def main():
  input_file, pages = util.get_extraction_info()
  if input_file.name.endswith('.kepub.epub'):
    input_file = convert.convert(input_file)

  prefix = input_file.stem

  with zipfile.ZipFile(input_file) as zf:
    paths = zf.namelist()
    for i, page in enumerate(pages, 1):
      image_path = paths[page - 1]
      image_ext = image_path.rsplit('.')[-1]
      image_data = zf.read(image_path)
      output_file = Path(f'{prefix} {page:03}.{image_ext}')
      output_file.write_bytes(image_data)
      print(f'Wrote {i}. {output_file}')

if __name__ == '__main__':
  main()
