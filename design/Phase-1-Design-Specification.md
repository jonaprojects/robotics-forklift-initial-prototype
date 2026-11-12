# EV3 forklift - phase 1 design review, P1-R1

> Later work: [Phase 2 digital lift review](cad/Phase-2-Review.md) corrects the gearbox and carriage geometry below. This file remains the historical candidate specification.

**Status: candidate design; exact assembly specification incomplete.**

This document replaces the general V0.1 proposal as the engineering baseline. It records a selected mechanism, actual LEGO element references, connection requirements and analytical verification. It is not a complete instruction book or a statement that a one-kit build has been verified.

## 1. Scope and selected architecture

Retain one EV3 brick, two large drive motors and one medium lift motor. Use LEGO's official EV3 Driving Base as the drivetrain reference, including its chassis, ball caster, wheels and brick mounting. The reference is the 46-page `sources/driving-base.pdf`, printed assembly steps 1-45. Its existing internal connections are defined by that document; this avoids inventing motor-housing mounts.

The proposed custom front attachment is a two-sided parallelogram lift with two forks. It transports a pallet between floor-level stations. It does not stack on shelves or provide powered mast tilt. The standard driving base has a relatively high brick position; the earlier suggestion to put the brick low at the rear is not part of this reference chassis. Balance must therefore be evaluated on this actual configuration, not assumed from the earlier drawing.

The complete Driving Base cannot yet be declared compatible with the custom lift. The custom attachment, sensor brackets and camera interface require the unresolved connections in section 8. The published Medium Motor Module is useful for inspecting motor mounting and shaft arrangements; its powered grab-frame is NOT the proposed fork lift and is not silently counted as a finished attachment.

## 2. Coordinate and hole conventions

- Global X points forward, Y left, Z up. Units are millimeters.
- Lift local origin is the center of its lower driven axle. The global location of this origin relative to the stock chassis is unresolved (U01).
- Beam holes are H1 through Hn, numbered from the pivot end for links, bottom upward for carriage sides.
- A 5x7 frame is oriented in the XZ plane with its 7L edge horizontal: its end-hole centers span 48 mm horizontally and 32 mm vertically. Frame front edge is X=0; rear edge is X=-48.
- Candidate left/right fixed frame center planes are Y=+16/-16. Link center planes are Y=+24/-24. The 2L axle-hole couplers sit one layer farther outward, Y=+32/-32.
- These coordinates specify nominal connection centers. They are not a solid-model collision check or a confirmed fit for gear hubs.

## 3. Lift geometry and torque path

Each side has a 7L upper link, 7L lower link and vertical 5L carriage side. Link endpoint hole spacing is 48 mm; both fixed and moving upper/lower pivots are 32 mm apart.

At angle theta, the carriage lower pivot is `(48 cos(theta), Y, 48 sin(theta))`; the upper pivot is 32 mm directly above it. Both forks are rigidly attached to the carriage and remain level in the ideal mechanism. Theta is commanded from -10 to +25 degrees. No assembly is allowed to pass through a joint limit or collision in obtaining this stroke.

**The drive connection must be keyed.** The supplied straight 7L beams have round holes. A driven axle through H1 alone cannot rotate them positively. On each lower link, the proposed 2L beam with crosshole has its crosshole coaxial with H1 and its round hole pinned to H2. This creates a torque-transmitting connection. Both lower links are driven by the same axle; upper links are free followers. This corrects a missing detail in V0.1.

Candidate gear train, using the double-bevel gears listed in the official inventory:

1. Input shaft: 12T gear.
2. Intermediate shaft: 36T and 12T gears keyed to the same shaft.
3. Output shaft: 36T gear keyed to the driven lift axle.
4. Three parallel shaft centers at X=-48, -24 and 0, all at local Z=0.
5. Stage-1 nominal gear center plane Y=-4; stage-2 plane Y=+4.

This is 9:1 speed reduction. Two external meshes preserve direction. A 35-degree output stroke requires 315 motor degrees, before backlash and calibration. The two 5x7 frames are candidate shaft supports. Exact spacers and motor coupling are not released: nominal pitch alignment does not prove that hubs, shafts and motor body fit.

The proposed output axle is 12L (96 mm). A simplified layer stack has bearing frames at +/-16, links at +/-24, drive couplers at +/-32 and retaining bushes at +/-40. This consumes 88 mm outer-to-outer under an 8 mm layer assumption. Exact part thicknesses and retention need solid-part verification.

## 4. Pallet and forks

Use an external test pallet, 80 mm across Y and 64 mm deep along X. It has an 8 mm deck with its underside 16 mm above the floor. Three 16 mm-wide runners centered at Y=-32, 0 and +32 form two 16 mm-wide channels centered at Y=-16 and +16. Runners run along the full depth; channel entrances stay open.

Two 9L fork beams have nominal length 72 mm, 8 mm width and thickness, with centers Y=-16 and +16. Plan for 48 mm unobstructed insertion and 24 mm for the rear connection region. Their low-position underside is 4 mm above the floor. This leaves 4 mm vertical clearance above the forks and 4 mm clearance on each side inside the channels.

The cross-fork connection must resist pitching and twisting at two points; a single free pin is insufficient. The exact perpendicular brackets tying the forward forks to the vertical carriage beams are unresolved (U04). This is a major assembly interface, not a cosmetic detail.

Nominal lift stroke is 28.6 mm. The first 4 mm takes up the initial fork-to-deck gap; actual pallet-floor clearance is therefore about 24.6 mm, rather than the full stroke. The carriage first advances slightly as the arms pass horizontal and then retreats. Full fore-aft excursion is about 4.5 mm; the net endpoint retreat alone is about 3.8 mm. Station guides must permit the full sweep.

