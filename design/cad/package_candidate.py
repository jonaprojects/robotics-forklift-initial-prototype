"""Portable B0.1 first-build package, with immutable predecessor and checks."""
import json,hashlib,zipfile
from pathlib import Path
from build_candidate import OUT,ROOT

def run():
    workspace=ROOT.parent.parent
    verification=json.loads((OUT/'verification.json').read_text())
    assert verification['summary']=={'PASS':80},verification['summary']
    browser=json.loads((OUT/'browser-checks.json').read_text(encoding='utf-8-sig'))
    assert len(browser['checks'])==5 and all(c['status']=='PASS' for c in browser['checks'])
    viewer=OUT/'EV3-Build-Candidate.html'
    assert browser['viewerSha256'].lower()==hashlib.sha256(viewer.read_bytes()).hexdigest()
    old=ROOT.parent/'saved'/'EV3-I0.3-preserved.zip'
    assert hashlib.sha256(old.read_bytes()).hexdigest()=='6cd3a9f48bf6036a3925d2865456a351ab3df826c9682434b9aad713bb0a0597'
    names=['BUILD-GUIDE.html','BUILD-GUIDE.md','EV3-Build-Candidate.html','build-candidate.mpd','build-candidate.ldr',
           'assembly.json','parts.csv','placements.csv','verification.json','whole-structure-audit.json','browser-checks.json',
           'file-checks.json','guide-checks.json','ATTRIBUTION.md','verify_viewer.ps1','verify_guide.ps1']
    files=[OUT/n for n in names]
    files += [OUT/'renders'/n for n in ['viewer-lowered.png','viewer-carrying.png','viewer-gears.png','viewer-step-touch.png','viewer-step-camera.png','guide-top.png','guide-touch.png']]
    sources=['build_candidate.py','candidate_steps.py','candidate-template.html','write_candidate_guide.py','package_candidate.py',
             'verify_candidate.py','audit_structure.py','build_integrated.py','build_lift.py','custom_chassis.py',
             'ldraw_geometry.py','render_model.py','package_model.py','check_clearances.py']
    files += [ROOT/n for n in sources]
    files += list((ROOT/'library'/'subset').rglob('*.dat'))
    files += [old,old.parent/'I0.3-manifest.json']
    assert all(p.is_file() for p in files)
    manifest={str(p.relative_to(workspace)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    (OUT/'package-manifest.json').write_text(json.dumps(dict(revision='B0.1',geometry_checks=80,browser_cases=5,files=manifest),indent=2))
    files.append(OUT/'package-manifest.json')
    readme='''# EV3 forklift B0.1 - first physical build candidate

Start with [the assembly guide](design/build_candidate/BUILD-GUIDE.html), then open [the offline 3D viewer](design/build_candidate/EV3-Build-Candidate.html).

The package contains 21 assembly stages, exact CAD and placements, 329 physical LEGO pieces in the bill, sensor brackets, a lift trigger, adjustable stops and a camera holder. Choose an assembly step in the viewer; blue marks new parts, and the isolate checkbox shows that subassembly. Drag to rotate and scroll to zoom.

All 80 recorded geometry checks and five browser cases pass. This is a model for the first lab assembly, not a physically demonstrated build. Camera identity/interface, kit stock, switch trip/travel, stiffness, cable sweep and loaded stability require the acceptance tests in the guide. The camera envelope is assumed at 40 x 30 x 24 mm. No measured payload rating or navigation software is included.

The prior I0.3 version is preserved in design/saved with its SHA-256 manifest. Do not mix its motor spacing or gear-plane placement with B0.1.

The HTML viewer and MPD work independently offline. Regeneration sources and the LDraw subset are under design/cad; Python requires numpy and matplotlib. From this extracted root run build_candidate.py, audit_structure.py, verify_candidate.py and write_candidate_guide.py using their full design/cad paths, in that order. Browser checks require Chrome on Windows. Source geometry retains its LDraw author and license headers; see ATTRIBUTION.md in the build folder.
'''
    archive=ROOT.parent/'EV3-Forklift-B0.1-First-Build.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('README.md',readme)
        for p in files:z.write(p,p.relative_to(workspace).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert all(hashlib.sha256(z.read(name)).hexdigest()==digest for name,digest in manifest.items())
    summary=dict(archive=archive.name,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),bytes=archive.stat().st_size,
                 verified_archive_entries=len(files)+1,all_manifest_hashes_verified=True)
    (OUT/'package-checks.json').write_text(json.dumps(summary,indent=2))
    print(summary)

if __name__=='__main__':run()
