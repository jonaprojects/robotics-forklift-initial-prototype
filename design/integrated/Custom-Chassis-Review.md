# EV3 custom chassis development I0.3

**Status: detailed mechanical candidate, not an instruction-book release.**

This revision replaces the merged chassis image with individual LEGO parts. The scene now contains 235 physical LEGO pieces, plus separately flagged camera/stop envelopes and pallet/station fixtures. The EV3 medium motor is counted as one physical assembly even though its body and rotor are separate digital references.

## Current deliverables

- `EV3-Integrated-Viewer.html`: offline 3D viewer and prescribed pickup/delivery sequence.
- `robot-station.mpd`: all geometry embedded; no merged chassis proxy.
- `catalog-parts.csv`: every currently placed LEGO component, core-set comparison and minimum extras. Future sensor brackets and the actual camera are excluded.
- `custom-chassis-checks.json`: connection-center checks, actual support contacts and stance values.
- `integration-checks.json` and `forward-layout-checks.json`: additional targeted geometry checks.

## Mechanical changes

The lower frame uses two 15L side rails. Each large drive motor connects at two rear mounting holes through an inner friction pin, a 2L pin-joiner tube and an outer friction pin. These are explicit parts at specified positions; there are no invisible motor supports.

Two split cross shafts brace the rear rails and pass through the caster socket's two mounting holes. Each shaft uses an 8L central axle, two stopped axle joiners and two 7L outer axles. Hollow tubes and half bushes locate the rails and corner-brace stacks. The joiners receive separate axle ends; stopped joiners are not incorrectly threaded onto uninterrupted axles.

Four 15L towers connect the lower rails to two upper brick rails. Lower 3x5 right-angle braces constrain the tower angles. At the upper joints a 3L pin passes through an **8 + 4 + 8 + 4 mm stack**: upper rail, inner thin beam, tower and outer thin beam. The 4 mm pieces are real thin liftarms, not scaled standard beams. The EV3 brick connects to the upper rails through four explicit pin/tube stand-offs.

The bridge to the lift is now represented by catalog components. Two upper side beams attach to the brick rails through two stand-offs per side. Four upright 9L posts connect the side beams to two 3x5 adapters on the lift frames. Each adapter has two lower shaft connections plus an upright locking pin, avoiding a freely swinging one-pin attachment. Shaft spacer stacks are modeled individually. Connection axes are checked, but full pin insertion paths and loaded rigidity are not yet verified.

## Stance and fork calibration

A level version of this frame leaves the 18 mm caster ball about 3 mm above the design floor. Rather than hiding that discrepancy, the complete rigid body is pitched approximately **-1.195 degrees about the drive axle**. Both tires and the caster ball now contact the same floor in the digital geometry.

The fixed lift assembly is raised 4 mm to share the chassis mounting grid. The lowered linkage angle is recalculated to approximately **-18.574 degrees**, making the highest fork surface 11.6 mm above the floor. The lowest fork surface is about 3.07 mm above the floor. The pallet deck underside remains at 16 mm, so nominal insertion clearance above the forks is 4.4 mm.

The forks remain level relative to the chassis, and therefore have the chassis's small pitch relative to the floor. Pallet movement is an illustration, not a friction/contact solver. Final ideal pallet rise is approximately 31.13 mm. The retained 5.4:1 train requires approximately **235.3 motor degrees** between the recalculated low angle and +25 degrees, before backlash and calibration. Old I0.2 stroke and clearance values are superseded.

## Verification scope

The current checks include 50 chassis/brick/caster/bridge, support and clearance checks, eight integration checks and five forward-layout checks. Source-part hole axes, not idealized beam centerlines, are used for connection matching. Floor contacts and the long-pin stack spans are measured from actual part meshes. The new input gear stage is sampled in its center plane over the lifting stroke. The files record the actual pass/fail results.

A matching axis is necessary but insufficient to prove a legal LEGO connection. Exact bore depth, friction fit, unsupported bending of long pin/tube stand-offs, axle retention, assembly access and the whole model's swept collisions still require review. No physical build or load test has been observed.

## Inventory and extended kit

The user reports that an extended kit may be available. Its identity and inventory are not confirmed. Extras are therefore permitted provisionally, with quantities kept visible rather than attributed to an unidentified set. Structural colors in the viewer are identification aids; equivalent pieces in another color may be usable.

This is not a one-core-set design. The current parts list contains substantial overdraw in bushes, pin-joiner tubes, thin beams and some standard beams/axles. Compare `catalog-parts.csv` with the lab's actual combined inventory before treating it as a build plan or buying parts. The final bill will also need the remaining sensor/stop mounts, cables and camera hardware. No parts have been purchased.

## What remains open

1. Review the chassis/bridge stand-offs for real pin engagement, assembly access, stiffness and interference. Small nominal clearances must be tested on actual pieces.
2. Replace the color/touch sensor placements with bracket assemblies and a working lift-reference trigger.
3. Replace stop envelopes with independent physical stop assemblies; check them against the revised lower angle.
4. Identify the camera, mount it using its real dimensions, and model cable routes and the actual brick battery configuration.
5. Recalculate balance using the custom chassis's actual weights and CG. The old 0.85 kg reference-chassis calculation is historical and must not be presented as proof of this new structure's stability.
6. Reconcile all remaining parts with the available core plus extended equipment and validate the complete assembly sequence before generating the instruction book.

## Sources and reproduction

All structural geometry comes from the official LDraw part library, https://library.ldraw.org/ . Authors and CC BY 2.0 / 4.0 license statements are preserved inside the MPD. License links: https://creativecommons.org/licenses/by/4.0/ and https://creativecommons.org/licenses/by/2.0/ . The original assembly and connection layout are authored by this project. The former RobotDSL merged base is no longer part of this scene.

In the project workspace run `python design/cad/build_integrated.py`, `python design/cad/verify_custom_chassis.py`, and `python design/cad/verify_integrated.py`. The first imports `custom_chassis.py`. Browser smoke checks use `design/integrated/verify_viewer.ps1`. Geometry regeneration requires the local LDraw subset; the exported viewer and MPD can be inspected independently.

Official core-inventory reference for the stock comparison: https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltd9e811d9ff83b385/5f8801d5887a311d8fa19812/45544_element_survey.pdf?locale=en-gb . No extended-set inventory has been assumed.
