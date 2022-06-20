"""
Convert .kepub.epub file to .cbz file
"""
from pathlib import Path
import zipfile
import xml.etree.ElementTree
from typing import List

# Namespace dictionary for xpath queries:
ns = dict(opf='http://www.idpf.org/2007/opf', xhtml='http://www.w3.org/1999/xhtml')


def convert(epub_file: Path):
  output_file = Path(epub_file.name[:-11] + '.cbz')

  with zipfile.ZipFile(output_file, 'w') as zf:
    for i, ext, image_data in get_image_datas(epub_file):
      zf.writestr(f'{i:03}.{ext}', image_data, compress_type=zipfile.ZIP_STORED)

  print(f'Converted {epub_file} to {output_file}')
  return output_file

def get_image_datas(input_file: zipfile.ZipFile):
  """
  Given a zip file, return a sequence of pairs of the form (number, image_extension, bytes)
  """
  with zipfile.ZipFile(input_file) as zf:
    page_paths = get_page_paths(zf)
    image_paths = list(get_image_paths(zf, page_paths))

    for i, image_path in enumerate(image_paths, 1):
      image_ext = image_path.rsplit('.')[-1]
      yield i, image_ext, zf.read(image_path)

def get_page_paths(zf: zipfile.ZipFile):
  """
  Return all page paths, in order
  """
  with zf.open('vol.opf') as fp:
    tree = xml.etree.ElementTree.parse(fp)
    for item in tree.findall(".//opf:item[@media-type='application/xhtml+xml']", ns):
      yield item.attrib['href']

def get_image_paths(zf: zipfile.ZipFile, page_paths: List[str]):
  """
  Given a sequence of page paths, return a sequence of image paths
  """
  for page_path in page_paths:
    with zf.open(page_path) as fp:
      tree = xml.etree.ElementTree.parse(fp)
      img = tree.find('.//xhtml:img', ns)
      yield img.attrib['src'][3:]  # chop off '../'

