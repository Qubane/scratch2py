import os
import json
from zipfile import ZipFile


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
        self.name: str = kwargs.get("Stage")
        self.variable: dict[str, list] = kwargs.get("variables")
        self.lists: dict[str, list] = kwargs.get("lists")
        self.broadcasts: dict[str, list] = kwargs.get("broadcasts")
        self.blocks: dict[str, Block] = dict()
        for key, val in kwargs.get("blocks", {}).items():
            self.blocks[key] = Block(**val)
        self.comments: dict = kwargs.get("comments")
        self.current_costume: int = kwargs.get("currentCostume")
        self.costumes: list = kwargs.get("costumes")
        self.sounds: list = kwargs.get("sounds")
        self.volume: int = kwargs.get("volume")
        self.layer_order: int = kwargs.get("layerOrder")
        self.visible: bool = kwargs.get("visible")
        self.x: int = kwargs.get("x")
        self.y: int = kwargs.get("y")
        self.size: int = kwargs.get("size")
        self.direction: int = kwargs.get("direction")
        self.draggable: bool = kwargs.get("draggable")
        self.rotation_style: str = kwargs.get("rotationStyle")

        if self.is_stage:
            self.tempo: int = kwargs.get("tempo")
            self.video_state: str = kwargs.get("videoState")
            self.video_transparency: int = kwargs.get("videoTransparency")
            self.tts_language: None = kwargs.get("textToSpeechLanguage")


class Project:
    def __init__(self, data: dict):
        self.targets: list[Target] = list()
        for val in data.get("targets", []):
            self.targets.append(Target(**val))
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
        project = Project(
            json.loads(file.read()))


if __name__ == '__main__':
    extract_data("Project.sb3")
    decode_data()
