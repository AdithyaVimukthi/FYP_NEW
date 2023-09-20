import numpy as np
from numpy import *

l1 = 173
l2 = 173
l3 = 173

while True:
    s = int(input('Enter Shoulder angle: '))
    if s > 360:
        break
    e = int(input('Enter elbow angle: '))
    if e > 360:
        break

    y = round(l2 * np.cos(e - s) - l1 * np.cos(s), 2)
    x = round(l2 * np.sin(e - s) + l1 * np.sin(s), 2)

    # x = round(l2 * np.cos(s - e) - l1 * np.cos(s), 2)
    # y = round(l2 * np.sin(s - e) - l1 * np.sin(s), 2)

    print(f'X - {x} || Y - {y}')

    q1 = arccos((x**2 + y**2 - 2 * (l3 ** 2))/(2*(l3**2)))
    beta = arctan(y/x) + arctan((l3 * sin(q1))/(l3 + l3 * cos(q1)))
    alpha = q1 - beta

    print(f'Q1 - {round(degrees(q1),2)} || Beta - {round(degrees(beta),2)}')