import numpy as np
from scipy.spatial.transform import Rotation as R

# Define the initial and final coordinate systems as rotation matrices
r_0 = np.array([[-0.02659679, -0.00281247,  0.99964229],
                [ 0.76308514, -0.64603356,  0.01848528],
                [ 0.64575048,  0.76330382,  0.01932857]])

r_1 = np.array([[ 0.05114056, -0.03815443,  0.99796237],
                [-0.30594799,  0.95062582,  0.05202294],
                [-0.95067369, -0.30798506,  0.03694226]])

r_0  =          [[1., 0., 0.],
              [0., 1., 0.],
              [0., 0., 1.]]

r_1=  [[0.98 ,-0.17,  -0.00],
        [0.12, 0.7 , -0.71],
        [0.12, 0.7 , 0.71]]

# Calculate the relative rotation matrix from t0 to t1
rot_mat_rel = np.matmul(np.transpose(r_0), r_1)

# Define the point to be transformed
point = np.array([0, 0, 100]) # Example point

# Apply the rotation to the point
rotated_point = np.dot(rot_mat_rel, point)

print("Original Point:", point)
print("Rotated Point:", rotated_point)
