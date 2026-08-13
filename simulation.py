import numpy as np

class Simulation:

    def __init__(self, track, vehicle, engine, gearbox):

        self.track = track
        self.vehicle = vehicle
        self.engine = engine
        self.gearbox = gearbox

    def calculate_cornering_speed(self):

        curvature = np.abs(self.track.curvature)

        # initialise to high max speed for straights
        cornering_speed = np.full(len(curvature),100.00)

        for i in range(len(curvature)):

            if curvature[i] > 0:

                numerator = self.vehicle.mu * self.vehicle.mass * self.vehicle.g

                denominator = self.vehicle.mass * curvature[i] - 0.5 * self.vehicle.mu * self.vehicle.air_density * self.vehicle.lift_coefficient * self.vehicle.frontal_area

                if denominator > 0:

                    cornering_speed[i] = np.sqrt(numerator / denominator)

        return cornering_speed


    def forward_pass(self,speed_limit):

        speed = np.zeros(len(speed_limit))

        speed[0] = 0.0

        for i in range(len(speed_limit) - 1):

            distance_step = self.track.distance[i + 1] - self.track.distance[i]

            best_gear, tractive_force, engine_rpm = self.gearbox.best_gear_and_force(vehicle_speed = speed[i],wheel_radius = self.vehicle.wheel_radius, engine = self.engine, drivetrain_efficiency = self.vehicle.drivetrain_efficiency)

            estimated_acceleration = tractive_force / self.vehicle.mass

            rear_traction_limit = self.vehicle.max_rear_tractive_force(speed = speed[i],acceleration = estimated_acceleration)

            combined_tire_limit = self.vehicle.max_longitudinal_force(speed = speed[i], curvature = self.track.curvature[i])

            actual_force = min(tractive_force,rear_traction_limit,combined_tire_limit)

            drag_force = self.vehicle.drag_force(speed[i])

            net_force = actual_force - drag_force

            acceleration = net_force / self.vehicle.mass

            possible_next_speed = np.sqrt(speed[i]**2 + 2*acceleration*distance_step)

            speed[i + 1] = min(possible_next_speed,speed_limit[i + 1])

        return speed

    def backward_pass(self, speed_profile):

        speed = speed_profile.copy()

        for i in range (len(speed) - 2, -1, -1):
            distance_step = self.track.distance[i+1] - self.track.distance[i]

            current_speed = speed[i+1]

            estimated_deceleration = 10.0

            max_tire_braking_force = self.vehicle.max_braking_force(speed = current_speed,deceleration = estimated_deceleration)

            drag_force = self.vehicle.drag_force(current_speed)

            total_braking_force = max_tire_braking_force + drag_force

            braking_deceleration = self.calculate_braking_deceleration(speed = current_speed,curvature = self.track.curvature[i+1])

            maximum_previous_speed = np.sqrt(speed[i+1] ** 2 + 2*braking_deceleration * distance_step)

            speed[i] = min(speed[i], maximum_previous_speed)

        return speed

    def calculate_lap_time(self,speed):

        total_time = 0.0

        for i in range(len(speed) -1):

            dist_step = self.track.distance[i+1] - self.track.distance[i]
            avg_speed = (speed[i] + speed[i+1]) / 2

            if avg_speed > 0:
                time_step = dist_step / avg_speed

                total_time = total_time + time_step

        return total_time

    def calculate_braking_deceleration(self,speed,curvature):
        # initial est
        deceleration = 10

        for _ in range (10):

            axle_braking_force = self.vehicle.max_braking_force(speed = speed, deceleration = deceleration)

            combined_tire_limit = self.vehicle.max_longitudinal_force(speed = speed,curvature = curvature)

            tire_braking_force = min(axle_braking_force,combined_tire_limit)

            drag_force = self.vehicle.drag_force(speed)

            total_braking_force = tire_braking_force + drag_force

            new_deceleration = total_braking_force / self.vehicle.mass

            if abs(new_deceleration - deceleration) < 0.001:
                break

            deceleration = new_deceleration

        return new_deceleration