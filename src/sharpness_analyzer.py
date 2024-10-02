import cv2
import numpy as np

class CameraSharpnessAnalyzer:
    MAX_VALUES = {
        'Laplacian': 1000,
        'Sobel': 500,
    }

    def __init__(self):
        pass

    def measure_sharpness_laplacian(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray_image, cv2.CV_64F).var()
        return laplacian_var

    def measure_sharpness_sobel(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(gray_image, cv2.COLOR_BGR2GRAY, 0, 1, ksize=5)
        sobel_mag = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
        sharpness = np.mean(sobel_mag)
        return sharpness


    def get_sharpness_values(self, image):
        sharpness_values = {}
        
        # Chỉ tính toán các phương pháp đã được chọn
        sharpness_values['Laplacian'] = self.measure_sharpness_laplacian(image)
        sharpness_values['Sobel'] = self.measure_sharpness_sobel(image)
        
        return sharpness_values
    
    def get_sharpness_values_percent(self, image):
        sharpness_values = {}
        
        # Chỉ tính toán các phương pháp đã được chọn
        sharpness_values['Laplacian'] = (self.measure_sharpness_laplacian(image)/self.MAX_VALUES['Laplacian']) * 100
        sharpness_values['Sobel'] = (self.measure_sharpness_sobel(image)/self.MAX_VALUES['Sobel']) * 100
     
        return sharpness_values


if __name__ == '__main__':
    analyzer = CameraSharpnessAnalyzer()
  