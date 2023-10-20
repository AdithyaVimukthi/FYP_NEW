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
        self.base.angle = 50

        self.curt_data = [0,0]

        self.rot_st = False
        self.curt_base_ang = 60

        self.cur_grip_st = None
        self.grip_init_ang = 0

        self.curt_LM_ang = 0
        self.curt_RM_ang = 0
        

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

    def base_rotation(self,x):

        max_ang = 100

        base_ang = int(round((max_ang * abs(x))))

        if base_ang < 0:
            base_ang = 0 
        elif base_ang > max_ang:
            base_ang = max_ang

        diff =  int(round(base_ang * self.ecf)) - int(round(self.curt_base_ang * self.ecf))
        
        print(f"Diff - {diff} || curt_base_ang = {self.curt_base_ang}({int(round(self.curt_base_ang * self.ecf))}) ||base_ang = {base_ang} ({int(round(base_ang * self.ecf))})")

        if diff > 0 :
            for i in range (diff):
                self.base.angle = int(round(self.curt_base_ang * self.ecf)) + i
                time.sleep(self.m_time)
        else:
            for i in range (abs(diff)):
                self.base.angle = int(round(self.curt_base_ang * self.ecf)) - i
                time.sleep(self.m_time)
        
        self.curt_base_ang = base_ang

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

        if self.curt_base_ang > 50:
            diff = self.curt_base_ang - 50
            for i in range (diff):
                self.base.angle = self.curt_base_ang - i+1
                time.sleep(10/1000)
            self.base.angle = 50
            self.curt_base_ang = 50
        elif self.curt_base_ang < 0:
            diff = 50 - self.curt_base_ang 
            for i in range (diff):
                self.base.angle = self.curt_base_ang + i
                time.sleep(10/1000)
            self.base.angle = 50
            self.curt_base_ang = 50

    def controll(self,data_string):
        data = data_string.split('T')[1]
        data_array = data.split(',')

        X_n_Y = [float(data_array[0]),float(data_array[1])]
        gripper_st = int(data_array[2])
        rot_trig_sig = int(data_array[3])

        if rot_trig_sig == 1:
            self.rot_st = not self.rot_st
        # print(self.rot_st)
        
        if self.rot_st == False:
            if gripper_st != self.cur_grip_st :
                if gripper_st == 0:
                    self.gripper.angle = 100 * self.ecf
                    self.cur_grip_st = 0
                elif gripper_st == 1:
                    self.gripper.angle = 0 * self.ecf
                    self.cur_grip_st =  1
            
            if gripper_st == 0:
                self.grip_msg = "Open"
            elif gripper_st == 1: 
                self.grip_msg = "Close"
            else:
                self.grip_msg = "Close"
            
            self.M_angle_data = self.data_process.process(X_n_Y)

            R_diff = int(round(self.M_angle_data[0]*self.ecf)) - int(round(self.curt_data[0]*self.ecf))
            L_diff = int(round(self.M_angle_data[1]*self.ecf)) - int(round(self.curt_data[1]*self.ecf))

            RC = threading.Thread(target=self.R_motor_con, args=(int(round(self.curt_data[0]*self.ecf)), R_diff))
            LC = threading.Thread(target=self.L_motor_con, args=(int(round(self.curt_data[1]*self.ecf)), L_diff))
        
            RC.start()
            LC.start()
        
            RC.join()
            LC.join()

            self.curt_data[0] = self.M_angle_data[0]
            self.curt_data[1] = self.M_angle_data[1]
        else:
            self.base_rotation(X_n_Y[0])

        return [self.grip_msg, str(self.M_angle_data[0]), str(self.M_angle_data[1])]
    