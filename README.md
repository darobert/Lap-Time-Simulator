# Lap-Time-Simulator
Python quasi-steady-state lap time simulator for vehicle performance analysis and setup optimisation.

The simulator calculates a vehicle's maximum achievable speed around a track using forward and backward integration while accounting for tyre grip, aerodynamic forces, drivetrain performance, weight transfer and combined longitudinal/lateral tyre loading.

## Features

- Forward acceleration and backward braking simulation
- Load-sensitive tyre grip model
- Friction-circle combined tyre force constraint
- Longitudinal weight transfer
- Aerodynamic downforce and drag
- Engine torque curve interpolation
- Multi-speed gearbox modelling
- Primary and final-drive reductions
- Optimal gear selection based on available tractive force
- CSV-based track curvature input
- Vehicle parameter sensitivity studies
- Final-drive and aerodynamic setup optimisation

## Simulation Method

The track is discretised into small distance steps and represented using curvature as a function of distance.

### Cornering Speed

The initial speed constraint at each point is calculated from the available lateral tyre force. Aerodynamic downforce increases the normal load on the tyres as vehicle speed increases.

### Forward Pass

A forward integration determines the maximum speed achievable under acceleration.

At each distance step, available engine torque is converted into wheel tractive force through the gearbox, primary reduction and final drive.

Acceleration is limited by:

- Available engine tractive force
- Rear-axle traction
- Combined tyre force capacity
- Aerodynamic drag

### Backward Pass

A backward integration determines the required braking points before each corner.

Braking capability accounts for tyre grip, combined lateral/longitudinal loading, weight transfer and aerodynamic drag.

The final speed profile is obtained by combining the acceleration, braking and cornering constraints.

## Vehicle Model

The vehicle model includes:

- Vehicle mass
- Wheel radius
- Tyre friction coefficient
- Load-sensitive tyre behaviour
- Front/rear weight distribution
- Centre of gravity height
- Wheelbase
- Aerodynamic lift coefficient
- Drag coefficient
- Frontal area
- Aerodynamic balance
- Drivetrain efficiency

## Drivetrain Model

Engine torque is interpolated from an RPM-dependent torque curve.

Engine speed is calculated from vehicle speed using:

`Engine RPM = Wheel RPM × Gear Ratio × Primary Ratio × Final Drive Ratio`

The simulator evaluates the available tractive force in each valid gear and selects the gear producing the greatest tractive force without exceeding the engine RPM limit.

## Outputs

The simulator produces:

- Predicted lap time
- Vehicle speed profile
- Optimal gear selection
- Engine RPM trace
- Longitudinal acceleration
- Lateral acceleration
- Aerodynamic downforce
- Aerodynamic drag

## Validation and Sensitivity Analysis

The model was evaluated using parameter sensitivity studies to verify that its behaviour was physically consistent.

### Vehicle Mass

Increasing vehicle mass produced a smooth increase in predicted lap time.

For the baseline test track:

- 200 kg: 23.97 s
- 250 kg: 25.14 s
- 300 kg: 26.13 s

This is consistent with the reduction in acceleration and increased demands on the tyres associated with increasing vehicle mass.

### Tyre Grip

Increasing the tyre friction coefficient reduced predicted lap time through increased cornering, braking and traction capability.

The resulting relationship was smooth and monotonic across the tested range.

### Aerodynamic Setup

Aerodynamic downforce and drag were varied together to investigate the trade-off between cornering performance and straight-line performance.

On a short, corner-dominated track, increasing the aerodynamic package produced continued lap-time improvement.

On a higher-speed track containing longer straights, the simulator instead identified an intermediate aerodynamic optimum as the drag penalty became increasingly significant.

This demonstrates that the preferred aerodynamic configuration is dependent on track characteristics.

### Final Drive Optimisation

The final-drive ratio was swept across a range of values.

The simulator identified an intermediate optimum, representing the trade-off between increased wheel torque from shorter gearing and reduced maximum vehicle speed.

This allows the model to be used for track-specific drivetrain setup studies.

## Example Simulation Results

### Speed and Gear Selection

The simulator generates a distance-based speed profile while selecting the gear that maximises available tractive force within the engine RPM limit.

![Speed and Gear Selection](results/Speed%20and%20Gear.png)

### Vehicle Acceleration Profile

Longitudinal and lateral acceleration are calculated throughout the lap, showing acceleration zones, braking zones and lateral loading through corners.

![Lateral and Longitudinal Acceleration](results/Lateral%20and%20Longitudinal%20Acceleration.png)


## Sensitivity Analysis and Model Verification

Parameter sweeps were performed to verify that the simulator responds consistently with expected vehicle dynamics behaviour.

### Vehicle Mass Sensitivity

Increasing vehicle mass produces a progressive increase in predicted lap time due to reduced acceleration performance and increased tyre loading.

![Mass Sensitivity](results/Mass%20Sensitivity.png)

### Tyre Grip Sensitivity

Increasing the tyre friction coefficient increases available longitudinal and lateral tyre force, reducing predicted lap time.

![Grip Sensitivity](results/Grip%20Sensitivity.png)

### Aerodynamic Package Optimisation

The aerodynamic package was varied to investigate the trade-off between increased downforce and increased aerodynamic drag. On a higher-speed track, the simulator identifies an intermediate optimum where the benefit of additional downforce is balanced against the straight-line drag penalty.

![Aero Package Optimisation](results/Aero%20Package%20Optimisation.png)

### Final Drive Optimisation

The final-drive ratio was varied to determine the optimum compromise between increased wheel torque and reduced maximum vehicle speed.

![Final Drive Optimisation](results/Final%20Drive%20Optimisation.png)

## Limitations

The simulator is intended primarily for comparative vehicle design and setup studies rather than absolute lap-time prediction.

Current simplifications include:

- Quasi-steady-state vehicle behaviour
- Simplified tyre model
- No transient suspension dynamics
- No tyre temperature or wear model
- No driver model
- No gearshift time or clutch dynamics
- Track represented using distance and curvature rather than a full 3D circuit model

Future validation against measured vehicle telemetry would be required to quantify absolute lap-time prediction accuracy.

## Technologies

- Python
- NumPy
- Matplotlib
- Object-oriented programming
- Numerical vehicle dynamics simulation
