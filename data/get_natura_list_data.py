import math
import os
from typing import Union, Any, List

import pandas as pd
import requests
from pandas import DataFrame
from tqdm import tqdm


def get_china_snake_species(max_results=100, per_page=20):
    base_url = "https://api.inaturalist.org/v1/observations/species_counts"

    params = {
        "verifiable": "true",  # 可核实的
        "spam": "false",  # 确保有图片
        "place_id": 6903,  # 地区id 中国6903
        "taxon_id": 85553,  # 类id
        "locale": "zh-CN",  # 仅下载“研究级别”数据（已验证）
        "per_page": per_page,  # 页大小
        "include_ancestors": "true"  # 包含祖先
    }

    species = []
    for page in tqdm(range(1, math.ceil(max_results / per_page) + 1)):
        params["page"] = page
        response = requests.get(base_url, params=params, verify=False).json()

        if response.get("results"):
            for obs in response.get("results"):
                if obs.get("taxon"):
                    species.append(
                        {
                            "id": obs["taxon"]["id"],
                            "count": obs["count"],
                            "english_common_name": obs["taxon"]["english_common_name"],  # 英文名称
                            "preferred_common_name": obs["taxon"]["preferred_common_name"],  # 中文名称
                        }
                    )
    return species

    # # 存储为CSV（含图片URL、物种名等信息）
    # df = pd.DataFrame([
    #     {
    #         "id": obs["taxon"]["id"],
    #         "count": obs["count"],
    #         "name": obs["taxon"]["name"],  # 获取高清图
    #         "preferred_common_name": obs["taxon"]["preferred_common_name"],
    #     } for obs in observations if obs.get("taxon")
    # ])
    # df.to_csv(f"inat_snake_data.csv", index=False)
    # return df


def get_obs_img_ids(taxon_id, max_photo=100):
    base_url = "https://api.inaturalist.org/v1/observations"

    params = {
        "taxon_id": taxon_id,  # 可真实
        "place_id": 6903,  # 可真实
        "order_by": "observed_on",  # 投票
        "order": "desc",  # 投票
        "quality_grade": "research",  # 每页返回数量（最大200）
        "photos": "true",  # 按热门排序（高质量图片靠前）
        "locale": "zh-CN",  # 按热门排序（高质量图片靠前）
        "page": 1,  # 按热门排序（高质量图片靠前）
        "return_bounds": "true",  # 按热门排序（高质量图片靠前）
        "verifiable": "true",  # 按热门排序（高质量图片靠前）
        "per_page": max_photo,  # 100张
    }

    observations = []
    response = requests.get(base_url, params=params, verify=False).json()
    observations.extend(response["results"])

    photons = []
    for obs in observations:
        observation_photos = obs.get("observation_photos")
        for photo in observation_photos:
            url = photo["photo"]["url"]
            url = url.replace("square", "medium")
            photons.append({
                "photo_id": photo["photo"]["id"],
                "url": url
            })

    return photons


def get_obs_photo_file(photo_id, img_url, save_path):
    id = str(photo_id)
    file_name = os.path.join(save_path, id + ".jpg")
    os.makedirs(os.path.dirname(file_name), exist_ok=True)  # 自动创建目录
    response = requests.get(img_url, verify=False, stream=True)
    if response.status_code == 200:
        with open(file_name, "wb") as file:  # "wb" 以二进制写入
            file.write(response.content)
        print("下载完成！")
    else:
        print(f"下载失败，HTTP 状态码: {response.status_code}，url: {img_url}")


if __name__ == '__main__':

    # 下载路径
    base_path = "E:/data/nature"
    image_files = []
    # 获取种类
    species = get_china_snake_species(10, 5)

    for spec in tqdm(species):

        # 获取图片信息
        photos = get_obs_img_ids(spec["id"], 5)
        print(f"<spec>{spec['preferred_common_name']},<spec_id>{spec['id']},<phots>{len(photos)}")

        # 下载照片
        for photo in photos:
            save_path = os.path.join(base_path, spec["english_common_name"])
            get_obs_photo_file(photo["photo_id"], photo["url"], save_path)
            image_files.append({
                "class": spec["english_common_name"],
                "name": spec["preferred_common_name"],
                "photo_id": photo["photo_id"],
            })

    # 存储为CSV（含图片URL、物种名等信息）
    df = pd.DataFrame(image_files).to_csv(f"{base_path}/data.csv", index=False)
