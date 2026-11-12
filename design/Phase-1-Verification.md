# Phase 1 verification report - P1-R1

**Release status: HOLD. Phase 1 is not fully complete.**

Analytical checks below apply to an idealized candidate. They do not verify an assembled LEGO model.

| Check | Result | Evidence |
|---|---|---|
| Lift target | PASS | 28.621 mm rise |
| Endpoint fore-aft shift | PASS | -3.768 mm; not the full swept excursion |
| Full fore-aft excursion | PASS | 4.497 mm; carriage initially moves forward, then rearward |
| Ideal parallelogram closure | PASS | maximum residual 7.11e-15 mm over 351 positions |
| Gear reduction | PASS | 9:1; motor travel 315 degrees |
| Gear stage 1 nominal pitch spacing | PASS | 24 mm shaft spacing vs 24 mm pitch requirement; tooth solids/hubs not checked |
| Gear stage 2 nominal pitch spacing | PASS | 24 mm shaft spacing vs 24 mm pitch requirement; tooth solids/hubs not checked |
| Fork and pallet channel alignment | PASS | [-16, 16] |
| Nominal insertion clearances | PASS | 4 mm per side; 4 mm above fork; 4 mm below fork |
| Pallet floor clearance after pickup | PASS | 24.621 mm; initial empty fork-to-deck gap consumes 4 mm of stroke |
| Insertion behind pallet center | PASS | 48 mm insertion vs 32 mm center depth; assumes centered load |
| Nominal output axle stack length | PASS | 88 mm outer-to-outer nominal stack in 96 mm axle; real hubs/spacers not checked |
| Illustrative gravity torque budget | PASS | 0.0942 Nm ideal peak requirement vs 0.3600 Nm modeled output; mass/efficiency assumptions only, no capacity certification |
| Listed lift subset vs official stock | PASS | 14 listed element types checked; excludes chassis use and unresolved hardware |

## Completion blockers

The exact connection list is incomplete. The following are requirements to resolve, not hidden assumptions:

- **U01: stock chassis to both lift frames.** exact pin/axle locations and rigid cross-bracing, with wheel clearance.
- **U02: medium motor to fixed frames and input shaft.** exact housing-hole mapping, brackets, spacers and axle coupling.
- **U03: left and right fixed frames.** rigid cross-ties and exact shaft spacer stacks.
- **U04: both carriage sides to both forks.** rigid, two-point fork brackets and transverse bracing, with exact part IDs.
- **U05: touch sensor to lift and limit actuator.** mounting holes, trigger geometry and independent hard stops.
- **U06: color sensor to chassis.** bracket pieces, hole mapping and ground clearance.
- **U07: camera to chassis and controller.** assumed camera envelope, exact bracket and compatible electrical interface.
- **U08: all candidate parts to core-set stock.** combined base-plus-lift allocation including brackets, ties, spacers and cable routing.

## What has not been verified

- Full base-plus-lift inventory consumption and connector quantities.
- Real part solids, gear hubs, collision sweeps, clutch/holding behavior or illegal connections.
- Motor housing orientation, sensor/camera mounts and cable access.
- Robot center of mass, tipping margin, drive traction and lifting capacity.
- Physical operation. No assembled prototype has been observed.

The earlier V0.1 proposal and concept drawing are superseded where this review identifies gaps. Do not use either as pin-by-pin instructions.

## Reference integrity

- driving-base.pdf: SHA-256 `848d2e8506c170119bf62ce2ef9049f2de1594a23327ad30c73c11306a1c0985`
- inventory.pdf: SHA-256 `7449fb95fd65dd145d663159cce22d974c243d77e8b28f6ddfe1ef7980efe08a`
- medium-module.pdf: SHA-256 `62b5e68fbde046eccd044b2e10580d1fe34fb1419c38001944c9c2953d3ba4a6`
