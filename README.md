# EV3 forklift project

[Open the GitHub Pages demo](https://jonaprojects.github.io/robotics-forklift-initial-prototype/).

The repository includes a static landing page and an automated Pages deployment on pushes to `main`. The workflow publishes a curated `_site` artifact containing the B0.1 viewer, guide, CAD, downloads and attribution. Run `python scripts/prepare_pages.py` locally to build it and check its relative links. To preview, run `python -m http.server 8000 --directory _site` and open `http://localhost:8000/`.

Pages uses the **GitHub Actions** publishing source (repository Settings > Pages). The workflow follows [GitHub's Pages deployment guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). Browser profiles, raw browser DOM dumps and local credentials are excluded from Git.

The intended final deliverable is a LEGO-style instruction booklet for a small EV3 forklift with camera-assisted docking.

The latest deliverable is **B0.1, a first physical build candidate**. It includes 329 physical LEGO pieces, sensor brackets and a lift-reference trigger, adjustable mechanical stops, a removable camera holder, wiring instructions and 21 assembly stages. All 80 recorded geometry checks pass. The camera identity, available kit inventory, actual switch travel, loaded stability and physical assembly still need lab confirmation.

- [Read the B0.1 assembly guide](design/build_candidate/BUILD-GUIDE.html).
- [Open the B0.1 step-by-step 3D viewer](design/build_candidate/EV3-Build-Candidate.html).
- [Download the complete B0.1 package](design/EV3-Forklift-B0.1-First-Build.zip).
- [Check the complete LEGO bill](design/build_candidate/parts.csv).
- [Read the verification scope and results](design/build_candidate/verification.json).

The previously current I0.3 version was saved separately before development, with a SHA-256 manifest:

- [Preserved I0.3 archive](design/saved/EV3-I0.3-preserved.zip).
- [Preservation manifest](design/saved/I0.3-manifest.json).

The following I0.3 files are historical references. B0.1 corrects motor-flange spacing and gear-stage interference found during its broader checks; do not mix the revisions.

- [Open the integrated robot/station viewer](design/integrated/EV3-Integrated-Viewer.html).
- [Read the current custom-chassis review](design/integrated/Custom-Chassis-Review.md).
- [Download the custom chassis candidate](design/EV3-Custom-Chassis-I0.3.zip).
- [Check all currently placed LEGO parts and core-set shortfalls](design/integrated/catalog-parts.csv).

An extended kit may be available, per the user; its specific inventory has not been assumed. The current candidate uses extra standard Technic pieces. The older I0.2 archive and review are retained as historical references.

The earlier isolated lift subassembly is retained below. Its original 9:1 input is superseded in the integrated candidate by a raised input stage giving 5.4:1 overall reduction.

- [Open the offline 3D lift viewer](design/cad/EV3-Lift-Viewer.html).
- [Read the current engineering review and limits](design/cad/Phase-2-Review.md).
- [Check physical parts and minimum stock shortfalls](design/cad/stock-ledger.csv).
- [Download the portable CAD/review package](design/EV3-Digital-Lift-P2-R1.zip).
- [Open the self-contained lowered CAD model](design/cad/lift-low-self-contained.mpd).
- [Open the self-contained raised CAD model](design/cad/lift-raised-self-contained.mpd).

The model uses actual LDraw part geometry and includes a geared medium motor, its proposed mounting bracket, a parallelogram lift, fork brackets, and cross-bracing. The viewer works offline and requires a browser with WebGL.

For B0.1 use the new assembly guide and its lab acceptance sequence. The older lift reviews describe earlier stages and do not reflect all current mounts or gear positions. The interactive assembly guide is available; a polished printable LEGO-style instruction booklet has not yet been released.

Earlier proposals are retained in this folder as historical references; use the current engineering review for the latest geometry and verification scope.
