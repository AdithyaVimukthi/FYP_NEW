import math
import numpy

l1 = 80
l2 = 80

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

x = int(input('Enter x: '))
y = int(input('Enter y: '))

new_theta_rad = math.acos((x**2+y**2-l1**2-l2**2)/(2*l1*l2))
new_alpha_rad = math.atan(y/x)+math.atan((l2*math.sin(new_theta_rad))/(l1+l2*math.cos(new_theta_rad)))

new_alpha_deg = round(57.2958 * new_alpha_rad)
new_theta_deg = round(57.2958 * new_theta_rad)


print(f"NEW alpha: {new_alpha_deg}")
print(f"NEW theta: {new_theta_deg}")
# X : 119.99996890598416
# Y : 69.28205025488421