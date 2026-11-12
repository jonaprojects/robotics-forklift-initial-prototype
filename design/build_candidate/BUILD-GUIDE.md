# EV3 forklift B0.1: first physical build candidate

Saved predecessor: `../saved/EV3-I0.3-preserved.zip` (SHA-256 recorded in `../saved/I0.3-manifest.json`). B0.1 is separate; do not mix its motor spacing and sensor brackets with I0.3.

This package gives the team a defined mechanical model to attempt in the lab: 329 physical LEGO pieces, complete sensor brackets, independent adjustable mechanical stops and a removable camera holder. It is a first-build candidate, not a physically proven robot or a finished navigation system. The actual extended-kit contents and camera model have not been confirmed.

Open `EV3-Build-Candidate.html` in a browser. Choose an assembly step; new parts appear blue. Use "Only parts added in this step" to inspect a subassembly, and drag to see both sides. For close fitting, use the exact self-contained `build-candidate.mpd` in an LDraw-compatible CAD program. No CAD software or network is needed for the HTML viewer. The animation illustrates pickup/delivery; it does not simulate navigation, contact, friction or loads.

## Specifications

| Item | B0.1 definition |
|---|---|
| Controller | One EV3 brick |
| Motors | Two large drive motors, one medium lift motor; port D spare |
| Steering | Differential drive; two 56 mm tires and rear ball caster |
| Lift | Four 7L parallel links; two 9L forks; 5.4:1 motor reduction |
| Nominal linkage stroke | -18.574 to +25 degrees; about 235.3 motor degrees before calibration |
| Fork entry | Lowest surface about 3.07 mm; highest surface 11.6 mm above floor |
| Pallet | 64 mm forward x 80 mm wide; deck underside 16 mm above floor |
| Ideal final pallet rise | 31.13 mm; illustrative rigid geometry |
| Low-pose overall robot envelope | Approximately 334.9 x 204.2 x 157.8 mm, including assumed camera |
| Camera allowance | 40 x 30 x 24 mm, lens toward front; interface and mass unconfirmed |
| Payload rating | Unassigned until measured balance and loaded tests pass |

The four-bar carriage remains parallel to the chassis. The assembled chassis rests about 1.195 degrees nose-up from its construction coordinate frame to put the caster and both tires on the floor. Do not try to force all beam axes level with the floor.

## Read the geometry

All construction dimensions below are millimeters before the stance rotation. X is forward, Y is left, Z is up. Positive and negative Y are mirror images except for the medium motor, touch switch and stop column. One LEGO hole pitch is 8 mm; L is a hole-count/nominal axle-length convention, not a dimension in millimeters. H1..H7 numbers refer to successive beam holes from the end identified in that instruction. Coordinates refer to hole centers or the source LDraw part origin; a sensor or motor origin is not its center of mass.

`placements.csv` contains every part's exact construction origin and 3x3 rotation matrix. It is an engineering supplement to the visual steps. `parts.csv` counts physical parts: split medium-motor and touch-switch meshes each count as one supplied device. Structural colors in the model are identification aids; compare actual part shapes and quantities in the lab. Station blocks, camera envelope, foam, straps and cables are excluded from the LEGO count. The expanded kit is not presumed to contain all extras.

## Extra equipment and wiring

| Equipment | Quantity / requirement |
|---|---|
| Camera | One fitting the assumed envelope; identify its interface before connection |
| Foam pads | Two, 40 x 30 x 2 mm; lower one on brick, upper one on tray |
| Camera straps | Two reusable ties >=200 mm, about 2.5 mm wide |
| Tray straps | Two reusable ties >=350 mm; keep battery release accessible |
| Cable ties | Small reusable ties as needed on stationary rails |
| EV3 leads | Five: 250 mm lift, 350 mm left, 350 mm right, 250 mm color, 500 mm touch proposed; verify actual reach |
| Target | A raised pallet; a solid cube flat on the floor cannot be entered by these forks |

| Port | Connection | Route |
|---|---|---|
| A | Medium lift motor | Along right fixed bridge, never through gears |
| B | Left large drive motor | Up left tower to brick |
| C | Right large drive motor | Up right tower to brick |
| 1 | Downward color sensor | Behind fixed rear frame to brick |
| 2 | Touch reference switch | Up right fixed stand/bridge with a port service loop |
| D, 3, 4 | Spare | Camera use depends on its actual interface |

