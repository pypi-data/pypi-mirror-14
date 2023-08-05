from .translation import String
from . import task
from . import mapping
from typing import List


class StaticPoint:
    def __init__(self):
        self.alt = 0
        self.type = "Turning Point"
        self.name = String()
        self.position = mapping.Point(0, 0)
        self.speed = 0
        self.formation_template = ""
        self.action = ""

    def load_from_dict(self, d, translation):
        self.alt = d["alt"]
        self.type = d["type"]
        self.position.x = d["x"]
        self.position.y = d["y"]
        self.action = d["action"]
        self.formation_template = d["formation_template"]
        self.speed = d["speed"]
        self.name = translation.get_string(d["name"])

    def dict(self):
        return {
            "alt": self.alt,
            "type": self.type,
            "name": self.name.id,
            "x": self.position.x,
            "y": self.position.y,
            "speed": round(self.speed, 13),
            "formation_template": self.formation_template,
            "action": self.action
        }


class MovingPoint(StaticPoint):
    def __init__(self):
        super(MovingPoint, self).__init__()
        self.alt_type = "BARO"
        self.ETA = 0
        self.ETA_locked = True
        self.speed_locked = True
        self.tasks = []  # type: List[task.Task]
        self.properties = None
        self.airdrome_id = None
        self.action = "Off Road"

    def load_from_dict(self, d, translation):
        super(MovingPoint, self).load_from_dict(d, translation)
        self.alt_type = d.get("alt_type", None)
        self.ETA_locked = d["ETA_locked"]
        self.ETA = d["ETA"]
        self.speed_locked = d["speed_locked"]
        for t in d["task"]["params"]["tasks"]:
            self.tasks.append(task._create_from_dict(d["task"]["params"]["tasks"][t]))
        self.airdrome_id = d.get("airdromeId", None)
        self.properties = d.get("properties", None)

    def dict(self):
        d = super(MovingPoint, self).dict()
        d["alt_type"] = self.alt_type
        d["ETA"] = self.ETA
        d["ETA_locked"] = self.ETA_locked
        d["speed_locked"] = self.speed_locked
        tasks = {}
        for i in range(0, len(self.tasks)):
            self.tasks[i].number = i+1
            tasks[i+1] = self.tasks[i].dict()
        d["task"] = {
            "id": "ComboTask",
            "params": {
                "tasks": {i+1: self.tasks[i].dict() for i in range(0, len(self.tasks))}
            }
        }
        if self.airdrome_id is not None:
            d["airdromeId"] = self.airdrome_id
        if self.properties is not None:
            d["properties"] = self.properties
        return d
