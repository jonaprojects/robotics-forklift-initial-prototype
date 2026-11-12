# EV3 lift: digital model review P2-R1

**Scope: a real-part lift subassembly with motor bracket. The whole forklift and phase 2 are not complete.**

This advances the mechanism from idealized beam lines to placed LDraw part geometry. It does not certify that a complete forklift can be built from a single core set. Chassis integration and sensing hardware remain open. No physical build has been observed.

## Open the result

- Open `EV3-Lift-Viewer.html` in a browser. It works offline; drag to orbit, scroll to zoom, move the lift-position slider or separate the layers.
- Open either self-contained `.mpd` file in a compatible LDraw CAD application. Its referenced geometry is embedded, including the original part attribution headers.
- The PNG views are in `renders/`. `assembly-low.json` and `assembly-raised.json` record every part placement in mm.
- `stock-ledger.csv` counts physical pieces and maps design files to official element IDs. `lift-parts.csv` lists digital references; its motor body and rotor together represent ONE medium motor.

## What was modeled

84 digital instances represent 83 physical pieces, counting the medium motor as one supplied assembly. There are 19 physical stock types. All displayed structural parts use actual LDraw surface geometry; no beam or gear is stretched to force a connection.

Two 5x7 frames support the three gearbox shafts. A compound 8T/24T spur train drives a shared lower-link axle. Four 7L links connect to two 9L carriage beams. Two white 3x5 right-angle beams attach the forks at two pin positions each. Cross ties brace both fixed frames and the moving carriage. A 9L spine connects the medium motor to a fixed frame, with the input shaft providing a second separated bearing axis.

## Changes since phase 1

1. **Gearbox corrected:** the actual 5x7 frame has no transverse bearing hole at the proposed X=-24 position. Two 8T/24T pairs use existing holes at X=-32, -16 and 0 mm and retain 9:1 reduction.
2. **Carriage length corrected:** 9L vertical beams replace the 5L candidates. Their lower pivot is H5 and upper pivot H9. The carriage extends 32 mm below the lower pivot so the forks can approach the floor.
3. **Fork mounting specified:** a 3x5 right-angle beam on each outer side attaches to carriage H1/H3, and to fork H1/H3. The fork starts 16 mm forward of the carriage centerline.
4. **Motor bracket specified:** the vertical 9L spine is centered at X=-32, Y=-32, Z=48 mm. Its H4/H6 receive the two motor-face pins; H5 carries the input axle. H9 connects to the frame through a 2L liftarm used as a spacer and a 3L pin. The long pin spans exactly Y=-36 to -12 mm.
5. **Through-spacers corrected:** hollow pin-joiner tubes are used on cross shafts. A stopped axle joiner is unsuitable for an uninterrupted shaft.
6. **Axle and gear clocking specified:** the output follows the links, the intermediate shaft follows the 3:1 relation and the input follows 9:1. Each shaft, its gears and keyed collars rotate together; gears are not independently turned inside fixed cross axles.
7. **Low angle adjusted:** -9.594 degrees, with the fixed lower pivot at Z=48 mm, places the fork center at Z=8 mm on an 8 mm grid. Upper angle remains +25 degrees.

## Refined dimensions

| Quantity | Digital value |
|---|---|
| Lowered module bounding box, including motor and axle ends | 182.9 x 156.2 x 79.6 mm (X/Y/Z) |
| Fork center spacing | 32 mm |
| Actual fork profile width / thickness | 8.0 / 7.2 mm |
| Lowered fork underside / top | 4.4 / 11.6 mm above the design floor |
| Carriage lift travel | 28.29 mm |
| Pallet-floor clearance, with deck underside at 16 mm | 23.89 mm, ideal rigid pickup |
| Medium-motor rotation for full stroke | 311.35 degrees, before backlash/calibration |
| Clear forward fork portion beyond the bracket | About 48 mm; use 40 mm insertion for the first approach trial |