Use a secured 40 mm cube of at most 50 g initially. Budget at most another 50 g for the pallet. These are starting assumptions, not measured capacity. Pallet construction material is external to the assumed kit and may be LEGO, card or another course-permitted material.

## 5. Parts identification and allocation

`phase1-model.json` lists the proposed lift's currently specified stock with official **element IDs** (color-specific identifiers, not generic design numbers). It records 14 element types, required quantities and the whole kit's available quantities.

Confirmed from LEGO's official element survey:

- Four 7L beams, element 4495930: all four proposed for the lift links.
- Four 2L beams with crosshole, element 6006140: two proposed as lower-link drive couplers.
- Three 5x7 frames, element 4539880: two proposed for the lift, while the Driving Base uses one.
- Two 12T double-bevel gears, element 4177431, and two 36T double-bevel gears, element 4255563: all proposed for the reduction train.
- Six 9L beams, element 4211866: two proposed for the forks.
- Two 12L axles, element 370826: one proposed for the output shaft.

This verifies existence and isolated quantities, not the full combined bill of materials. Remaining brackets, bracing, pin spacers and sensor mounts have not been allocated. No claim that one kit is sufficient for the whole proposed assembly is justified yet. Do not buy extras based on this partial allocation.

## 6. Connections defined so far

The machine-readable connection register C01-C14 is in `phase1-model.json`. It specifies the four moving carriage joints, upper follower pivots, lower driven pivots, axle-hole drive couplers and both gear meshes. Chassis-internal connections are incorporated by reference to the exact Driving Base instructions.

Suggested assembly dependency order is: stock driving base -> fixed lift module and gearbox -> links and carriage -> fork brackets -> lift limit/stop -> sensors -> camera mount. This is a dependency plan only; final step numbers and page illustrations follow a complete connection model.

## 7. Electrical and control interfaces

| EV3 port | Device | Provisional cable allocation |
|---|---|---|
| A | Medium lift motor | 25 cm |
| B | Left large drive motor | 35 cm, per base reference |
| C | Right large drive motor | 35 cm, per base reference |
| 1 | Color sensor | 25 cm |
| 2 | Lower-limit touch sensor | 25 cm |
| 3 | Reserved for camera only if EV3-compatible | Depends on actual camera |
| D / 4 | Spare motor / sensor port | No assignment |

The official kit has enough cables for these first five connections, but route lengths and strain relief must be checked against the assembled model. Camera interface remains unspecified: it is absent from the kit and its identity is unknown. Reserve it as an external device, not a proven EV3 sensor.

Lower slowly to a touch switch, stop, establish a motor encoder reference, then operate within calibrated bounds. Include independent hard stops, a homing timeout and a stop on failed homing. Spur gearing is not a mechanical lock; holding behavior requires a powered-hold test. Test the mechanism manually before applying motor power.

## 8. Verification disposition and completion gate

Run `python design/verify_phase1.py`. The report is `Phase-1-Verification.md`. An exit status of **2 means the assembly release is blocked**, even if all analytical checks pass.

The following are unfinished exact connections, enumerated U01-U08 in the machine-readable file:

1. Four-point or otherwise rigid lift-to-stock-chassis attachment with actual hole locations.
2. Medium-motor housing bracket and input shaft coupling.
3. Cross-bracing and spacer stacks between the fixed frames.
4. Fork-to-carriage brackets and carriage cross-bracing.
5. Touch-sensor mount, switch actuator and upper/lower hard stops.
6. Color-sensor mounting bracket.
7. Camera mounting and electrical interface.
8. Complete combined part allocation after all the above are specified.

**Phase 1 is complete only when these entries become explicit part-and-hole connections and the aggregate bill of materials reconciles.** The next work must resolve these interfaces, using actual part geometry where needed. It would be misleading to start an authoritative instruction book before that gate passes. The current analysis establishes a candidate geometry, not a complete LEGO assembly.

## 9. Sources and provenance

- [LEGO 45544 official element survey](https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltd9e811d9ff83b385/5f8801d5887a311d8fa19812/45544_element_survey.pdf?locale=en-gb), local copy `sources/inventory.pdf`.
- [LEGO Driving Base, 46-page reference](https://assets.education.lego.com/v3/assets/blt293eea581807678a/blt6e7360758df8f1ea/5ec7c6dd2238e044d39d24b0/ev3-rem-driving-base.pdf?locale=en-us), local copy `sources/driving-base.pdf`. Pages were rendered and inspected to distinguish the reference chassis from the proposed custom lift.
- [LEGO Medium Motor Module, 21-page reference](https://assets.education.lego.com/v3/assets/blt293eea581807678a/blt2e65cac565ac7465/5ec7c6ccf32b1a633f902a82/ev3-medium-motor-driving-base.pdf?locale=en-us), local copy `sources/medium-module.pdf`. This is a powered frame attachment, not a level fork carriage.
- [LEGO EV3 user guide](https://www.lego.com/cdn/cs/set/assets/bltbef4d6ce0f40363c/LMSUser_Guide_LEGO_MINDSTORMS_EV3_11_Tablet_ENUS.pdf), motor specification: medium-motor running torque 8 Ncm. Torque estimates assume 50% transmission efficiency and 200 g total vertically moving mass; neither assumption has been measured.

References define LEGO parts and the stock chassis. The custom geometry, coordinates and calculations are original engineering proposals. No collision-checked CAD model or physical build is claimed.
