import sys
sys.path.append('../.')

import cv2
import numpy as np
import pickle
import os
from tqdm import tqdm

class CameraCalib(object):
    def __init__(self, chessboard_size=(10,7),square_size=1.0, w=1920, h=1080):
        self.chessboard_size =  chessboard_size
        self.square_size = square_size
        self.w = w
        self.h = h
        self.objp = np.zeros((self.chessboard_size[0] * self.chessboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:self.chessboard_size[0], 0:self.chessboard_size[1]].T.reshape(-1, 2)
        self.objp *= self.square_size
        
        # Mảng để lưu trữ các điểm 3D và 2D
        self.objpoints = []
        self.imgpoints = []
        self.gray = None
        self.newcameramtx = None
        self.roi = None
        self.ret = None
        self.mtx = None
        self.dist = None
        self.rvecs = None
        self.tvecs = None
        
    def calib(self, img):
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Tìm các góc của bàn cờ
        ret, corners = cv2.findChessboardCorners(self.gray, self.chessboard_size, None)
        # Nếu tìm thấy, thêm các điểm 3D và 2D
        if ret:
            self.objpoints.append(self.objp)
            self.imgpoints.append(corners)
            
    def export_calib_config(self, save_folder='./'):
        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.gray.shape[::-1], None, None)
        self.newcameramtx, self.roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.w,self.h), 1, (self.w,self.h))
        try:
            config_calibration = [self.objpoints, self.imgpoints, self.gray]
            path_save = os.path.join(save_folder, 'calib.pkl')
            with open(path_save, 'wb') as f:
                pickle.dump(config_calibration,f)
            return True
        except Exception as e:
            return False
        
    def load_calib_config(self, path_config='./calib.pkl'):
        try:
            with open(path_config, 'rb') as f:
                self.objpoints, self.imgpoints, self.gray = pickle.load(f)
                self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.gray.shape[::-1], None, None)
            self.newcameramtx, self.roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.w,self.h), 1, (self.w,self.h))
            return True
        except Exception as e:
            return False
        
    def get_img_calibrated(self, img):
        img_res = img.copy()
        if self.newcameramtx is None:
            return None
        else:
            dst = cv2.undistort(img_res, self.mtx, self.dist, None, self.newcameramtx)
            x, y, w, h = self.roi
            dst = dst[y:y+h, x:x+w]
            img_res = dst.astype('uint8')
            return img_res
    
    def calculate_error(self):
        mean_error = 0
        for i in range(len(self.objpoints)):
            imgpoints2, _ = cv2.projectPoints(self.objpoints[i], self.rvecs[i], self.tvecs[i], self.mtx, self.dist)
            error = cv2.norm(self.imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            mean_error += error
        return mean_error

def main():
    calib_camera = CameraCalib()
    img_folder = 'D:/Projects-Persional/image-processing-cv2/test/img'
    filenames = os.listdir(img_folder)
    
    for filename in tqdm(filenames):
        path_file = os.path.join(img_folder, filename)
        img = cv2.imread(path_file)
        calib_camera.calib(img)
    
    calib_camera.export_calib_config()
    print('Error: {}'.format(calib_camera.calculate_error()))
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    while True:
        _, img = cap.read()
        img_calib = calib_camera.get_img_calibrated(img)
        cv2.imshow('img', img_calib)
        cv2.waitKey(10)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()