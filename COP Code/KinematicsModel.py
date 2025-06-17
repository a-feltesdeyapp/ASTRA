import math
import numpy as np
import euler


class ASTRAKinematicsModel:

    def __init__(self):
        """
        Initialize the ASTRA Kinematics Model
        """

        # ASTRA physical parameters
        self.l_ab = 2.06  # in
        self.l_bc = 6  # in
        self.r_c1o = [8, -9.5, -1.9]  # in
        self.r_c2o = [8, 9.5, -1.9]  # in
        self.r_a1o = np.add([7.0 + 15.0/16.0, -1*(7.0 + 9.0/16.0), (3.0 + 9.0/16.0)], [0.64, 0, 0])
        self.r_a2o = np.add([7.0 + 15.0/16.0, 1 * (7.0 + 9.0 / 16.0), (3.0 + 9.0 / 16.0)], [0.64, 0, 0])
        self.psi_a1 = math.pi / 2
        self.psi_a2 = -math.pi / 2

        pass

    # Step 1: Convert pitch and roll to the
    def _pitch_roll_to_vectors(self, phi: float, theta: float, r_co, r_ao) -> list[float]:
        """
        Convert desired pitch and roll angles (in radians) to a vector needed
        for kinematics model calculations
        """

        # Generate Rotation Matrix
        rotation_matrix = euler.euler_321_matrix(0, theta, phi)

        # Perform the rotation
        r_co_prime = np.matmul(rotation_matrix, r_co)

        r_ca = np.subtract(r_co_prime, r_ao)

        return r_ca

    # Run kinematics for a single arm
    def _single_arm_kinematics(self, r_ca: list[float], psi_a) -> float:
        """
        Implement the ASTRA kinematics model.
        Mom come pick me up, I'm scared.
        """

        # Parameters e, f, g - no physical significance to these
        # Apologies for the single-letter variable names
        e = 2 * self.l_ab * r_ca[2]
        f = 2 * self.l_ab * (math.cos(psi_a) * r_ca[0] + math.sin(psi_a) * r_ca[1])
        g = np.linalg.norm(r_ca) ** 2 - (self.l_bc ** 2 - self.l_ab ** 2)

        # Motor angle theta_AB
        theta_ab = np.asin(g / (math.sqrt(e ** 2 + f ** 2))) - math.atan2(f, e)

        return theta_ab

    def calculate(self, phi, theta) -> list[float]:
        """
        Calculate angles for each actuator.
        """

        theta = -theta
        phi = -phi

        r_c1o_prime = self._pitch_roll_to_vectors(phi, theta, self.r_c1o, self.r_a1o)
        r_c2o_prime = self._pitch_roll_to_vectors(phi, theta, self.r_c2o, self.r_a2o)

        theta_a1 = self._single_arm_kinematics(r_c1o_prime, self.psi_a1) - math.pi
        theta_a2 = self._single_arm_kinematics(r_c2o_prime, self.psi_a2) - math.pi

        return [float(theta_a1), float(theta_a2)]


def deg2rad(angle) -> float:
    """Convert degrees to radians"""

    return angle * math.pi / 180


def main():
    kinematics_model_obj = ASTRAKinematicsModel()
    theta_vec = kinematics_model_obj.calculate(deg2rad(5), deg2rad(0))
    print(np.multiply(theta_vec, 180 / math.pi))


if __name__ == '__main__':
    main()