The module bounding box is not the whole robot footprint. A 40 mm insertion reaches beyond the 32 mm depth-center of a 64 mm pallet, assuming the load is centered and the station is correctly aligned. Lift strength and stability are still unmeasured.

## Verification performed

- **56/56 geometry checks pass; 0 fail.** Includes proper rigid transforms, primitive-derived bearing and pin axes, fork brackets at three poses, actual pin stack length and a floor sweep through 71 poses.
- **PASS: Selected structural parts across 71 poses.** 14910 pair/pose bounding-box checks; 0 unresolved pairs. Gear meshes and fasteners excluded. Lower-link/bracket broad overlaps resolved with conservative 4.1 mm profile-radius envelopes; minimum clearance 6.301 mm.
- **PASS: Gear tooth center-plane section test.** 30 center-plane tests at 0.04 mm grid spacing. Maximum estimated overlap area 0.0000 mm^2. This does not test all axial sections or certify real tooth contact.
- **Browser smoke checks pass for this exact viewer file:** lowered, raised and gearbox-only views render in headless Chrome with WebGL error code 0. The viewer hash and observations are in `browser-checks.json`.

These checks are targeted engineering checks. Bounding boxes reject separated parts; the link/bracket cases use conservative profile envelopes. The gear test samples actual center-plane sections; it does not check every tooth surface in 3D. Pins, axle keys, friction-fit deformations and internal motor contacts are not covered by the structural sweep. A matching hole axis alone is not proof of an accessible insertion path or correct pin retention.

## Stock shortfalls

Compared with the official inventory, the standalone lift already needs these extras:

| Element ID | Item | Lift needs | Core set has | Minimum extra |
|---|---|---|---|---|
| 4211622 | gray full bush | 13 | 10 | 3 |
| 4239601 | yellow half bush | 18 | 10 | 8 |
| 4526985 | gray 2L pin-joiner tube | 5 | 4 | 1 |

These are lower bounds. The driving base also consumes parts from the same kit; its requirements must be added before deciding what the complete robot needs. In particular, using the kit's axle supply for the lift can leave too few for the chassis. No extras have been purchased. A later simplification can reduce spacer demand if keeping strictly to one kit becomes a requirement.

## Remaining work before instruction-book release

| Interface | Status |
|---|---|
| Lift-to-chassis attachment | Open: exact bracket, hole mapping and full assembly clearance |
| Motor bracket | Digitally specified; physical rigidity and pin insertion/retention need checking |
| Fixed frame cross-bracing | Digitally specified; physical play needs checking |
| Fork brackets and moving cross-bracing | Digitally specified; insertion and loaded stiffness need checking |
| Lower-limit switch and independent hard stops | Open |
| Color sensor and camera mounting | Open; camera model/interface unknown |
| Combined chassis/lift/sensor parts allocation | Open |
| Full collision, assembly-path and balance validation | Open |

The immediate next engineering work is to integrate this module with the chosen chassis. The final instruction booklet should be generated only from a completed assembly sequence, with the unresolved items closed or explicitly scoped out.

## Reproduce the checks

Python dependencies: numpy and matplotlib. From this directory run:

```text
python build_lift.py
python check_clearances.py
python render_model.py
python package_model.py
```

The HTML viewer itself needs no Python or network access. Source-part geometry is stored under `library/subset/`.

## Sources

- Geometry: https://library.ldraw.org/ . The project downloaded individual official part ZIPs including their subparts/primitives. `ATTRIBUTION.md` records all used contributors and licenses.
- Core-set stock: LEGO official Element Survey 45544, saved at `../sources/inventory.pdf`: https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltd9e811d9ff83b385/5f8801d5887a311d8fa19812/45544_element_survey.pdf?locale=en-gb .
- The stock Driving Base remains an external reference (`../sources/driving-base.pdf`); it is not included in this module CAD file.
