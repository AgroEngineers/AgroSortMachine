import datetime
from enum import Enum
from pathlib import Path

logfile: Path


class LogType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    WEB_SERVER = "WEB SERVER"


def _check_logs_folder():
    Path("logs").mkdir(parents=True, exist_ok=True)


def _load_logfile():
    global logfile
    _check_logs_folder()
    logfile = Path(f"logs/{datetime.datetime.now()}.log")
    with open(logfile, 'x') as f:
        f.write(f"LOG FROM {datetime.datetime.now()}\n")


def log(content: str, log_type: LogType = LogType.INFO):
    log_str = f"[{log_type.value}] <{datetime.datetime.now()}>: {content}"
    print(log_str)
    with open(logfile, 'a') as f:
        f.write(log_str + "\n")


def init_logman():
    _load_logfile()

    log("LogMan here!")
    log(f"LogFile: {str(logfile.absolute())}")
