from scipy.spatial.transform import Rotation as R
import numpy as np

# Define a quaternion for a 90-degree rotation about the z-axis
quaternion = [0, 0, np.sin(np.pi/4), np.cos(np.pi/4)]

# Create a rotation object from the quaternion
rotation = R.from_quat(quaternion)

# Define a point to rotate
point = np.array([33, 22, 15])

# Apply the rotation to the point
rotated_point = rotation.apply(point)

print(rotated_point)
