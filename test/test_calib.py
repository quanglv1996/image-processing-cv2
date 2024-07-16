import cv2
import numpy as np
import glob

# Kích thước của bàn cờ (số lượng ô - 1)
chessboard_size = (10, 7)
# Kích thước của các ô trên bàn cờ (đơn vị tùy chọn, ví dụ: mm)
square_size = 1.0

# Tạo các điểm 3D của các góc bàn cờ
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# Mảng để lưu trữ các điểm 3D và 2D
objpoints = []
imgpoints = []

# Đọc tất cả các ảnh trong thư mục
images = glob.glob('D:/Projects-Persional/image-processing-cv2/test/img/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Tìm các góc của bàn cờ
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # Nếu tìm thấy, thêm các điểm 3D và 2D
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Vẽ các góc bàn cờ và hiển thị ảnh
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Kiểm tra nếu có đủ ảnh để calib
if len(objpoints) > 0 and len(imgpoints) > 0:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print("Calibration was successful.")
    print("Camera matrix:\n", mtx)
    print("Distortion coefficients:\n", dist)
else:
    print("Not enough images for calibration.")

# Reprojection Error
mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )