
pages = '5'
input_file = '~/Books/[Mox.moe][火鳳燎原]第01卷.kepub.epub'

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
    for path in get_page_paths(zf):
      print(path)

def get_page_paths(zf: zipfile.ZipFile):
  """
  Return all page paths, in order
  """
  with zf.open('vol.opf') as fp:
    tree = xml.etree.ElementTree.parse(fp)
    for item in tree.findall(".//opf:item[@media-type='application/xhtml+xml']", ns):
      yield item.attrib['href']

if __name__ == '__main__':
  main()
