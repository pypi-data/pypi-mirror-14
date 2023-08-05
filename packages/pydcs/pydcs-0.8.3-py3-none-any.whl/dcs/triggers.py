import copy
from typing import List

from dcs import mapping


class TriggerZone:
    def __init__(self, _id, position: mapping.Point, radius=1500, hidden=False, name=""):
        self.id = _id
        self.radius = radius
        self.position = copy.copy(position)
        self.hidden = hidden
        self.name = name
        self.color = {1: 1, 2: 1, 3: 1, 4: 0.15}  # TODO color attributes

    def dict(self):
        return {
            "name": self.name,
            "hidden": self.hidden,
            "x": self.position.x,
            "y": self.position.y,
            "zoneId": self.id,
            "radius": self.radius,
            "color": self.color
        }

    def __repr__(self):
        return "TriggerZone({id}, {x}, {y}, {r}, '{n}')".format(
            id=self.id, x=self.position.x, y=self.position.y, r=self.radius, n=self.name
        )


class Triggers:
    def __init__(self):
        self.current_zone_id = 0
        self._zones = []  # type: List[TriggerZone]

    def load_from_dict(self, data):
        self.current_zone_id = 0
        self._zones = []
        for x in data["zones"]:
            imp_zone = data["zones"][x]
            tz = TriggerZone(
                imp_zone["zoneId"],
                mapping.Point(imp_zone["x"], imp_zone["y"]),
                imp_zone["radius"],
                imp_zone["hidden"],
                imp_zone["name"]
            )
            tz.color = imp_zone["color"]
            self._zones.append(tz)
            self.current_zone_id = max(self.current_zone_id, tz.id)

    def add_triggerzone(self, position: mapping.Point, radius=1500, hidden=False, name="") -> TriggerZone:
        self.current_zone_id += 1
        tz = TriggerZone(self.current_zone_id, position, radius, hidden, name)
        self._zones.append(tz)
        return tz

    def zones(self) -> List[TriggerZone]:
        return self._zones

    def dict(self):
        return {
            "zones": {i + 1: self._zones[i].dict() for i in range(0, len(self._zones))}
        }
