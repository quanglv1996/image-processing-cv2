import cv2

# Tạo đối tượng VideoCapture
cap = cv2.VideoCapture(0)

# Kiểm tra xem camera có mở được không
if not cap.isOpened():
    print("Không thể mở camera")
else:
    # Liệt kê các độ phân giải cần kiểm tra
    resolutions = [
        (320, 240),
        (640, 480),
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1920, 1080),
        (3840, 2160)
    ]
    
    for res in resolutions:
        width, height = res
        # Thiết lập độ phân giải
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # Đọc lại độ phân giải từ camera
        actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        # Kiểm tra xem độ phân giải có được thiết lập đúng không
        if (actual_width, actual_height) == res:
            print(f"Hỗ trợ độ phân giải: {width}x{height}")
        else:
            print(f"Không hỗ trợ độ phân giải: {width}x{height}")

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
