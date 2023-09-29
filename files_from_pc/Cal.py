import numpy as np
import matplotlib.pyplot as plt

# Define the parameters of the robot arm
link1_length = 80  # Length of the first link
link2_length = 80  # Length of the second link

# Define the range of joint angles (theta1 and theta2)
theta1_range = np.linspace(0, np.pi/2, 100)  # Range of theta1 values
theta2_range = np.linspace(0, (2*np.pi)/3, 100)  # Range of theta2 values

# Create empty lists to store the end-effector positions
end_effector_x = []
end_effector_y = []

# Calculate the end-effector position for each combination of joint angles
for theta1 in theta1_range:
    for theta2 in theta2_range:
        # Forward kinematics to calculate the end-effector position
        x = link1_length * np.cos(theta1) + link2_length * np.cos(theta2 - theta1)
        y = link1_length * np.sin(theta1) - link2_length * np.sin(theta2 - theta1)

        end_effector_x.append(x)
        end_effector_y.append(y)

# Plot the task space
plt.figure(figsize=(8, 6))

plt.plot([80, 80, 80], [-38, 0, 50], label='LL', color='red', linewidth=2)
plt.plot([80, 100, 120, 150], [-38, -38, -38, -38], label='LB', color='red', linewidth=2)
plt.plot([150, 150, 150], [-38, 0, 50], label='LR', color='red', linewidth=2)
plt.plot([80, 100, 120, 150], [50, 50, 50, 50], label='LT', color='red', linewidth=2)
plt.scatter(end_effector_x, end_effector_y, s=2, c='b', marker='.')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.title('Task Space of 2-DOF Robot Arm')
plt.grid(True)
plt.axis('equal')  # Set equal scaling for x and y axes
plt.show()
