import os

from ultralytics import YOLO

# 强制禁用GPU（避免意外调用CUDA）
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# 加载预训练权重（YOLOv8n为轻量版，如需高精度换成YOLOv8x）
model = YOLO("yolov8n.pt")  # 或 "yolov8s.pt", "yolov8m.pt"...

# 训练参数配置
results = model.train(
    data=os.path.join("E:\data\dataset", "data.yaml"),  # RoboFlow自动生成的配置文件
    epochs=80,  # 减少轮次
    batch=8,  # 小批量降低内存压力
    imgsz=416,  # 匹配下载分辨率
    device="cpu",  # 强制指定CPU
    workers=4,  # 避免多进程内存溢出
    single_cls=False,  # 多类别训练
    optimizer="AdamW",  # SGD对CPU更友好但收敛慢
    lr0=0.001,  # 初始学习率
    pretrained=True,  # 利用预训练权重
    patience=5,  # 早停防过拟合
    dropout=0.1,  # 正则化
    hsv_h=0.01,  # 弱化色彩增强减少计算
    hsv_s=0.01,
    hsv_v=0.01,
    translate=0.05,  # 降低平移增强幅度
    name="snake_cpu_v1",
    deterministic = True  # 稳定训练结果
)

if __name__ == '__main__':
    print("开始训练")