A generic USB/web camera needs a compatible host/interface; it cannot be assumed to work in an EV3 sensor socket. Choose an EV3-compatible vision device or an external computer link after identifying the camera. A second EV3 brick is not mechanically required. The camera looks forward from the rear tray; check for lift/brick occlusion using the real camera. No visual-navigation software or camera compatibility is certified by this model.

## Assembly order

Build with power off. Assemble both mirrored sides where indicated. Keep the stated shafts partially withdrawable until their inner spacers and mounting beams are in place. Tighten bushes only enough to locate parts without binding moving links. Do not force a pin if alignment is wrong.


### 1. Side frames

Build two mirrored side frames. Lower 15L rails have hole centers X=-96..16, Y=+/-60, Z=28. Towers stand at X=-88 and -32, Y=+/-68; their bottom holes are Z=28. Put the 3x5 lower braces outside at Y=+/-76. Leave the rear cross-shaft holes and front X=-32/Z=28 holes open. Pin the other lower brace holes. Fit upper 15L brick rails at Y=+/-56/Z=116. At each upper tower joint stack rail / thin beam / tower / thin beam (8+4+8+4 mm), then insert a 3L pin. Do not substitute thick beams for the two thin ones.

[Inspect step 1 in 3D](EV3-Build-Candidate.html?step=1)



### 2. Caster and rear cross shafts

Snap the ball into its socket. The socket mounting holes are X=-88 and -72, Z=28. At each X insert an 8L center axle, then work outward on both sides: tube at Y=12, half bush at 22, stopped joiner at 32, separate 7L outer axle centered at 60, tube at 48, rail/tower/brace stack, half bush at 82 (mirror all Y coordinates). Axles enter opposite ends of the stopped joiner; they do not pass through its center stop. Seat bushes without squeezing the frame.

[Inspect step 2 in 3D](EV3-Build-Candidate.html?step=2)



### 3. Color-sensor cross shafts

At X=-32 fit cross shafts at Z=28 and 68 using the same split 8L/7L axle pattern as the caster. Put a 6536 block at the center of each shaft. The lower block points its pin hole up to Z=36; the upper points down to Z=60. At Z=68 add full bushes at Y=+/-60 and +/-76 around the tower. At Z=28 the existing lower rail and corner brace fill these positions. Keep the original brace pin at X=-32/Z=44.

[Inspect step 3 in 3D](EV3-Build-Candidate.html?step=3)



### 4. Downward color sensor

Use a vertical 7L beam centered at X=-40/Z=44, with its holes facing along X. Its hole centers run Z=20..68. Attach the sensor side mounting bar using 2L pins at Z=28 and 44; the sensor optical face points down. Attach the beam to the two cross-shaft blocks using pins at Z=36 and 60. The sensor body reference is X=-48/Z=36; the optical window is offset toward negative Y. Check the light spot on the floor before tying its cable.

[Inspect step 4 in 3D](EV3-Build-Candidate.html?step=4)



### 5. Drive motors and wheels

Fit two large motors with axle centers X=64/Z=28 and motor origins Y=+/-28. Their rear mounting flange OUTER faces are Y=+/-40. At X=-8 and +8 use inner 2L pin / 2L pin-joiner tube centered at Y=+/-48 / outer 2L pin to reach the lower rail at Y=+/-60. Fit the 9L drive axles centered Y=+/-52, wheel hubs and tires centered Y=+/-64, and outer full bushes at Y=+/-82. Test both wheels independently for free motion.

[Inspect step 5 in 3D](EV3-Build-Candidate.html?step=5)



### 6. EV3 brick

Mount the brick between its upper rails. Brick reference X=-48/Z=116; side mounting holes are X=-80 and -16. On each side use inner 2L pins at Y=36, hollow tubes centered Y=44 and outer pins at Y=52 (mirror for the right side) to reach the rail at Y=56. Insert cables before the camera tray. The tray must remain removable for battery access.

[Inspect step 6 in 3D](EV3-Build-Candidate.html?step=6)



### 7. Lift frames and fixed ties

Build this module off the robot. Two 5x7 frames lie in XZ planes at Y=+/-16, centered X=72/Z=68. Lower shaft holes are X=64,80,96/Z=52. Upper tie positions are X=48 and 80/Z=84; the lower rear tie is X=48/Z=52. Each tie has a 2L tube and full bush inside the frame pair, plus external half-bush retainers. The two upper ties use the extended axles shown in the viewer so the bridge can share them.

