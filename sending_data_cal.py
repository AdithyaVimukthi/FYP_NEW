import numpy as np
from typing import Tuple


def calculate_dis(a, b, place):
    a = np.array(a)  # First point
    b = np.array(b)  # second point

    sqrs = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    dist = np.sqrt(sqrs)

    return dist


class Data_process:
    def __init__(self):
        self.border = None
        self.y2 = None
        self.y1 = None
        self.x1 = None
        self.x2 = None

        self.distance_calibration_data = None
        self.shoulder_R_vis = None
        self.shoulder_L_vis = None
        self.mft = None
        self.wrist = None
        self.elbow = None
        self.shoulder_R = None
        self.shoulder_L = None

        self.end_eff_pos = None
        self.gripper_state = None
        self.Rotation = None

        self.width = None
        self.height = None

    def Proces(self, landmark_data, size_data):

        self.width = size_data[0]
        self.height = size_data[1]

        self.shoulder_L = [landmark_data[0][0], landmark_data[0][1]]
        self.shoulder_R = [landmark_data[1][0], landmark_data[1][1]]
        self.elbow = landmark_data[2]
        self.wrist = landmark_data[3]
        self.shoulder_L_vis = landmark_data[0][2]
        self.shoulder_R_vis = landmark_data[1][2]
        self.mft = landmark_data[4]
        self.distance_calibration_data = landmark_data[5]

        drawing_data = self.draw_data()

        R_x = round((self.x2 - self.wrist[0]) / (self.x2 - self.x1), 2)

        # R_x = self.shoulder_R[0] - self.wrist[0]
        R_y = round((self.shoulder_R[1] - self.wrist[1])/(self.height - 2 * self.border), 2)

        self.end_eff_pos = [R_x, R_y]

        if self.mft != "None" and self.wrist != "None":
            dist_mft_wrist = round(calculate_dis(self.mft, self.wrist, "dmw"))

            if dist_mft_wrist >= 70:
                self.gripper_state = 0  # gripper open
            elif dist_mft_wrist < 70:
                self.gripper_state = 1  # gripper closed
        else:
            self.gripper_state = 999

        if type(self.distance_calibration_data) != str:
            self.Rotation = self.rotation_mapping()
        else:
            self.Rotation = 999

        msg_str = f"{self.end_eff_pos[0]},{self.end_eff_pos[1]},{self.gripper_state},{self.Rotation}"
        return tuple([msg_str, drawing_data])

    def draw_data(self):
        m1 = 0
        m2 = 250
        self.border = 50

        self.x1 = int(self.shoulder_R[0] - m1 - m2)
        self.y1 = int(self.shoulder_R[1] - (self.height - 2 * self.border) / 2)
        self.x2 = int(self.shoulder_R[0] - m1)
        self.y2 = int(self.shoulder_R[1] + (self.height - 2 * self.border) / 2)

        if self.x1 < 0:
            self.x1 = 0
        if self.y1 < 0:
            self.y1 = 0
        if self.y2 > self.height:
            self.y2 = self.height

        rec_data = [self.x1, self.y1, self.x2, self.y2]

        return tuple([rec_data, self.shoulder_R, self.wrist])

    def rotation_mapping(self):
        val1 = 0

        max_rob_angle = 90
        min_rob_angle = 0

        open_max_val = 100
        open_min_val = 30
        close_max_val = 90
        close_min_val = 20

        dist_thumbcmc_pinkymcp = round(calculate_dis(self.distance_calibration_data[0], self.distance_calibration_data[1], "dtp"))

        if self.gripper_state == 0 or self.gripper_state == 999:  # gripper open
            if dist_thumbcmc_pinkymcp < 30:
                dist_thumbcmc_pinkymcp = 30
            elif dist_thumbcmc_pinkymcp > 100:
                dist_thumbcmc_pinkymcp = 100
            val1 = round((dist_thumbcmc_pinkymcp - open_min_val) / (open_max_val - open_min_val), 3)
        elif self.gripper_state == 1:
            if dist_thumbcmc_pinkymcp < 20:
                dist_thumbcmc_pinkymcp = 20
            elif dist_thumbcmc_pinkymcp > 90:
                dist_thumbcmc_pinkymcp = 90
            val1 = round((dist_thumbcmc_pinkymcp - close_min_val) / (close_max_val - close_min_val), 3)

        rotation_angle = (round((max_rob_angle - min_rob_angle) * val1)) + min_rob_angle
        print(f"Rotation_angle = {rotation_angle} ----> {dist_thumbcmc_pinkymcp}")

        return rotation_angle