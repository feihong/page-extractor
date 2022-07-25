"""
Look for .kepub.epub files in ~/Downloads and for each one:
- Convert it to .cbz
- Move it into a subdirectory of your designated books directory
"""
import re
from pathlib import Path
import shutil
import util
import convert

downloads_dir = Path('~/Downloads').expanduser()

for epub_file in downloads_dir.glob('*.kepub.epub'):
  match = re.match(r'\[Mox\.moe\]\[(.*)\]', epub_file.name)
  if match:
    cbz_file = convert.convert_epub_to_cbz(epub_file)
    dest_dir = util.books_dir / match.group(1)
    if not dest_dir.exists():
      dest_dir.mkdir()
    shutil.move(cbz_file, dest_dir)
    print(f'Moved {cbz_file} to {dest_dir}')