[Inspect step 7 in 3D](EV3-Build-Candidate.html?step=7)



### 8. Lower gear train

Insert the lower input shaft at X=64/Z=52, intermediate at X=80/Z=52, output at X=96/Z=52. On the negative-Y layer fit 8T input -> 24T intermediate; on the positive-Y layer fit 8T intermediate -> 24T output. Keep a full bush on the positive input layer at Y=4. The extra 24T gear for the raised drive goes OUTBOARD at Y=44 in step 9. Use the individual bushes shown. Keep the output inner full bush at Y=-4 and half bush at Y=-10. Reserve its two outer ends for the touch stand at Y=-40 and stop anchor at Y=40. Rotate by hand before connecting the motor.

[Inspect step 8 in 3D](EV3-Build-Candidate.html?step=8)



### 9. Raised input and medium motor

Use 12L input and raised shafts centered Y=4. At X=64/Z=84 fit the 40T gear OUTBOARD at Y=44, meshing with an extra 24T at X=64/Y=44/Z=52. The gear pair must not be inside the frame ties. On each shaft a full bush centered Y=32 and half bush at Y=38 locate the gear from inside; a half bush at Y=50 retains it from outside. Fit the vertical 9L motor spine at X=64/Y=-32/Z=84, then the medium motor with two front pins at Z=76 and 92. The motor shaft and raised shaft are coaxial. The resulting motor-to-lift reduction is 5.4:1. The 40T stage increases speed; the two 8T/24T stages reduce it.

[Inspect step 9 in 3D](EV3-Build-Candidate.html?step=9)



### 10. Four lifting links

Use four 7L links: lower fixed pivot X=96/Z=52, upper fixed pivot X=96/Z=84, links at Y=+/-24. Link H1 is the fixed end, H7 the carriage end (48 mm between centers). The two lower links are keyed to the output shaft using 60483 couplers at Y=+/-32 and pins through H2. Upper links rotate freely on the 12L upper pivot axle. Fit only the specified retainers; avoid clamping the links tightly.

[Inspect step 10 in 3D](EV3-Build-Candidate.html?step=10)



### 11. Fork carriage

At each moving end fit a vertical 9L carriage at Y=+/-16: carriage H5 meets the lower link H7; carriage H9 meets the upper link H7. Use frictionless pins at those four pivots. The carriage bottom is 32 mm below the lower moving pivot. Attach a 3x5 L bracket outside each carriage at Y=+/-24, then a forward-facing 9L fork at Y=+/-16. Use pins at the bracket corner, 16 mm above it, and 16 and 32 mm forward. Add both carriage cross ties before testing movement.

[Inspect step 11 in 3D](EV3-Build-Candidate.html?step=11)



### 12. Join lift and chassis

Fit the blue 3x5 adapters outside the lift frames at Y=+/-24, with their horizontal legs on Z=84 and vertical corners at X=48. Add 9L bridge posts at X=48 and 80/Y=+/-32; pin the rear adapter corners at Z=100. Fit side 15L beams at Y=+/-80/Z=116. At X=48 and 80 use 9L transverse axles, hollow tubes at Y=44/60, full spacer at 72, inner half bush at 26 and outer full bush at 88, mirrored on the right. Join side beams to brick rails with two pin/tube/pin stand-offs at X=0 and 8. Support the lift by hand until both sides are attached.

[Inspect step 12 in 3D](EV3-Build-Candidate.html?step=12)



### 13. Touch-switch bracket

Slide the 11L stand onto the negative ends of the output and upper pivot shafts: stand origin X=96/Y=-40/Z=44, supported at Z=52 and 84. Retain outside with half bushes at Y=-46; add an inner half bush at Y=-34 on the upper pivot. The lower drive coupler occupies the inner side of the lower joint. Build lower and upper 3x5 L braces at Y=-32 and -24, with long legs X=96..128/Z=4 and 20. Pin their rear ends to the stand, using a 60483 spacer on the upper rear joint. Mount the upward touch sensor at X=120/Y=-56/Z=12, with 3L backing beam at Y=-48. At X=120/Z=4 and 20 use 6L clamp axles centered Y=-40: sensor bar, backing beam, full-bush spacer at Y=-40, then brace and filler bush. At Z=4 use lower L at Y=-32 and filler at -24; at Z=20 filler at -32 and upper L at -24. Retain at Y=-62 and -18. Extended button tip: X=104/Y=-56/Z=44. Keep the sensor housing clear of the right tire.

