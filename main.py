import numpy as np
import matplotlib.pyplot as plt

from vehicle import Vehicle
from track import Track
from simulation import Simulation
from engine import Engine
from gearbox import Gearbox

def run_simulation (car,track,engine,gearbox):

    simulation = Simulation(track,car,engine,gearbox)

    cornering_speed = simulation.calculate_cornering_speed()
    forward_speed = simulation.forward_pass(cornering_speed)
    final_speed = simulation.backward_pass(forward_speed)

    lap_time = simulation.calculate_lap_time(final_speed)

    return lap_time

gearbox = Gearbox(

    gear_ratios=[
        2.8,
        2.1,
        1.7,
        1.4,
        1.2,
        1.0
    ],

    final_drive=3.5,
    primary_ratio = 2.11

)

engine = Engine(
    rpm_values=[2000, 4000, 6000, 8000, 10000, 12000, 14000],
    torque_values=[30, 40, 50, 58, 62, 60, 52],
    idle_rpm=2000,
    max_rpm=14000
)

car = Vehicle()

track = Track.from_csv("sample_track.csv")

lap_time = run_simulation(car,track,engine,gearbox)

print(f"Lap time: {lap_time:.2f} seconds")