"""Build and validate a static Pages artifact using only Python's standard library."""
import argparse,shutil
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--output',default='_site')
args=parser.parse_args()
out=(ROOT/args.output).resolve()
if out==ROOT or ROOT not in out.parents:raise SystemExit('Output must be a subdirectory of the repository')
out.mkdir(parents=True,exist_ok=True)
files=['index.html','design/EV3-Forklift-B0.1-First-Build.zip','design/saved/EV3-I0.3-preserved.zip','design/saved/I0.3-manifest.json']
base='design/build_candidate/'
files += [base+n for n in ['BUILD-GUIDE.html','BUILD-GUIDE.md','EV3-Build-Candidate.html','build-candidate.mpd','parts.csv','placements.csv','verification.json','browser-checks.json','ATTRIBUTION.md','renders/viewer-lowered.png']]
for name in files:
    dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,dest)
(out/'.nojekyll').touch()
class Links(HTMLParser):
    def __init__(self):super().__init__();self.refs=[]
    def handle_starttag(self,tag,attrs):
        for name,value in attrs:
            if name in ('href','src') and value:self.refs.append(value)
bad=[]
for name in files:
    if not name.endswith('.html'):continue
    p=out/name;page=Links();page.feed(p.read_text(encoding='utf-8'))
    for ref in page.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc or not url.path:continue
        target=(p.parent/unquote(url.path)).resolve()
        if url.path.startswith('/') or out not in target.parents or not target.is_file():bad.append((name,ref))
if bad:raise SystemExit('Broken or non-portable links: '+repr(bad))
print(f'Pages artifact ready: {len(files)+1} files; all HTML links resolve; project-subpath compatible.')
