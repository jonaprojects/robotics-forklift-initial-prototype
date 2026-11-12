# EV3 forklift: integrated spatial prototype I0.2 - forward-axle candidate

> Historical layout review. The current scene is documented in [Custom-Chassis-Review.md](Custom-Chassis-Review.md), which supersedes the merged chassis, stance and stroke values below.

**Release status: HOLD. A complete, build-verified digital prototype has not been achieved.**

This iteration adds an overall robot/station layout and a pickup/delivery sequence to the real-part lift model. It closes four lift-side adapter bore checks. It does not close the chassis end of the adapter, full part allocation, balance, or the sensor/stop mounts. The scene includes a mixture of real LEGO components, a merged reference chassis and explicitly named concept envelopes.

## Open the model

Open `EV3-Integrated-Viewer.html` in a WebGL-capable browser. Drag to rotate, scroll to zoom and use the sequence slider. `?pose=carry` starts at a raised carrying pose. The animation illustrates approach, lift, reversal, lowering and withdrawal. It is prescribed motion, not a navigation, friction or force simulation.

`robot-station.mpd` embeds all referenced CAD geometry. Project-prefixed geometry represents a merged reference model or a non-LEGO fixture/envelope; those files are not LEGO catalog parts. `assembly-initial.json` records component transforms and status flags. `layout-parts.csv` excludes parts inside the merged chassis and therefore is NOT a complete bill of materials.

## What was added

| Assembly | Representation and status |
|---|---|
| Chassis, EV3 brick and rear support | A third-party reconstruction of LEGO's Driving Base, stored as a merged reference mesh. Individual joints and rear-support floor contact remain unaudited. |
| Drive motors | Two actual EV3 large-motor shapes placed at X=64, Y=+/-32, Z=28 mm. This moves the axle ahead of the reference base configuration; a custom forward motor mount/chassis is required. |
| Drive wheels | Actual 56 mm tires and hubs, plus proposed 9L axles and retaining bushes. Tires touch the design floor; full hub/key engagement is not verified. |
| Lift module | Existing real-part mechanism translated 96 mm ahead of the drive axle. The motor is raised 32 mm and drives a new 40T-to-24T stage into the original 9:1 train. The resulting overall reduction is 5.4:1, with approximately 186.8 motor degrees for the full linkage stroke. Two adapter cross shafts are extended. The motor spine uses its lower hole as a second shaft-bearing constraint; insertion, retention and structural rigidity remain unverified. |
| Lift adapter | Two blue 7L beams centered at X=64, Y=+/-24, Z=80 mm. Their holes at X=48 and 80 align with upper frame holes. Two cross-tie shafts become 8L; their outer half bushes move to Y=+/-30. The rear attachment to the chassis is open. |
| Color sensor | Real EV3 sensor geometry placed near the floor. Bracket, optical direction and cable routing are open. |
| Lower-reference touch sensor | Real EV3 sensor geometry placed clear of the coupler. Its support and trigger cam remain open; the shown placement does not establish switch activation. |
| Camera | Orange 40 x 30 x 24 mm box on a blue support envelope. Assumed dimensions only; no camera model, optical field, wiring or mount is verified. |
| Limit stops | Two red 6 x 8 x 4 mm envelopes show candidate stop regions. These are not designed LEGO stop assemblies. |
| Pallet | External 80 mm wide x 64 mm deep fixture, with three 16 mm runners and 16 mm fork channels. Deck underside is 16 mm above the floor. |
| Payload | A 40 mm cube. Its geometry does not establish its mass or load capacity. |
| Pickup target | A red station marker showing a possible camera target position. No vision detector or pose estimation is implemented. |

No wheel-motion controller, camera pipeline, line follower, switch logic or EV3 program is included in this CAD scene.

## Sequence and checks

The robot advances 40 mm to insert the forks, lifts, reverses 120 mm, lowers the pallet, then reverses a further 50 mm to withdraw. While supported, the pallet follows the carriage's small fore-aft arc. A 4.4 mm entry gap is taken up before the pallet rises. Ideal final pallet-floor clearance is about 23.9 mm.

`integration-checks.json` records eight checks: four actual lift-side adapter hole-axis matches; stable component ordering through 71 poses; tire-floor contact; nominal pallet rise; and proper rigid rotations. These checks pass. A six-pose floor audit found no mesh below the design floor (`floor-and-balance.json`). This is not a complete interference or assembly-path check.

Browser checks exercise initial, carrying and gearbox views and store the viewer file hash, so a successful render can be tied to the generated file. These verify display behavior, not mechanical construction.

## Balance: revised candidate passes an assumption case

The original stock-axle placement failed the initial example budget; that historical case is retained in `floor-and-balance.json`. To address it, this candidate moves the drive axle 64 mm forward. A new raised lift-motor input clears the tire tops by approximately **12.4 mm**, based on actual mesh bounding heights. Its added 40T/24T gear stage is checked at the gear center plane over 15 lifting poses, not over every tooth surface in 3D.

