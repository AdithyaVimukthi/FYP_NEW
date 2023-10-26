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
        self.rot_trg_sig = None
        self.dist_mft_wrist = None
        self.gap = None
        self.m1 = None
        self.h_bottom = None
        self.h_top = None
        self.w = None
        self.border = None
        self.y2 = None
        self.y1 = None
        self.x1 = None
        self.x2 = None
        self.prev_dis_t2p = 0
        self.grip_prev_st = 0
        self.prev_val = [0, 0]

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
        self.Rotation_trig_signal = None

        self.width = None
        self.height = None

    def Proces(self, landmark_data, size_data):

        self.width = size_data[0]
        self.height = size_data[1]

        # self.shoulder_L = [landmark_data[0][0], landmark_data[0][1]]
        self.shoulder_R = [landmark_data[1][0], landmark_data[1][1]]
        # self.elbow = landmark_data[2]
        self.wrist = landmark_data[3]
        # self.shoulder_L_vis = landmark_data[0][2]
        # self.shoulder_R_vis = landmark_data[1][2]
        self.mft = landmark_data[4]
        self.distance_calibration_data = landmark_data[5]

        drawing_data = self.draw_data()

        if self.wrist[0] > self.shoulder_R[0]:
            self.wrist[0] = self.shoulder_R[0]
        elif self.wrist[0] < self.shoulder_R[0] - self.w:
            self.wrist[0] = self.shoulder_R[0] - self.w

        if self.wrist[1] > self.shoulder_R[1] + self.h_bottom:
            self.wrist[1] = self.shoulder_R[1] + self.h_bottom
        elif self.wrist[1] < self.shoulder_R[1] - self.h_top:
            self.wrist[1] = self.shoulder_R[1] - self.h_top

        delta_x = self.shoulder_R[0] - self.wrist[0]
        delta_y = self.shoulder_R[1] - self.wrist[1]

        R_x = round((abs(delta_x)) / self.w, 4)

        if delta_y > 0:
            R_y = round((abs(delta_y)) / self.h_top, 4)
        else:
            R_y = round(-1 * ((abs(delta_y)) / self.h_bottom), 4)
            R_x = R_x * (-1)

        self.end_eff_pos = [R_x, R_y]

        if self.mft != -999 and self.wrist != -999:
            self.dist_mft_wrist = round(calculate_dis(self.mft, self.wrist, "dmw"))

            if self.dist_mft_wrist >= 70:
                self.gripper_state = 0  # gripper open
            elif self.dist_mft_wrist < 70:
                self.gripper_state = 1  # gripper closed
        else:
            self.gripper_state = self.grip_prev_st

        if self.distance_calibration_data != -999:
            self.Rotation_trig_signal = self.rotation_mapping
        else:
            self.Rotation_trig_signal = 0

        # print(f"[X = {R_x} , Y = {R_y}] , [Grip_st = {self.gripper_state}]")

        msg_str = f"T{self.end_eff_pos[0]},{self.end_eff_pos[1]},{self.gripper_state},{self.Rotation_trig_signal}"

        # previous state and position update
        self.grip_prev_st = self.gripper_state
        self.prev_val = self.end_eff_pos

        return tuple([msg_str, drawing_data])

    def draw_data(self):
        self.h_top = 192
        self.h_bottom = 180
        self.w = 225
        self.m1 = 0  # 80
        # self.gap = 80

        # self.border = 50

        self.x1 = int(self.shoulder_R[0] - self.m1 - self.w)
        self.y1 = int(self.shoulder_R[1] - self.h_top)
        self.x2 = int(self.shoulder_R[0] - self.m1)
        self.y2 = int(self.shoulder_R[1] + self.h_bottom)

        if self.x1 < 0:
            self.x1 = 0
        if self.y1 < 0:
            self.y1 = 0
        if self.y2 > self.height:
            self.y2 = self.height

        rec_data = [self.x1, self.y1, self.x2, self.y2]

        return tuple([rec_data, self.shoulder_R, self.wrist])

    @property
    def rotation_mapping(self):
        val1 = 0

        max_rob_angle = 90
        min_rob_angle = 0

        open_max_val = 100
        open_min_val = 30
        close_max_val = 90
        close_min_val = 20

        dist_thumbcmc_pinkymcp = round(
            calculate_dis(self.distance_calibration_data[0], self.distance_calibration_data[1], "dtp"))
        # print(f"dist_thumbcmc_pinkymcp = {dist_thumbcmc_pinkymcp}")

        if dist_thumbcmc_pinkymcp > 100 and self.dist_mft_wrist < 60:
            if dist_thumbcmc_pinkymcp - self.prev_dis_t2p > 40:
                self.rot_trg_sig = 1
            else:
                self.rot_trg_sig = 0
        else:
            self.rot_trg_sig = 0

        print(f"Signal --> {self.rot_trg_sig}")
        # print(f"Signal --> {self.rot_trg_sig} || curt_dis = {dist_thumbcmc_pinkymcp}"
        #       f" || prev_dis = {self.prev_dis_t2p} || dist_m2w = {self.dist_mft_wrist}")
        self.prev_dis_t2p = dist_thumbcmc_pinkymcp

        # if self.gripper_state == 0 or self.gripper_state == 999:  # gripper open
        #     if dist_thumbcmc_pinkymcp < 30:
        #         dist_thumbcmc_pinkymcp = 30
        #     elif dist_thumbcmc_pinkymcp > 100:
        #         dist_thumbcmc_pinkymcp = 100
        #     val1 = round((dist_thumbcmc_pinkymcp - open_min_val) / (open_max_val - open_min_val), 3)
        # elif self.gripper_state == 1:
        #     if dist_thumbcmc_pinkymcp < 20:
        #         dist_thumbcmc_pinkymcp = 20
        #     elif dist_thumbcmc_pinkymcp > 90:
        #         dist_thumbcmc_pinkymcp = 90
        #     val1 = round((dist_thumbcmc_pinkymcp - close_min_val) / (close_max_val - close_min_val), 3)
        #
        # rotation_angle = (round((max_rob_angle - min_rob_angle) * val1)) + min_rob_angle
        # # print(f"Rotation_angle = {rotation_angle} ----> {dist_thumbcmc_pinkymcp}")

        return self.rot_trg_sig
