"""
从所有蛇类中筛选出10张图片，进行手工标注，训练蛇类设备通用模型
Author: Dave
Date: 2025-05-16
"""

import os
from pathlib import Path

import pandas as pd


def select_sampled_photos(path, sampled_size=10):
    """
        选择采样数据.
        arg
            :param path :
            :param sampled_size:
        returns
            int

    """

    df = pd.read_csv(path, dtype={'photo_id': str})

    # 分组随机采样
    return (
        df.groupby('class')
        .apply(lambda x: x['photo_id'].sample(n=min(sampled_size, len(x)), replace=False))
        .reset_index(name='photo_id')
    )


def find_photo_files(photo_ids, search_dir):
    """
    在指定目录中根据photo_id查找照片文件
    返回匹配的文件路径列表
    """
    matched_files = []
    photo_ids = set(photo_ids)  # 转换为集合提高查找效率

    # 遍历目录(包括子目录)
    for root, _, files in os.walk(search_dir):
        for file in files:
            # 检查文件名是否包含任一photo_id
            if any(pid in file for pid in photo_ids):
                matched_files.append(Path(root) / file)

    return matched_files


if __name__ == '__main__':

    # 输入参数
    cvs_path = 'E:/data/nature/data.csv'
    photos_dir = "E:/data/nature"  # 替换为你的照片目录
    output_dir = "E:/data/nature/sampled"  # 输出目录

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 选择样例
    photos = select_sampled_photos(cvs_path)['photo_id']

    # 查找文件
    found_files = find_photo_files(photos, photos_dir)

    # 复制文件到输出目录
    for src_file in found_files:
        dest_file = Path(output_dir) / src_file.name
        dest_file.write_bytes(src_file.read_bytes())
