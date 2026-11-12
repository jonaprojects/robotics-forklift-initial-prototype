# EV3 forklift — preliminary design V0.1

> Superseded engineering details: see [the digital lift review](design/cad/Phase-2-Review.md) and [offline 3D viewer](design/cad/EV3-Lift-Viewer.html). The digital work corrects several connections and identifies additional small parts. This original proposal is not an assembly manual.

Purpose: a proposal for team discussion and a first laboratory prototype. Dimensions below are design targets, not measured performance. This is an assembly plan, not a verified pin-by-pin LEGO instruction set. Confirm inventory, clearances, gearing and balance during construction.

## 1. Proposed machine

One EV3 brick controls two independently driven wheels and one fork-lifting motor. A rear ball caster supports the chassis. The brick sits low toward the rear. A fixed camera looks forward toward the pickup station. A color sensor looks down at the route.

The load sits on a small pallet. Two parallel forks enter underneath it. A short parallelogram linkage raises the forks while keeping them approximately level. This replaces a tall sliding mast for the first prototype; it is a low-lift pallet transporter with forklift-style handling. A true vertical mast can be a later revision if shelf stacking becomes a requirement.

## 2. Working assumptions and target dimensions

| Item | Initial target |
|---|---|
| Kit | EV3 Education Core Set 45544; actual inventory to confirm |
| Surface | Flat, smooth indoor floor |
| Chassis footprint, excluding forks | Approximately 240 x 180 mm; adjust to actual motor mounting |
| Overall length with forks | Approximately 310–330 mm |
| Load | One light cube, approximately 40 x 40 x 40 mm |
| Initial payload | 50 g maximum for the first tests; pallet weight is additional |
| Pallet | Approximately 80 mm wide x 64 mm deep |
| Pallet underside clearance | At least 16 mm inside the fork channels |
| Forks | Two beams, approximately 72 mm long; 48–56 mm usable insertion |
| Fork center spacing | 32 mm; match pallet channels to this spacing |
| Fork thickness | Approximately 8 mm; verify actual orientation and connectors |
| Fork underside clearance when lowered | Target 4–6 mm on the actual floor |
| Useful lift travel | Approximately 25–30 mm |
| Navigation | A dark route line with colored station markers; camera for final alignment if compatible |
| Powered mast tilt | Omitted from first prototype |

LEGO Technic hole pitch is 8 mm. A 7L beam has six hole intervals between its end holes: 48 mm. Specify hole intervals when laying out linkages, rather than confusing beam length with pivot spacing.

The chassis dimensions may grow once real parts are placed. Do not shorten the wheel track just to meet the nominal width. The payload target is a test starting point, not a certified lifting capacity.

## 3. Equipment and provisional parts list

- 1 EV3 brick and battery.
- 2 large motors, 2 matching drive wheels and tires, 1 rear ball caster or free-swiveling support.
- 1 medium motor for the lift.
- 1 color sensor; 1 touch sensor for the lowered lift reference.
- Camera with its interface and computing hardware still to be identified. It is an additional item, not assumed to be supplied in the core set.
- Two rigid side structures and several cross-members for the chassis; use long beams and Technic frames available in the lab.
- Four matching 7L beams for the lift links, two equal-height fixed pivot supports and two equal-height moving carriage sides.
- Two straight 9L beams for the forks, plus cross-members and connectors.
- Axles, bushes and pivot connectors; use low-friction joints at moving pivots.
- A gear reduction for the lift. Candidate: a 12-tooth gear driving a 36-tooth gear, repeated on a compound intermediate shaft, for 9:1 reduction. Use only if these gears and mounting clearances are available. The exact gear inventory is not yet verified.
- A small pallet and visible station target. Pallets and station guides may need additional LEGO pieces or permitted non-LEGO material.

This is a functional shopping/checking list, not an assertion that every proposed part fits within one unmodified kit.

## 4. Motor and sensor connections

