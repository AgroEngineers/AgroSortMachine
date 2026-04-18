import re

from asm.api.ai import ASMAI
from asm.api.cv import ASMDetector, ASMOpenCV
from asm.api.hardware import ASMHardware
from logman import *

import core

ai: ASMAI
hw: ASMHardware
od: ASMDetector
cvs: list[ASMOpenCV]


def logo():
    log("=======================================================")
    log("    ___   _____ __  ___   ______            _          ")
    log("   /   | / ___//  |/  /  / ____/___  ____ _(_)___  ___ ")
    log("  / /| | \__ \/ /|_/ /  / __/ / __ \/ __ `/ / __ \/ _ \\")
    log(" / ___ |___/ / /  / /  / /___/ / / / /_/ / / / / /  __/")
    log("/_/  |_/____/_/  /_/  /_____/_/ /_/\__, /_/_/ /_/\___/ ")
    log("                                  /____/               ")
    log("=======================================================")


def load():
    pass


def init():
    logo()
    core.init_fastapi()


def get_id_by_display_name(display_name: str) -> str:
    return re.sub(r'[\\/*?:"<>| ]', '_', display_name)

