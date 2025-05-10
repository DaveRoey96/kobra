import os
import pandas as pd
from sklearn.model_selection import train_test_split


def csv_to_yolo(csv_path, img_dir, output_label_dir):
    df = pd.read_csv(csv_path)

    # 处理每张图片的所有标注
    for img_name, group in df.groupby('image_path'):
        img_path = os.path.join(img_dir, img_name)

        # 验证图片是否存在 (重要！)
        assert os.path.exists(img_path), f"Image {img_path} not found!"

        # 获取图片尺寸 (可动态获取或CSV中预设)
        img_width, img_height = 640, 640  # 假设或通过PIL读取

        # 生成YOLO格式标签
        label_path = os.path.join(output_label_dir,
                                  os.path.splitext(img_name)[0] + '.txt')

        with open(label_path, 'w') as f:
            for _, row in group.iterrows():
                # 坐标归一化计算
                x_center = ((row['xmin'] + row['xmax']) / 2) / img_width
                y_center = ((row['ymin'] + row['ymax']) / 2) / img_height
                width = (row['xmax'] - row['xmin']) / img_width
                height = (row['ymax'] - row['ymin']) / img_height

                # 写入标签文件
                f.write(f"{int(row['class_id'])} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


if __name__ == '__main__':
    # 示例调用
    csv_to_yolo(
        csv_path='E:\data\sample_0\sample_0_venom_nonvenom.csv',
        img_dir='/kaggle/input/your-dataset/images',
        output_label_dir='dataset/labels/train'
    )
