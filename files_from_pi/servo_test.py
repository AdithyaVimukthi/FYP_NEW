from adafruit_servokit import ServoKit
import time
import numpy as np
import threading

x_max = 150
x_min = 80
y_max = 50
y_min = -38

LM_init_ang = 0.52359
RM_init_ang = 0 

m_time = 10/1000

ecf = 3/2
curnt_angles = [0,0]

kit = ServoKit(channels=16)

gripper = kit.servo[12]   # max 90
RM = kit.servo[13]        # shoulder - elbow link max 80
LM = kit.servo[14]        # elbow - wrist link  max 80
base = kit.servo[15]      # max 120

# LM.angle = 0
# RM.angle = 0

def R_motor_con(cur_ang, diff):
    if diff > 0 :
          for i in range (diff):
            RM.angle = cur_ang + i
            time.sleep(m_time)
    else:
         for i in range (abs(diff)):
            RM.angle = cur_ang - i
            time.sleep(m_time)

def L_motor_con(cur_ang, diff):
    if diff > 0 :
          for i in range (diff):
            LM.angle = cur_ang + i
            time.sleep(m_time)
    else:
         for i in range (abs(diff)):
            LM.angle = cur_ang - i
            time.sleep(m_time)

def process(x, y):
        l1 = 80
        l2 = 80

        q_init_deg = 30

        q_init_rad = q_init_deg * 0.0174533

        q2 = np.pi - np.arccos((l1**2 + l2**2 - x**2 - y**2)/(2*l1*l2))
        q1 = np.arctan(y/x) + np.arctan((l2*np.sin(q2))/(l1+l2*np.cos(q2)))
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

# while True:
    
#     x = int(input("Enter X Coordinate (80 -> 125 || 110 -> 125) : "))
#     y = int(input("Enter Y Coordinate (11 -> 75 || 11 -> -25): "))

#     motor_angles = process(x,y)

#     print(f"motor_angles --> {motor_angles}")
#     R_diff = int(round(motor_angles[0]*ecf)) - int(round(curnt_angles[0]*ecf))
#     L_diff = int(round(motor_angles[1]*ecf)) - int(round(curnt_angles[1]*ecf))

#     # R_motor_con(int(round(curnt_angles[0]*ecf)), R_diff)
#     # L_motor_con(int(round(curnt_angles[1]*ecf)), L_diff)

#     RC = threading.Thread(target=R_motor_con, args=(int(round(curnt_angles[0]*ecf)), R_diff))
#     LC = threading.Thread(target=L_motor_con, args=(int(round(curnt_angles[1]*ecf)), L_diff))
 
#     RC.start()
#     LC.start()
 
#     RC.join()
#     LC.join()

#     curnt_angles[0] = motor_angles[0]
#     curnt_angles[1] = motor_angles[1]


mid_ang = int(round(30 * (3/2)))
max_ang = int(round(60 * (3/2)))

for x in range(5):
    for i in range (max_ang):
        RM.angle = i 
        time.sleep(m_time)
    
    for i in range(max_ang):
        RM.angle = max_ang - i
        time.sleep(m_time)


# for x in range(5):
#     for i in range (mid_ang,max_ang):
#         RM.angle = i 
#         time.sleep(m_time)

#     for i in range(max_ang):
#         RM.angle = max_ang - i
#         time.sleep(m_time)

#     for i in range (mid_ang):
#         RM.angle = i
#         time.sleep(m_time)

RM.angle = 0