| Port | Assignment |
|---|---|
| A | Medium lift motor |
| B | Left large drive motor |
| C | Right large drive motor |
| D | Spare |
| 1 | Downward color sensor |
| 2 | Lift lower-limit touch sensor |
| 3 | Reserved for compatible camera, if it uses an EV3 sensor port |
| 4 | Spare / optional distance sensor |

A generic webcam is not assumed to connect to sensor port 3. Its eventual processing and communication architecture must be decided after identifying it. Motor direction signs must be calibrated because the drive motors may be mounted as mirror images.

## 5. Assembly sequence

### A. Make the pallet first

1. Make a stiff platform approximately 80 x 64 mm.
2. Support it so there are two unobstructed fork channels, centered 32 mm apart. Leave at least 16 mm of vertical clearance; make each channel comfortably wider than the fork, initially about 16–20 mm clear width.
3. Keep channel entrances open and avoid low cross-members that would block insertion.
4. Fix the cube to the pallet for the first tests. Loose-load handling comes later.
5. Slide two loose fork beams underneath by hand. Confirm that they can support and release the pallet without snagging.

### B. Build the chassis

1. Make a rectangular chassis with two side structures joined by front, middle and rear cross-members. Reinforce joints so it does not twist when lifted by a corner.
2. Mount one large motor on each side, driving matching wheels directly. Put the wheel axle line near the front of the chassis, behind the lifting linkage.
3. Fit the rear caster centrally. Check that all three ground contacts carry weight and that the chassis sits level.
4. Mount the EV3 brick low, behind the drive-wheel axle. Leave access to buttons, ports and battery.
5. Add a rigid front cross-member for the lift. Keep its loads out of the color sensor bracket.
6. Secure cables away from wheels and all moving linkage positions.

### C. Build the level-lifting linkage by hand

Build this as a separate module before adding its motor.

1. On each side of the module, make two fixed pivot holes separated vertically by four hole intervals (32 mm).
2. Make matching moving carriage sides with the same 32 mm vertical pivot spacing.
3. Connect each fixed side to its moving side using two 7L beams. Use the end holes, giving 48 mm link pivot spacing. There are four links in total, two per side.
4. The fixed pivots and moving pivots must form a parallelogram on each side. Do not pin the moving joints rigidly. Both sides must move freely through the same angle range.
5. Join the moving sides with cross-members to form a stiff carriage. Fix the two forks to that carriage, pointing forward, spaced 32 mm center to center.
6. Couple the lower links through a shared driven axle; fix those links to the axle with suitable axle-hole connectors. Merely putting a round-hole beam over an axle will not transmit torque. Keep the upper links as freely rotating followers.
7. Arrange the geometry so the links move approximately from 10 degrees below horizontal to 25 degrees above horizontal. With 48 mm links this gives about 29 mm of rise and about 4 mm of rearward movement. Actual limits must be checked for collisions.
8. Adjust the fixed pivot height and fork mounting until the lowered forks clear the floor by 4–6 mm while fitting beneath the pallet. Exact brackets depend on the pieces available.
9. Add a lower stop and an upper stop outside the normal commanded range. Avoid linkage positions near vertical where the geometry becomes unfavorable.

The carriage follows an arc, not a perfectly vertical path. The small rearward movement must not pull the pallet into the chassis or bind against station guides. This design only serves low pickups and drop-offs.

### D. Add the lift motor and reference switch

1. Mount the medium motor rigidly to the fixed lift structure or chassis.
2. Connect it to the lower-link driven axle through reduction gears. For the candidate 9:1 train: motor 12T -> intermediate 36T; a 12T fixed on that SAME intermediate shaft -> output 36T. The intermediate gears rotate together. Lay out gear centers for proper meshing; do not force a mesh to fit convenient holes.
3. Support loaded gear shafts on both sides where possible. Use bushes to prevent sideways axle movement.
4. Mount the touch sensor so the carriage presses it just before reaching the lower mechanical stop.
5. At startup, lower slowly until the switch activates, stop and zero the motor position. Add a timeout so a missing switch cannot run the motor indefinitely.
6. For a 35-degree linkage movement, a 9:1 train requires about 315 degrees of motor rotation, assuming a rigid direct output connection. Calibrate the actual raised position slowly; do not assume this calculated value is collision-free.
7. Test the controller's available position-hold mode. Spur gears can back-drive; the gearing is not a mechanical lock. Check for descent over 10 seconds with the intended load. If it drifts, reduce the load, change reduction or add a suitable holding mechanism before transport.

