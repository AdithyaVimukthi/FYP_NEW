import math
import numpy as np

# alpha_deg = int(input('Enter alpha angle: '))
# theta_deg = int(input('Enter theta angle: '))
#
# alpha_rad = 0.0174533 * alpha_deg
# theta_rad = 0.0174533 * theta_deg
#
# x = round(l1 * math.cos(alpha_rad) + l2 * math.cos(theta_rad - alpha_rad), 2)
# y = round(l1 * math.sin(alpha_rad) - l2 * math.sin(theta_rad - alpha_rad), 2)
#
# print(f"X : {x}")
# print(f"Y : {y}")

class post_process():
    def __init__(self):
        self.x_max = 150
        self.x_min = 80
        self.y_max = 50
        self.y_min = -38

        self.l1 = 80
        self.l2 = 80

        self.LM_init_ang = 0.52359
        self.RM_init_ang = 0 

    def process(self,data):

        x = ((self.x_max - self.x_min) * data[0]) + self.x_min

        if data[1] < 0: 
            y = self.y_min * data[1] * (-1)
        else:
            y = self.y_max * data[1]
        
        theta_rad = math.acos((x**2+y**2-self.l1**2-self.l2**2)/(2*self.l1*self.l2))
        alpha_rad = math.atan(y/x)+math.atan((self.l2*math.sin(theta_rad))/(self.l1+self.l2*math.cos(theta_rad)))

        # alpha_deg = round(57.2958 * alpha_rad)
        # theta_deg = round(57.2958 * theta_rad)

        RM_angle = round(((np.pi)/2 - alpha_rad - self.RM_init_ang) * 57.2958)
        LM_angle = round(((np.pi)/3 + alpha_rad - theta_rad) * 57.2958)

        return tuple([RM_angle, LM_angle])

