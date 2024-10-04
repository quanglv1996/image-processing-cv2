import sys
sys.path.append('../.')

import cv2
import numpy as np


class HSVFilter:
    def __init__(self):
        # Define HSV color ranges for various colors
        self.color_dict_HSV = {
            'black': [[180, 255, 30], [0, 0, 0]],
            'white': [[180, 18, 255], [0, 0, 231]],
            'red1': [[180, 255, 255], [159, 50, 70]],
            'red2': [[9, 255, 255], [0, 50, 70]],
            'green': [[89, 255, 255], [36, 50, 70]],
            'blue': [[128, 255, 255], [90, 50, 70]],
            'yellow': [[35, 255, 255], [25, 50, 70]],
            'purple': [[158, 255, 255], [129, 50, 70]],
            'orange': [[24, 255, 255], [10, 50, 70]],
            'gray': [[180, 18, 230], [0, 0, 40]]
        }  # upper, lower

        # Initialize color boundaries
        self.h_lower, self.s_lower, self.v_lower = 0, 0, 0
        self.h_upper, self.s_upper, self.v_upper = 0, 0, 0

    def get_colorspaces_sample(self, name: str) -> list:
        """Get sample HSV color ranges for a specific color name."""
        return self.color_dict_HSV.get(name, [[0, 0, 0], [0, 0, 0]])

    def update_colorspaces(self, h_lower: int, s_lower: int, v_lower: int, 
                            h_upper: int, s_upper: int, v_upper: int) -> None:
        """Update the HSV color boundaries."""
        self.h_lower, self.s_lower, self.v_lower = h_lower, s_lower, v_lower
        self.h_upper, self.s_upper, self.v_upper = h_upper, s_upper, v_upper

    def get_colorspaces(self) -> tuple:
        """Get the current HSV color boundaries."""
        return (self.h_lower, self.s_lower, self.v_lower, 
                self.h_upper, self.s_upper, self.v_upper)

    def show_info(self) -> None:
        """Print the current HSV color boundaries."""
        print(f'Colorspaces | HL: {self.h_lower} | SL: {self.s_lower} | VL: {self.v_lower} | '
              f'HU: {self.h_upper} | SU: {self.s_upper} | VU: {self.v_upper} |')

    def run(self, frame: np.ndarray) -> np.ndarray:
        """Apply the HSV filter on the given frame."""
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_lower = np.array([self.h_lower, self.s_lower, self.v_lower], dtype=np.uint8)
        color_upper = np.array([self.h_upper, self.s_upper, self.v_upper], dtype=np.uint8)
        mask = cv2.inRange(hsv_img, color_lower, color_upper)
        return mask
