import numpy as np

class Vehicle:

    def __init__(self):
        self.mass = 250 #k g
        self.mu = 1.4 # no unit
        self.g = 9.81 # m / s^2
        self.wheel_radius = 0.23
        self.drivetrain_efficiency = 0.90
        self.lift_coefficient = 1.5

        #aero
        self.air_density = 1.225 # kg / m^3
        self.drag_coefficient = 0.9
        self.frontal_area = 1.0 # m^2

        self.wheelbase = 1.6 # m
        self.cg_height = 0.3 # m

        self.front_weight_distrubution = 0.45
        self.front_aero_distribution = 0.45

        self.tire_load_sensitivity = 0.10
        self.reference_tyre_load = 613.125  # N


    def drag_force(self, speed):

        drag = 0.5 * self.air_density * self.drag_coefficient * self.frontal_area * speed ** 2

        return drag

    def downforce(self, speed):

        downforce = 0.5 * self.air_density * self.lift_coefficient * self.frontal_area * speed ** 2

        return downforce

    def max_longitudinal_force(self,speed,curvature):

        normal_force = self.mass * self.g + self.downforce(speed)

        total_grip = self.mu * normal_force

        lateral_force = self.mass * speed**2 * abs(curvature)

        longitudinal_force_squared = total_grip ** 2 - lateral_force ** 2

        longitudinal_force_squared = max(longitudinal_force_squared,0.0)

        max_longitudinal_force = np.sqrt(longitudinal_force_squared)

        return max_longitudinal_force

    def axle_normal_loads (self, speed, acceleration):

        weight = self.mass * self.g

        # static axle loads
        front_static = self.front_weight_distrubution * weight
        rear_static = (1 - self.front_weight_distrubution) * weight

        total_downforce = self.downforce(speed)
        front_downforce = self.front_aero_distribution * total_downforce
        rear_downforce = (1 - self.front_aero_distribution) * total_downforce

        weight_transfer = self.mass * acceleration * self.cg_height /self.wheelbase

        front_normal = front_static + front_downforce - weight_transfer
        rear_normal = rear_static + rear_downforce + weight_transfer

        return front_normal, rear_normal

    def max_rear_tractive_force (self,speed,acceleration):

        front_normal , rear_normal = self.axle_normal_loads(speed, acceleration)

        rear_tire_load = rear_normal / 2

        rear_tire_grip = self.tire_grip(rear_tire_load)

        max_rear_force = 2 * rear_tire_grip

        return max_rear_force

    def tire_grip(self,normal_load):

        reference_load = self.reference_tyre_load

        if normal_load <= 0:
            return 0.0

        effective_mu = self.mu * (normal_load / reference_load) ** (-self.tire_load_sensitivity)

        max_force = effective_mu * normal_load

        return max_force

    def max_braking_force (self, speed, deceleration):

        front_normal , rear_normal = self.axle_normal_loads(speed = speed,acceleration= -deceleration)

        front_tire_load = front_normal / 2
        rear_tire_load = rear_normal / 2

        front_axle_grip = 2*self.tire_grip(front_tire_load)
        rear_axle_grip = 2*self.tire_grip(rear_tire_load)

        total_braking_force = front_axle_grip + rear_axle_grip

        return total_braking_force

        