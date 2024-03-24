from scipy.spatial.transform import Rotation
import numpy as np


def rotate_point_euler(point, euler_angles):
    """
    Rotate a 3D point using Euler angles.

    Parameters:
    - point: A 3D point as a numpy array or list of shape (3,).
    - euler_angles: Euler angles as a numpy array or list of shape (3,), in the order of roll, pitch, yaw.

    Returns:
    - The rotated point as a numpy array.
    """
    # Convert Euler angles to radians
    euler_angles_rad = np.radians(euler_angles)

    # Create a Rotation object from Euler angles
    rotation = Rotation.from_euler('xyz', euler_angles_rad)

    # Apply the rotation to the point
    rotated_point = rotation.apply(point)

    return rotated_point


# Example usage
point = np.array([1, 0, 0])  # Example point
euler_angles = np.array([0, 90, 0])  # Euler angles (roll, pitch, yaw)

rotated_point = rotate_point_euler(point, euler_angles)
print("Rotated point:", rotated_point)
