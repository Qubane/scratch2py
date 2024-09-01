import os
import json
from typing import Any
from zipfile import ZipFile


class ScratchVariable:
    def __init__(self, name: str, value: Any):
        self.name: str = name
        self.value: Any = value

    def __repr__(self):
        return f"['{self.name}': {self.value.__repr__()}]"


class ScratchList:
    def __init__(self, name: str, data: list[Any]):
        self.name: str = name
        self.data: list[Any] = data

    def __repr__(self):
        if len(self.data) < 10:
            return f"['{self.name}': {self.data.__repr__()}]"
        else:
            return f"['{self.name}': {self.data[:10].__repr__()}, ...]"


class Block:
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name")
        self.opcode: str = kwargs.get("opcode")
        self.next: str = kwargs.get("next")
        self.parent: str = kwargs.get("parent")
        self.inputs: dict[str, list] = kwargs.get("inputs")
        self.fields: dict[str, list] = kwargs.get("fields")
        self.shadow: bool = kwargs.get("shadow")
        self.top_level: bool = kwargs.get("topLevel")


class Target:
    def __init__(self, **kwargs):
        self.is_stage: bool = kwargs.get("isStage")
        self.name: str = kwargs.get("name")
        self.variable: dict[str, ScratchVariable] = dict()
        for key, val in kwargs.get("variables", {}).items():
            self.variable[key] = ScratchVariable(val[0], val[1])
        self.lists: dict[str, ScratchList] = dict()
        for key, val in kwargs.get("lists", {}).items():
            self.lists[key] = ScratchList(val[0], val[1])
        self.broadcasts: dict[str, list] = kwargs.get("broadcasts")
        self.blocks: dict[str, Block] = dict()
        for key, val in kwargs.get("blocks", {}).items():
            self.blocks[key] = Block(**val, name=key)
        self.comments: dict = kwargs.get("comments")
        self.current_costume: int = kwargs.get("currentCostume")
        self.costumes: list = kwargs.get("costumes")
        self.sounds: list = kwargs.get("sounds")
        self.volume: int = kwargs.get("volume")
        self.layer_order: int = kwargs.get("layerOrder")


class Sprite(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visible: bool = kwargs.get("visible")
        self.x: int = kwargs.get("x")
        self.y: int = kwargs.get("y")
        self.size: int = kwargs.get("size")
        self.direction: int = kwargs.get("direction")
        self.draggable: bool = kwargs.get("draggable")
        self.rotation_style: str = kwargs.get("rotationStyle")


class Stage(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tempo: int = kwargs.get("tempo")
        self.video_state: str = kwargs.get("videoState")
        self.video_transparency: int = kwargs.get("videoTransparency")
        self.tts_language: None = kwargs.get("textToSpeechLanguage")


class Project:
    def __init__(self, data: dict):
        self.targets: list[Stage | Sprite] = list()
        for val in data.get("targets", []):
            if val.get("isStage"):
                self.targets.append(Stage(**val))
            else:
                self.targets.append(Sprite(**val))
        self.monitors: list = data.get("monitors")
        self.extensions: list = data.get("extensions")
        self.meta: dict[str, str | dict] = data.get("meta")


def extract_data(filepath: str):
    if not os.path.isdir("temp"):
        os.mkdir("temp")
    with ZipFile(filepath, "r") as zip_file:
        zip_file.extractall("temp")


def decode_data():
    with open("temp/project.json", "r", encoding="utf-8") as file:
        json_project = json.loads(file.read())
        project = Project(json_project)
        print(json.dumps(json_project, indent=2))


if __name__ == '__main__':
    extract_data("Project.sb3")
    decode_data()
