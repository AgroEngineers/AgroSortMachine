import logging
import platform
import sys

import fastapi
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

# import config
import engine
import logman


class MyLogmanHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        logman.log(log_entry, logman.LogType.WEB_SERVER)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(message)s"},
    },
    "handlers": {
        "logman_handler": {
            "class": "__main__.MyLogmanHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["logman_handler"], "level": "INFO"},
        "uvicorn.access": {"handlers": ["logman_handler"], "level": "INFO"},
    },
}

# from backend import mount_backend

app = fastapi.FastAPI()


def init_fastapi():
    # config.read_config()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # mount_backend(app)

    @app.get("/ui", response_class=HTMLResponse)
    async def web_ui():
        return open("web/webUI.html", "rb").read()

    import uvicorn
    uvicorn.run("core:app", host="0.0.0.0", port=8000, reload=False, log_config=LOGGING_CONFIG)


if __name__ == '__main__':
    if sys.version_info != (3, 9) and platform.system() != "Linux":
        sys.exit("You must use Python 3.9 and Linux")

    print("ASM booting...")
    logman.init_logman()
    engine.init()
