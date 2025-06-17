## Mô tả

Đề tài "Nhận diện một số bệnh từ ảnh CT phổi bằng YOLOv5" tập trung vào việc xây dựng một hệ thống hỗ trợ chẩn đoán hình ảnh y tế sử dụng học sâu,
cụ thể là mô hình YOLOv5 (You Only Look Once version 5) để phát hiện các biểu hiện bệnh lý trên ảnh CT phổi. Dự án hướng đến việc tự động phát hiện
và khoanh vùng các vùng tổn thương đặc trưng như viêm phổi, tràn dịch màng phổi, xơ hoá phổi hoặc dấu hiệu nghi ngờ ung thư. Dữ liệu sử dụng là tập ảnh
CT ngực được gán nhãn thủ công từ chuyên gia hoặc lấy từ các nguồn công khai. Ảnh đầu vào được tiền xử lý để đảm bảo chất lượng huấn luyện như chuẩn hóa
độ sáng, tăng cường dữ liệu (augmentation), và chuyển đổi định dạng phù hợp với yêu cầu của YOLOv5. Mô hình sau khi huấn luyện sẽ có khả năng xác định
nhanh và chính xác các vùng nghi ngờ bệnh trên ảnh đầu vào, giúp bác sĩ tiết kiệm thời gian và tăng độ chính xác trong chẩn đoán. Ngoài ra, hệ thống
được tích hợp vào một giao diện web cho phép người dùng tải ảnh lên và nhận kết quả phân tích trực quan bằng bounding box và nhãn bệnh. Ứng dụng này
mở ra tiềm năng hỗ trợ sàng lọc bệnh phổi tự động trong môi trường y tế thiếu nhân lực hoặc trong các hệ thống khám chữa bệnh từ xa.

