import torch
import sys
import pathlib
from PIL import Image
import numpy as np
import cv2  # Để vẽ bounding box
from pathlib import Path  # Để xử lý đường dẫn
import os  # Để xử lý đường dẫn
from yolov5.utils.general import non_max_suppression
from yolov5.utils.torch_utils import select_device
from yolov5.models.experimental import attempt_load

sys.path.append(os.path.abspath('E:\\ĐHBKĐN\\BKĐN-Năm 4, Học kì 1\\PBL6\\X-rays web\\yolov5\\models'))

def load_model():
    """Tải mô hình YOLOv5"""
    PosixPath = Path(r"E:\ĐHBKĐN\BKĐN-Năm 4, Học kì 1\PBL6\X-rays web\yolov5\kaggle\working\yolov5\runs\train\exp\weights\best1.pt")
    pathlib.PosixPath = pathlib.WindowsPath
    device = select_device('cpu')  # Chạy trên CPU. Nếu có GPU, thay đổi thành '0' để sử dụng GPU.
    model = attempt_load(str(PosixPath), device=device)  # Tải mô hình YOLOv5
    return model, device

def model_prediction(test_image, model, device):
    """Xử lý ảnh và dự đoán"""
    image = Image.open(test_image).convert('RGB')
    img_np = np.array(image)
    img = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # PIL -> OpenCV format
    img_resized = cv2.resize(img_np, (640, 640))  # Resize ảnh về 640x640
    img_tensor = torch.from_numpy(img_resized.transpose(2, 0, 1)).float() / 255.0
    img_tensor = img_tensor.unsqueeze(0).to(device)

    # Dự đoán
    with torch.no_grad():
        pred = model(img_tensor)[0]
        pred = non_max_suppression(pred, 0.4, 0.5)  # Ngưỡng conf=0.4, iou=0.5

    labels_sorted = []  # Danh sách nhãn sắp xếp theo độ tin cậy
    colors = generate_colors(len(get_labels()))  # Sinh ra danh sách màu sắc cho các nhãn bệnh

    if pred is not None and len(pred) > 0 and pred[0] is not None:
        detections = pred[0].cpu().numpy()
        for *xyxy, conf, cls in detections:
            x1, y1, x2, y2 = map(int, xyxy)
            cls_name = get_labels()[int(cls)]
            conf_percent = round(float(conf) * 100, 2)
            color = colors[int(cls)]  # Lấy màu sắc tương ứng với nhãn bệnh

            # Vẽ bounding box với màu sắc tương ứng
            cv2.rectangle(img_resized, (x1, y1), (x2, y2), color, 2)
            # Hiển thị nhãn và độ tin cậy
            text = f"{cls_name}: {conf_percent}%"
            cv2.putText(img_resized, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            # Lưu thông tin nhãn và độ tin cậy
            labels_sorted.append(f"{cls_name}: {conf_percent}%")

    # Lưu ảnh đã xử lý vào thư mục static/uploads
    output_image = f"processed_{os.path.basename(test_image)}"
    output_full_path = os.path.join('static/uploads', output_image).replace("\\", "/")
    cv2.imwrite(output_full_path, img_resized)
    print(f"Output image path: {output_full_path}")
    return output_image, labels_sorted

def get_labels():
    """Trả về danh sách nhãn bệnh"""
    return [
        "Aortic enlargement", "Atelectasis", "Calcification", "Cardiomegaly", 
        "Consolidation", "ILD", "Infiltration", "Lung Opacity", "Nodule/Mass", 
        "Other lesion", "Pleural effusion", "Pleural thickening", "Pneumothorax", 
        "Pulmonary fibrosis"
    ]

def generate_colors(num_colors):
    """Tạo danh sách màu sắc ngẫu nhiên"""
    np.random.seed(42)  # Đảm bảo màu sắc nhất quán cho mỗi nhãn
    colors = []
    for _ in range(num_colors):
        color = tuple(np.random.randint(0, 256, 3).tolist())  # Tạo màu RGB ngẫu nhiên
        colors.append(color)
    return colors
