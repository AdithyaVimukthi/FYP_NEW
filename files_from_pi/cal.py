import math
import numpy as np

class post_process():
    def __init__(self):
        self.xt_max = 140
        self.xt_min = 80

        self.xb_max = 140
        self.xb_min = 120

        self.yt_max = 75
        self.yt_min = 0

        self.yb_max = 0
        self.yb_min = -50

        self.l1 = 80
        self.l2 = 80

        self.LM_init_ang = 0.52359
        self.RM_init_ang = 0 

    def process(self,data):

        q_init_deg = 30
        q_init_rad = q_init_deg * 0.0174533

        if data[0] < 0:
            x = ((self.xb_max - self.xb_min) * abs(data[0])) + self.xb_min
        else:
            x = ((self.xt_max - self.xt_min) * data[0]) + self.xt_min
        

        if data[1] < 0: 
            y = (self.yb_max - self.yb_min) * abs(data[1]) + self.yb_max
        else:
            y = (self.yt_max - self.yt_min) * data[1] + self.yt_min

        q2 = np.pi - np.arccos((self.l1**2 + self.l2**2 - x**2 - y**2)/(2*self.l1*self.l2))
        q1 = np.arctan(y/x) + np.arctan((self.l2*np.sin(q2))/(self.l1+self.l2*np.cos(q2)))
        qr = (np.pi/2) - q1
        ql = np.pi - q2 - q_init_rad - qr

        RM_angle = round(qr * 57.2958)
        LM_angle = round(ql * 57.2958)

        if RM_angle < 0:
            RM_angle = 0
        elif RM_angle > 90:
            RM_angle = 90

        if LM_angle < 0:
            LM_angle = 0
        elif LM_angle > 90:
            LM_angle = 90

        return tuple([RM_angle, LM_angle])

