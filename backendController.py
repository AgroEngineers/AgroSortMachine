from fastapi import *

import hardwareController
from hardwareController import *
from starlette.responses import StreamingResponse
from typing import Optional
from json import loads

app = FastAPI()

class Socket:
    ws: Optional[WebSocket] = None

    @classmethod
    async def send(cls, message):
        if cls.ws:
            await cls.ws.send_json(message)
    @classmethod
    def close(cls):
        cls.ws = None
        abadon()

def mount_backend(main_app: FastAPI):
    main_app.mount("/api", app)

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    Socket.ws = ws
    try:
        while True:
            await proceed_ws(loads(await ws.receive_text()))
    except WebSocketDisconnect:
        pass
    finally:
        Socket.close()

async def proceed_ws(data):
    if data["type"] == "mode":
        aiController.allow_control = not bool(data["manual"])
    elif data["type"] == "sync":
        await sync(data)
    elif data["type"] == "info":
        await Socket.send({
            "type": "info",
            "machine": {
                "connected": is_machine_connected(),
                "availablePorts": available_ports()
            },
            "camera": {
                "connected": False,
                "availablePorts": get_cameras()
            }
        })
    elif data["type"] == "connectHw":
        await connect_machine(data["port"])
    elif data["type"] == "connectCam":
        await connect_camera(data["port"])
    elif data["type"] == "disconnect":
        abadon()

@app.get("/video")
async def video_feed():
    return StreamingResponse(
        hardwareController.camera.generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "X-Frame-Options": "ALLOWALL"
        }
    )
