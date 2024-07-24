import sys
sys.path.append('../.')

import cv2
import numpy as np
import pickle
import os
from tqdm import tqdm
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QMessageBox
import time

class CameraCalib(QThread):
    change_pixel_signal = pyqtSignal(np.ndarray)
    info_update = pyqtSignal(tuple)
    
    def __init__(self, type_calib=0, chessboard_size=(10,7),square_size=1.0, w=1920, h=1080):
        super().__init__()
        self.type_calib = type_calib
        self.chessboard_size =  chessboard_size
        self.square_size = square_size
        self.w = w
        self.h = h
        self.criteria  = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
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
        
        self.cap = None
        
    def calib(self, img):
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Tìm các góc của bàn cờ
        ret, corners = cv2.findChessboardCorners(self.gray, self.chessboard_size, None)
        # Nếu tìm thấy, thêm các điểm 3D và 2D
        if ret:
            self.objpoints.append(self.objp)
            self.imgpoints.append(corners)
            return ret, corners
        else:
            return None, None
            
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
    
    def calib_with_camera(self, id=0, epoch=10):
        count = 0
        self.cap = cv2.VideoCapture(id)
        self.cap.set(cv2.CAP_PROP_FOURCC, 0x47504A4D)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.h)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        while count < epoch:
            self.is_continue = True
            _, img = self.cap.read()
            ret, corners = self.calib(img.copy())
            if ret is not None:
                corners2 = cv2.cornerSubPix(self.gray,corners, (11,11), (-1,-1), self.criteria)
                cv2.drawChessboardCorners(img, (self.chessboard_size[0],self.chessboard_size[1]), corners2, ret)
                count+=1
                self.change_pixel_signal.emit(img)
                self.info_update.emit((count, epoch))
                while self.is_continue:
                    time.sleep(1)
            else:
                self.change_pixel_signal.emit(img)
        self.export_calib_config('./calib.pkl')
        while True:
            _, img = self.cap.read()
            img_res = self.get_img_calibrated(img.copy())
            self.change_pixel_signal.emit(img_res)

    def calib_with_imgs(self):
        pass
    
    def run(self):
        if self.type_calib == 0:
            self.calib_with_camera()

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