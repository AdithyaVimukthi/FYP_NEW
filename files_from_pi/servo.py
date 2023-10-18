from adafruit_servokit import ServoKit
import time
from cal import post_process
import threading

class servo_controller():
    def __init__(self):
        self.kit = ServoKit(channels=16)
        self.gripper = self.kit.servo[12]   # max 120
        self.RM = self.kit.servo[13]        # shoulder - elbow link max 150
        self.LM = self.kit.servo[14]        # elbow - wrist link  max 80
        self.base = self.kit.servo[15]      # max 90

        self.ecf = 3/2
        self.m_time = 10/1000

        #setting servos to init positions
        self.gripper.angle = 0
        self.RM.angle = 0
        self.LM.angle = 0
        self.base.angle = 60

        self.curt_data = [0,0]

        self.cur_grip_st = None
        self.grip_init_ang = 0
        self.curt_LM_ang = 0
        self.curt_RM_ang = 0
        self.curt_base_ang = 60

        self.data_process = post_process()
    
    def R_motor_con(self, cur_ang, diff):
        if diff > 0 :
            for i in range (diff):
                self.RM.angle = cur_ang + i
                time.sleep(self.m_time)
        else:
            for i in range (abs(diff)):
                self.RM.angle = cur_ang - i
                time.sleep(self.m_time)

    def L_motor_con(self, cur_ang, diff):
        if diff > 0 :
            for i in range (diff):
                self.LM.angle = cur_ang + i
                time.sleep(self.m_time)
        else:
            for i in range (abs(diff)):
                self.LM.angle = cur_ang - i
                time.sleep(self.m_time)

    def to_init_pos(self):
        #setting servos to init positions
        self.gripper.angle = 0
        self.cur_grip_st = 0 

        if self.curt_data[1] != 0:
            for i in range (self.curt_data[1]):
                self.LM.angle = self.curt_data[1] - i+1
                time.sleep(10/1000)
            self.LM.angle = 0
            self.curt_data[1] = 0
        
        if self.curt_data[0] != 0:
            for i in range (self.curt_data[0]):
                self.RM.angle = self.curt_data[0] - i+1
                time.sleep(10/1000)
            self.RM.angle = 0
            self.curt_data[0] = 0

        if self.curt_base_ang > 60:
            diff = self.curt_base_ang - 60
            for i in range (diff):
                self.base.angle = self.curt_base_ang - i+1
                time.sleep(10/1000)
            self.base.angle = 60
            self.curt_base_ang = 60
        elif self.curt_base_ang < 0:
            diff = 60 - self.curt_base_ang 
            for i in range (diff):
                self.base.angle = self.curt_base_ang + i
                time.sleep(10/1000)
            self.base.angle = 60
            self.curt_base_ang = 60

    def controll(self,data_string):
        data = data_string.split('T')[1]
        data_array = data.split(',')

        end_effector_pos = [float(data_array[0]),float(data_array[1])]
        gripper_st = int(data_array[2])
        # rot_len = int(data_array[3])

        if gripper_st != self.cur_grip_st :
            if gripper_st == 0:
                self.gripper.angle = 120 * self.ecf
                self.cur_grip_st = 0
            elif gripper_st == 1:
                self.gripper.angle = 0 * self.ecf
                self.cur_grip_st =  1
        
        if gripper_st == 0:
            grip_msg = "Open"
        elif gripper_st == 1: 
            grip_msg = "Close"
        else:
            grip_msg = "Close"
        
        self.M_angle_data = self.data_process.process(end_effector_pos)

        # R_diff = self.M_angle_data[0] - self.curt_data[0]
        # L_diff = self.M_angle_data[1] - self.curt_data[1]

        R_diff = int(round(self.M_angle_data[0]*self.ecf)) - int(round(self.curt_data[0]*self.ecf))
        L_diff = int(round(self.M_angle_data[1]*self.ecf)) - int(round(self.curt_data[1]*self.ecf))

        RC = threading.Thread(target=self.R_motor_con, args=(int(round(self.curt_data[0]*self.ecf)), R_diff))
        LC = threading.Thread(target=self.L_motor_con, args=(int(round(self.curt_data[1]*self.ecf)), L_diff))
    
        RC.start()
        LC.start()
    
        RC.join()
        LC.join()

        # self.RM.angle = self.M_angle_data[0] * self.error_correction_factor
        self.curt_data[0] = self.M_angle_data[0]
        # self.LM.angle = self.M_angle_data[1] * self.error_correction_factor
        self.curt_data[1] = self.M_angle_data[1]

        # print(f"RM_angle = {self.M_angle_data[0]} || LM_angle = {self.M_angle_data[1]}")
        
        # R_ang_diff = abs(self.curt_RM_ang - self.M_angle_data[0])
        # L_ang_diff = abs(self.curt_LM_ang - self.M_angle_data[1])

        # # Right Motor (shoulder - elbow)
        # if self.curt_RM_ang < self.M_angle_data[0]:
        #     if R_ang_diff > 5:
        #         for i in range (R_ang_diff):
        #             self.RM.angle = (self.curt_RM_ang + i) * self.error_correction_factor
        #             time.sleep(10/1000)
        #         self.curt_RM_ang = self.M_angle_data[0]
        # elif self.curt_RM_ang > self.M_angle_data[0]:
        #     if R_ang_diff > 5:
        #         for i in range (R_ang_diff):
        #             self.RM.angle = (self.curt_RM_ang - i) * self.error_correction_factor
        #             time.sleep(10/1000)
        #         self.curt_RM_ang = self.M_angle_data[0]

        # #Left Motor (elbow - wrist)
        # if self.curt_LM_ang < self.M_angle_data[1]:
        #     if L_ang_diff > 5:
        #         for i in range (L_ang_diff):
        #             self.LM.angle = (self.curt_LM_ang + i) * self.error_correction_factor
        #             time.sleep(10/1000)
        #         self.curt_LM_ang = self.M_angle_data[1]

        # elif self.curt_LM_ang > self.M_angle_data[1]:
        #     if L_ang_diff > 5:
        #         for i in range (L_ang_diff):
        #             self.LM.angle = (self.curt_LM_ang - i) * self.error_correction_factor
        #             time.sleep(10/1000)
        #         self.curt_LM_ang = self.M_angle_data[1]

        return [grip_msg, str(self.M_angle_data[0]), str(self.M_angle_data[1])]
        
####################################



# kit = ServoKit(channels=16)

# motor = kit.servo[14]

# ang = 90

# max_ang = int(round((ang/2)*3))

# # for x in range(5):
# # for i in range (max_ang):
# #     motor.angle = i
# #     time.sleep(15/1000)

# for i in range(max_ang):
#     motor.angle = max_ang - i 
#     time.sleep(15/1000)

# # motor.angle = (max_ang/2)*3

# # motor.angle = 0