[Inspect step 13 in 3D](EV3-Build-Candidate.html?step=13)



### 14. Touch-switch trigger

Attach a red 3L trigger at Y=-48 using lower-link H3 and H5. At each joint work outward from the link at Y=-24: inner 2L pin centered Y=-28, 2L hollow pin-joiner tube at Y=-36, outer 2L pin at Y=-44, trigger beam at Y=-48. These two stand-offs keep the trigger aligned; one pin would let it swing. Near the low position its rear rounded end presses the edge of the touch button. Displayed compression is illustrative, up to 1.8 mm. Check the real electrical trip and travel before powering the lift; the switch must trip before the hard stop.

[Inspect step 14 in 3D](EV3-Build-Candidate.html?step=14)



### 15. Fixed stop column

At the positive-Y ends of the output and upper pivot shafts fit 6536 blocks with their pin bores along Y at X=96/Y=40/Z=52 and 84. Their axle bores point vertically at X=104/Y=40, forward of the output axis. Pass a 12L axle vertically through both; its center is Z=60. Fit column locators centered Z=46 and 90. At the upper pivot add an inner half bush at Y=34; retain both anchors with half bushes at Y=46. The column is stationary while the lower output shaft turns inside the round anchor bore.

[Inspect step 15 in 3D](EV3-Build-Candidate.html?step=15)



### 16. Lower mechanical stop

Slide a keyed 60483 coupler onto the column at Z=24.2 and a horizontal red 5L beam above it at Z=32.2, with beam holes along X=96..128 and vertical hole axes. The column passes through beam H2 at X=104; point the key coupler rearward and pin its round hole to beam H1 at X=96. Half bushes on the column at Z=18.2 and 38.2 retain the assembly. Pin a 6536 carrier at X=112/Y=40/Z=40.2 to beam H4 at X=120; its axle bore points along Y. Insert a 5L transverse stop axle centered Y=32 and retain at Y=34 and 46. This axle sits just BELOW the lower left link in the commanded low pose. The fractional height is set by sliding bushes, not by forcing a LEGO grid connection.

[Inspect step 16 in 3D](EV3-Build-Candidate.html?step=16)



### 17. Upper mechanical stop

Make the second keyed stop assembly with its horizontal 5L beam at Z=76, 60483 key below at Z=68, and lower column retainer at Z=62. The fixed upper column anchor retains it from above. Pin the 6536 carrier below beam H4 so the 5L stop axle is at X=112/Z=68, pointing along Y and centered Y=32. Retain at Y=34 and 46. It sits ABOVE the lower link near the +25 degree commanded high position. Turn the lift by hand to both physical stops before motor testing.

[Inspect step 17 in 3D](EV3-Build-Candidate.html?step=17)



### 18. Camera tray

Place a 40x30x2 mm foam pad on the rear brick roof, centered X=-80/Y=0/Z=124.6. Put a horizontal 5x7 frame above it, centered Z=129.6, with its 40 mm dimension along X. Strap frame and brick together at X=-96 and -64 using two reusable ties at least 350 mm long. Route below the brick without trapping cables or the battery release. Place a second 40x30x2 mm pad on top of the tray. The upper pad clears the tray tie bands.

[Inspect step 18 in 3D](EV3-Build-Candidate.html?step=18)



### 19. Camera fit check

The orange block is an assumed camera envelope, not a purchased camera: maximum 40 mm X by 30 mm Y by 24 mm Z. Put the lens toward +X. Use two reusable ties at least 200 mm long at X=-92 and -68 around camera and tray, keeping the lens clear. The target camera underside is Z=135.6. A different camera requires a revised holder; electrical compatibility and field of view are still conditional on its exact model.

[Inspect step 19 in 3D](EV3-Build-Candidate.html?step=19)



### 20. Wiring and first power-on

With power off: medium lift motor -> A; left and right drive motors -> B and C; color sensor -> 1; touch sensor -> 2; leave D,3,4 free. Reserve 250 mm for A, 350 mm each for B/C, 250 mm for color, 500 mm for touch, subject to actual cable reach. Route drive cables up the stationary towers, color behind the brick, and touch up the right stationary stand and bridge. Tie to stationary rails with small reusable ties; leave slack at ports and keep every loop away from gears, links, tires and the floor. Camera cable is separate and depends on its interface. Do not plug a generic camera into an EV3 sensor port.

