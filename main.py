
pages = '5'
input_file = '~/Books/[Mox.moe][火鳳燎原]第01卷.kepub.epub'

from typing import List
from pathlib import Path
import zipfile
import sys
import xml.etree.ElementTree

pages = [int(s) for s in pages.strip().split(' ')]
input_file = Path(input_file).expanduser()

# Namespace dictionary for xpath queries:
ns = dict(opf='http://www.idpf.org/2007/opf', xhtml='http://www.w3.org/1999/xhtml')

def main():
  with zipfile.ZipFile(input_file) as zf:
    page_paths = get_page_paths(zf)
    for path in get_image_paths(zf, page_paths):
      print(path)

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

if __name__ == '__main__':
  main()
