import numpy as np

def euler_321_matrix(psi, theta, phi):
    """
    Calculates the 3-2-1 Euler angle rotation matrix.

    Args:
        psi: Yaw angle (rotation around Z-axis) in radians.
        theta: Pitch angle (rotation around Y-axis) in radians.
        phi: Roll angle (rotation around X-axis) in radians.

    Returns:
        A 3x3 numpy array representing the rotation matrix.
    """

    c_psi = np.cos(psi)
    s_psi = np.sin(psi)
    c_theta = np.cos(theta)
    s_theta = np.sin(theta)
    c_phi = np.cos(phi)
    s_phi = np.sin(phi)

    R1 = np.array([[1, 0, 0],
                    [0, c_phi, s_phi],
                    [0, -s_phi, c_phi]])

    R2 = np.array([[c_theta, 0, -s_theta],
                    [0, 1, 0],
                    [s_theta, 0, c_theta]])

    R3 = np.array([[c_psi, s_psi, 0],
                    [-s_psi, c_psi, 0],
                    [0, 0, 1]])

    return R1 @ R2 @ R3