### E. Add the sensing brackets

1. Put the color sensor on a stiff downward-facing bracket close to the floor. Set its final height through black/white calibration on the actual floor and check clearance across the whole lift stroke.
2. Leave a camera mounting point above the lift, with an unobstructed view of a target on the pickup station. Choose final height and angle only after checking the camera's focus and field of view.
3. Use a target above pallet level so it stays visible during approach. Keep it out of the load's path.
4. Make all brackets easy to adjust without dismantling the drivetrain.

## 6. First demonstration and control sequence

First demonstrate pickup with the robot positioned manually. Then add a straight-line approach to one station. Only after those work, add route following and camera alignment.

Proposed sequence:

1. Reference the lift using its lower-limit switch.
2. Follow the route toward a selected station.
3. Stop at its marker. Do not assume a single color sensor can simultaneously read an intersecting marker and track the line; define a short marker-reading maneuver.
4. Align using the station target, once camera compatibility and detection are established.
5. Creep forward to the calibrated insertion depth.
6. Stop both drive motors, lift the pallet and hold position.
7. Reverse clear of the station and travel slowly with the load low.
8. At the destination, stop, lower onto the floor and reverse to withdraw the forks.

Centered in an image does not by itself prove correct distance or heading. Use a known target geometry, repeatable station layout and tested insertion distance. Short flared guide rails may help, but they must clear the pallet and permit withdrawal. If a target is lost or insertion is uncertain, stop rather than raise blindly.

## 7. Laboratory acceptance checks

| Check | Initial acceptance target |
|---|---|
| Free linkage movement | Full stroke by hand without binding |
| Empty lift | 10 cycles without gear skipping or collisions |
| Loaded lift | 10 cycles with a 50 g cube plus the actual pallet |
| Load holding | No visible descent over 10 seconds |
| Static balance | Rear caster remains in contact with the floor with the load raised |
| Loaded movement | Slow starts, stops and turns without tipping or losing the pallet |
| Manual-alignment pickup | 10 consecutive successful pickup/drop-off cycles |
| Automatic docking | Record success over 10 attempts; report the observed rate |

If the rear caster unloads, bring the load closer to the drive axle, reduce payload, or move the existing brick rearward. Recheck dynamic balance; static contact alone does not prove turn or braking stability.

Record the final wheel diameter, chassis width, fork height/spacing, gear ratio, lift positions, payload including pallet, camera model, software environment and every structural substitution. These measurements become the basis for a verified V1 guide.

## 8. Items to resolve at the lab

- Actual kit inventory, especially lift gears, frames and pivot connectors.
- Whether the course permits a parallelogram low lift or requires a vertical mast / shelf stacking.
- Camera model, connection and processing computer, if required.
- Actual pallet and cube dimensions and mass.
- Required course, station spacing and allowed guides.

## References

- [LEGO official 45544 element survey](https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltd9e811d9ff83b385/5f8801d5887a311d8fa19812/45544_element_survey.pdf?locale=en-gb): check proposed parts against the actual inventory.
- [LEGO Move Objects lesson](https://education.lego.com/en-us/lessons/ev3-tutorials/move-object/): reference driving base and motorized object-handling attachment. Not instructions for this custom linkage.
- [LEGO EV3 user guide](https://www.lego.com/cdn/cs/set/assets/bltbef4d6ce0f40363c/LMSUser_Guide_LEGO_MINDSTORMS_EV3_11_Tablet_ENUS.pdf): brick, motor and sensor reference.

The custom dimensions, linkage and test procedure above are a proposed engineering design, not an official LEGO model or a tested build.