[Inspect step 20 in 3D](EV3-Build-Candidate.html?step=20)



### 21. Calibration and acceptance

Start with wheels raised and no load. Verify motor directions and sensor readings. Test the lift by hand first; confirm the switch releases when lifting. Home downward at low power with a timeout and stop immediately on switch press; set encoder zero there. Start with a short upward move, then approach a conservative travel limit below the nominal 235 motor degrees. Confirm both hard stops remain outside the normal commanded stroke. Test straight travel, turns, cable sweep, empty pallet pickup and then gradual test loads. No payload rating is assigned until measured balance and loaded trials pass.

[Inspect step 21 in 3D](EV3-Build-Candidate.html?step=21)



## Verification and release gate

The recorded checks are in `verification.json`, browser checks in `browser-checks.json`, and selected whole-structure section samples in `whole-structure-audit.json`. The section audit compares actual LDraw surfaces at three poses on a 0.4 mm grid in three transverse planes per overlapping pair. It omits fasteners, flexible consumables and detailed gear contact. The only recorded overlap flags left in that audit belong to the supplied touch sensor's own body/button; these are not external structural clashes. This is a useful sampled check, not a complete 3D collision proof.

The 71 animation poses contain only 15 distinct linkage angles. Checks cover floor clearance in all 71, source-hole alignment for the mounts, the trigger's two pin axes, motor flange spacing and sampled mechanical-stop contact. The camera and flexible cables require real equipment for fit validation. The stop-contact search uses a 0.05 mm section grid, not a strength calculation.

Before releasing this as a proven build, record these lab results:

1. Count the actual core plus extended inventory against `parts.csv` and list substitutions.
2. Check all pins seat fully and all axles are retained; gently twist the chassis and bridge to identify loose stand-offs.
3. Turn the complete lift by hand with cables installed; it must move freely without touching tires, sensor housing or cable loops.
4. Read the real touch input while lowering by hand. It must trip before the lower mechanical stop and release on ascent; avoid using the motor to force an uncalibrated switch.
5. Confirm the hard stops limit overtravel and the forks remain clear of the floor. Stop assemblies rely on sliding bushes; check that they do not migrate under gentle manual force.
6. Check camera fit, view and connection; secure the cable and confirm the brick controls and battery remain accessible.
7. Raise wheels for the first motor-direction test. Use low lift power, encoder bounds and a timeout; a software stop must precede a mechanical stop in normal use.
8. Measure mass and balance with the actual battery/camera. At maximum reach, require a chosen restoring/overturning moment margin (for example 1.5) before increasing load. This model supplies no measured payload rating.
9. Run repeated empty-pallet cycles and turns, then add load gradually. Record payload, cycle count, binding, tipping, slipping and structural changes. Accept a payload only after these tests.

## Changes from the saved version

- Corrected the large-motor flange spacing by moving each motor 4 mm inward; axle and wheel centers remain as specified.
- Moved the raised 40T/24T stage outboard to clear the fixed cross ties. Replaced unsupported sensor placements with actual pinned brackets and a two-pin lift trigger.
- Moved the upper color cross brace clear of the drive motors.
- Replaced stop boxes with a fixed column, keyed beam assemblies and retained transverse stop axles.
- Added a removable camera tray, pads and explicit reusable straps, using a stated camera envelope.
- Added a step-selectable offline viewer, exact part placements, a combined physical bill and wiring/calibration instructions.

## Provenance and reproduction

Structural surfaces are from the official LDraw library, https://library.ldraw.org/ . Authors and CC BY 2.0/4.0 license headers are preserved inside `build-candidate.mpd`; see also `ATTRIBUTION.md`. Original assembly, fixtures and guides are authored by this project. This is an unofficial design.

From the workspace, regenerate in order: `python design/cad/build_candidate.py`; `python design/cad/audit_structure.py`; `python design/cad/verify_candidate.py`; `python design/cad/write_candidate_guide.py`; then run `design/build_candidate/verify_viewer.ps1`. The first-build package contains the required Python sources and LDraw subset. The viewer and MPD are independently usable offline.
