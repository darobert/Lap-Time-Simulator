import numpy as np

class Engine:

    def __init__(self, rpm_values, torque_values, idle_rpm, max_rpm):

        self.max_rpm = max_rpm
        self.idle_rpm = idle_rpm
        self.rpm_values = np.array(rpm_values, dtype=float)
        self.torque_values = np.array(torque_values, dtype=float)


    def torque_at_rpm(self,rpm):
        rpm = np.clip(rpm,self.idle_rpm,self.max_rpm)

        torque = np.interp(rpm, self.rpm_values,self.torque_values)

        return torque