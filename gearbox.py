import numpy as np

class Gearbox:

    def __init__(self, gear_ratios, final_drive,primary_ratio):

        self.gear_ratios = gear_ratios
        self.final_drive = final_drive
        self.primary_ratio = primary_ratio

    def wheel_rpm(self, vehicle_speed, wheel_radius):

        wheel_angular_velocity = vehicle_speed / wheel_radius
        wheel_rpm = wheel_angular_velocity * 60 / (2 * np.pi)

        return wheel_rpm

    def engine_rpm(self, vehicle_speed, wheel_radius, gear_index):

        wheel_rpm = self.wheel_rpm(vehicle_speed,wheel_radius)

        gear_ratio = self.gear_ratios[gear_index]

        engine_rpm = gear_ratio * wheel_rpm * self.final_drive * self.primary_ratio

        return engine_rpm

    def wheel_torque(self, engine_torque, gear_index, drivetrain_efficiency):

        gear_ratio = self.gear_ratios[gear_index]

        wheel_torque = gear_ratio * engine_torque * self.final_drive * drivetrain_efficiency * self.primary_ratio

        return wheel_torque

    def tractive_force(self,engine_torque,gear_index, wheel_radius ,drivetrain_efficiency):

        wheel_torque = self.wheel_torque(engine_torque,gear_index,drivetrain_efficiency )

        force = wheel_torque / wheel_radius

        return force

    def best_gear_and_force ( self, vehicle_speed, wheel_radius,engine,drivetrain_efficiency):
        best_force = 0.0
        best_gear_index = 0.0
        best_engine_rpm = 0.0

        for gear_index in range(len(self.gear_ratios)):
            engine_rpm = self.engine_rpm(vehicle_speed,wheel_radius,gear_index)

            if engine_rpm > engine.max_rpm:
                continue

            engine_torque = engine.torque_at_rpm(engine_rpm)

            force = self.tractive_force(engine_torque,gear_index,wheel_radius,drivetrain_efficiency)

            if force > best_force:
                best_force = force
                best_gear_index = gear_index
                best_engine_rpm = engine_rpm

        return best_gear_index, best_force, best_engine_rpm


