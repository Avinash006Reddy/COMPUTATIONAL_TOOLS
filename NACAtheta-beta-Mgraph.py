import numpy as np
import math

class ObliqueShockCalculator:
    def __init__(self, gamma=1.4):
        self.gamma = gamma

    def get_theta(self, beta_deg, M):
        if M <= 1: return None
        beta = math.radians(beta_deg)
        
        if M == float('inf'):
            num = math.sin(2 * beta)
            den = self.gamma + math.cos(2 * beta)
            return math.degrees(math.atan(num / den))

        M2 = M**2
        sin2_beta = math.sin(beta)**2
        if (M2 * sin2_beta - 1) < 0: return None

        num = 2 * (1 / math.tan(beta)) * (M2 * sin2_beta - 1)
        den = M2 * (self.gamma + math.cos(2 * beta)) + 2
        return math.degrees(math.atan(num / den))

    def solve_for_beta(self, M, theta_target):
        mach_angle = math.degrees(math.asin(1/M))
        solutions = []
        # Scan beta from mach angle to 90 degrees
        for b in np.arange(mach_angle, 90.01, 0.01):
            theta = self.get_theta(b, M)
            if theta and abs(theta - theta_target) < 0.05:
                if not solutions or abs(solutions[-1] - b) > 1.0:
                    solutions.append(round(b, 2))
        return solutions

# Example Usage
calc = ObliqueShockCalculator()
M = 2.5
theta = 15.0
betas = calc.solve_for_beta(M, theta)
print(f"For M={M} and theta={theta}°, Beta solutions: {betas}")
