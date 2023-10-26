import numpy as np
import matplotlib.pyplot as plt

# Define the parameters of the robot arm
link1_length = 80  # Length of the first link
link2_length = 80  # Length of the second link
q_init_rad = 30 * 0.0174533

# Define the range of joint angles (theta1 and theta2)
theta1_range = np.linspace(0, np.pi / 2, 100)  # Range of theta1 values  Qr
theta2_range = np.linspace(0, np.pi / 2, 100)  # Range of theta2 values  Ql

# Create empty lists to store the end-effector positions
end_effector_x = []
end_effector_y = []

# Calculate the end-effector position for each combination of joint angles
for theta1 in theta1_range:
    for theta2 in theta2_range:
        # Forward kinematics to calculate the end-effector position
        x = link1_length * np.sin(theta1) + link2_length * np.sin(theta2 + q_init_rad)
        y = link1_length * np.cos(theta1) - link2_length * np.cos(theta2 + q_init_rad)

        end_effector_x.append(x)
        end_effector_y.append(y)

# Plot the task space
plt.figure(figsize=(8, 6))

plt.plot([80, 80, 80, 80], [11, 25, 50, 75], label='LL', color='red', linewidth=2)
plt.plot([80, 100, 120, 125], [11, 11, 11, 11], label='LB', color='red', linewidth=2)
plt.plot([125, 125, 125, 125], [11, 25, 50, 75], label='LR', color='red', linewidth=2)
plt.plot([80, 100, 120, 125], [75, 75, 75, 75], label='LT', color='red', linewidth=2)

plt.plot([110, 110, 110], [11, -10, -25], label='LL', color='green', linewidth=2)  # L
plt.plot([110, 115, 125], [11, 11, 11], label='LB', color='green', linewidth=2)  # B
plt.plot([125, 125, 125], [11, -10, -25], label='LR', color='green', linewidth=2)  # R
plt.plot([110, 115, 125], [-25, -25, -25], label='LT', color='green', linewidth=2)  # T

plt.scatter(end_effector_x, end_effector_y, s=2, c='b', marker='.')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.title('Task Space of 2-DOF Robot Arm')
plt.grid(True)
plt.axis('equal')  # Set equal scaling for x and y axes
plt.show()
