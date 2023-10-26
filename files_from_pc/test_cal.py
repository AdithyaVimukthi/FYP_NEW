import math
import numpy as np

while True:
    x = int(input("Enter X value: "))
    y = int(input("Enter Y value: "))

    l1 = 80
    l2 = 80

    q_init_deg = 30

    q_init_rad = q_init_deg * 0.0174533

    q2 = np.pi - np.arccos((l1**2 + l2**2 - x**2 - y**2)/(2*l1*l2))
    q1 = np.arctan(y/x) + np.arctan((l2*np.sin(q2))/(l1+l2*np.cos(q2)))
    qr = (np.pi/2) - q1
    ql = np.pi - q2 - q_init_rad - qr

    qr_deg = round(qr * 57.2958)
    ql_deg = round(ql * 57.2958)

    print(f"Right Angle = {qr_deg}  || Left Angle = {ql_deg}")

