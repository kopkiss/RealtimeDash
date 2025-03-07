from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import redis
import json

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)  # เชื่อม Redis

class DataInput(BaseModel):
    value: int

# บันทึกเซ็นเซอร์ลง Redis + Broadcast ผ่าน WebSocket
@app.post("/receive")
async def receive_data(data: DataInput):
    print(f"Received: {data.value}")
    r.set("sensor_value", json.dumps({"value": data.value}))  # บันทึกค่า
    await broadcast_data()  # ส่งข้อมูลไปยัง WebSocket
    return {"message": "Data received", "value": data.value}

# WebSocket Clients
clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # รอข้อความจาก Client (แต่เราไม่ใช้)
    except:
        clients.remove(websocket)  # ถ้าหลุดให้ลบออก

# ฟังก์ชัน Broadcast ข้อมูลไปยัง Clients ทุกคน
async def broadcast_data():
    data = r.get("sensor_value")
    print(f"Broadcast: {data}")
    if data:
        for client in clients:
            await client.send_text(data)