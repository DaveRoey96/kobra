from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import uvicorn

from ultralytics import YOLO

app = FastAPI()
model = YOLO('yolov8n.pt')  # 加载训练好的模型

# 添加CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，生产环境应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

@app.post("/detect")
async def detect_snake(file: UploadFile):
    img = Image.open(io.BytesIO(await file.read()))
    results = model(img)

    if len(results[0].boxes) == 0:
        return {"error": "No objects detected"}

    return {
        "species": results[0].names[int(results[0].boxes.cls[0])],
        "confidence": float(results[0].boxes.conf[0]),
        "location": results[0].boxes.xyxy[0].tolist()
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)  # 默认port=8000
