import platform
import sys

import fastapi
from backendController import mount_backend

app = fastapi.FastAPI()

mount_backend(app)

@app.get("/ui")
async def dick():
    return open("web/webUI.html", "rb").read()

if __name__ == '__main__':
    if sys.version_info != (3,9) and platform.system() != "Linux":
        sys.exit("You must use Python 3.9 and Linux")

    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)