The new sensitivity case assumes a chassis/brick/drive mass of 0.85 kg, fixed lift mass 0.18 kg, moving lift mass 0.08 kg and pallet-plus-load mass 0.10 kg. The original chassis CG assumption was X=-50 mm; moving two assumed 80 g drive motors forward shifts that CG to about X=-38 mm. The drive axle is at X=64 mm. The fixed and moving lift CG assumptions are X=76 and 161 mm. The payload position is derived from the scene and reaches about X=219.6 mm relative to the robot before clearance take-up.

Under these assumptions the restoring mass-moment is about 0.08666 kg m and the overturning mass-moment about 0.02548 kg m: a ratio of about **3.40**, above the illustrative 1.5 target. This is a sensitivity calculation, not measured mass data, an accepted standard, dynamic stability or a lifting-capacity certification. The exact results and assumptions are in `forward-layout-checks.json`.

Moving the axle fixes this particular example budget but creates a requirement for a custom forward drivetrain mount. The merged reference chassis is now a body/layout reference, not a claim that LEGO's unchanged Driving Base supports these motor positions. The whole model remains on hold until this interface and full-body interference checks are resolved. Rear support geometry/contact, acceleration, braking and lateral turning stability remain unverified.

## Parts and connection audit

The isolated lift already exceeded one core set by at least three full bushes, eight half bushes and one pin-joiner tube. Integration changes its two upper frame ties from 6L to 8L axles, adds two 7L adapters, two drive motors, wheel/hub pairs, proposed drive axles/bushes, two sensors and the raised input stage (40T gear, 24T gear, 10L shaft, revised 12L lower input shaft and spacers). These compete with parts inside the reference chassis.

**Do not use `layout-parts.csv` as a shopping list.** It cannot reconcile the merged reference mesh. The actual chassis must be decomposed into catalog parts or replaced by a fully specified custom chassis before a combined stock audit is possible. Camera electronics and its support are still unknown. No equipment was purchased.

Current connection register:

| Interface | Status |
|---|---|
| Lift upper frame -> blue adapter rails | Bore axes specified and checked; actual insertion and retention still need assembly review |
| Adapter rails -> chassis | OPEN: no released connection |
| Motor/hub/axle -> chassis | Proposed positions; pin and keyed-shaft engagement OPEN |
| Touch sensor, actuator and stops -> structure | OPEN |
| Color sensor -> structure | OPEN |
| Camera -> structure/controller | Assumed envelope; OPEN |
| Pallet -> forks | Nominal dimensional and prescribed-motion study; no contact/friction solver |
| Rear support and load stability | Forward-axle sensitivity case passes; actual masses, support contact and dynamics OPEN |

## Completion gate

The whole digital prototype is complete only when every open mechanical interface has a catalog-part connection, the camera assumption is resolved, the full bill of materials reconciles, all critical motion/assembly/cable clearances are checked and a defensible balance estimate passes. Physical stiffness, friction, actual capacity and navigation reliability remain lab checks after that gate. The instruction booklet has not been released.

The immediate priority is a fully specified chassis/axle mounting arrangement for the forward-axle candidate. Refining the camera bracket before that decision would risk redoing its position.

## Sources and attribution

- LDraw community component geometry: https://library.ldraw.org/ . Part author/license headers are preserved in the MPD. CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ ; CC BY 2.0: https://creativecommons.org/licenses/by/2.0/ . The earlier detailed attribution table is `../cad/ATTRIBUTION.md`; newly used components retain attribution in their embedded source headers.
- Chassis reconstruction: RobotDSL Team, after LEGO Education's EV3 Driving Base instructions, using LDraw components. Dataset: https://huggingface.co/datasets/Aki-Frank/robotdsl-library-assets . Source asset: https://huggingface.co/datasets/Aki-Frank/robotdsl-library-assets/resolve/main/parts/lego_45544_driving_base_chassis/assets/model.glb . Original credits state CC BY 2.0 AND CC BY 4.0 for the derived chassis; the assembly source is credited CC BY 4.0. The source asset is saved in `../sources/reference-base.glb`, with the original dataset README in `../sources/robotdsl-readme.md`.
- Official LEGO driving-base instructions remain at `../sources/driving-base.pdf`; core-set inventory at `../sources/inventory.pdf`.
- Pallet, target and concept-box geometry and original integration code are authored by this project, CC BY 4.0. No vendor camera or bracket is implied by the placeholder shapes.

## Reproduction in the project workspace

Run `python design/cad/build_integrated.py`, then `python design/cad/verify_integrated.py`. The browser smoke check is `design/integrated/verify_viewer.ps1` (Windows/Chrome). The shared LDraw subset and saved reference GLB are required for regeneration; the delivered viewer and MPD are self-contained for inspection. The previous isolated lift viewer and its 9:1 specification remain historical subassembly references, not the current integrated 5.4:1 input.
