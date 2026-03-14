import json
import os
import pathlib
from typing import Any

config_pattern = """
{
  "ai": {
    "default_model": ""
  },
  "containers": []
}
"""

config: Any

def read_config():
    global config
    if os.path.isfile("config.json"):
        with open("config.json", "r") as read_file:
            config = json.load(read_file)
    else:
        create_config()
        config = json.loads(config_pattern)

def update_config():
    global config
    with open("config.json", "w") as write_file:
        json.dump(config, write_file, indent=4)

def create_config():
    with open("config.json", "w") as write_file:
        json.dump(config_pattern, write_file)

def range_overlap(a, b):
    return a["min"] <= b["max"] and b["min"] <= a["max"]

def check_conflict():
    containers = config["containers"]
    conflicts = []

    for i in range(len(containers)):
        for j in range(i + 1, len(containers)):
            a = containers[i]
            b = containers[j]

            if a["ai"]["type"] != b["ai"]["type"]:
                continue
            if a["ai"]["model"] != b["ai"]["model"]:
                continue

            if not range_overlap(a["color"]["r"], b["color"]["r"]):
                continue
            if not range_overlap(a["color"]["g"], b["color"]["g"]):
                continue
            if not range_overlap(a["color"]["b"], b["color"]["b"]):
                continue

            if not range_overlap(a["size"]["width"], b["size"]["width"]):
                continue
            if not range_overlap(a["size"]["height"], b["size"]["height"]):
                continue

            conflicts.append((a["id"], b["id"]))

    return conflicts

def find(type_, model, r, g, b, width, height):
    for c in config["containers"]:
        if c["ai"]["type"] != type_:
            continue
        if c["ai"]["model"] != model:
            continue

        if not (c["color"]["r"]["min"] <= r <= c["color"]["r"]["max"]):
            continue
        if not (c["color"]["g"]["min"] <= g <= c["color"]["g"]["max"]):
            continue
        if not (c["color"]["b"]["min"] <= b <= c["color"]["b"]["max"]):
            continue

        if not (c["size"]["width"]["min"] <= width <= c["size"]["width"]["max"]):
            continue
        if not (c["size"]["height"]["min"] <= height <= c["size"]["height"]["max"]):
            continue

        return c

    return None

def get_ai_available():
    return [p.name for p in pathlib.Path("models").glob("*.tflite")]

def get_ai_classes(model_name):
    with open(f"models/{model_name}.txt", "r") as read_file:
        return read_file.read().splitlines()

def get_container(id_):
    for c in config["containers"]:
        if str(c['id']) == str(id_):
            return c
    return None

def set_container(id_, data):
    for c in range(len(config["containers"])):
        if config["containers"][c]["id"] == id_:
            config["containers"][c] = data
            break
    update_config()