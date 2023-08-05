# terrain module
from typing import List, Dict, Optional
from dcs import mapping, lua
from dcs import unittype
import random


class ParkingSlot:
    def __init__(self,
                 crossroad_idx,
                 position: mapping.Point,
                 large=False,
                 slot_name=None,
                 heli=False,
                 airplanes=True,
                 length=None,
                 width=None,
                 height=None,
                 shelter=False):
        self.crossroad_idx = crossroad_idx
        self.position = position
        self.length = length
        self.width = width
        self.height = height
        self.helicopter = heli
        self.airplanes = airplanes
        self.large = large
        self.shelter = shelter
        self.unit_id = None  # type: int
        self.slot_name = slot_name

    def __repr__(self):
        return 'ParkingSlot({id}, "{name}", large={large}, heli={heli})'.format(
            id=self.crossroad_idx, name=self.slot_name, large=self.large, heli=self.helicopter
        )


class Runway:
    def __init__(self, heading, ils=None, leftright=0):
        """

        :param heading: Compass direction of runway
        :param ils:
        :param leftright: 0 only 1 runway
                          1 left runway
                          2 right runway
        :return: None
        """
        self.heading = heading
        self.ils = ils
        self.leftright = leftright


class Airport:
    id = None
    name = None
    position = None  # type: mapping.Point
    tacan = None
    frequencies = []
    unit_zones = []  # type: List[mapping.Rectangle]
    civilian = True
    slot_version = 1

    def __init__(self):
        self.runway_free = True
        self.runways = []  # type: List[Runway]
        self.parking_slots = []  # type: List[ParkingSlot]

        # warehouse values
        self.coalition = "NEUTRAL"
        self.size = 100
        self.speed = 16.666666
        self.periodicity = 30
        self.unlimited_munitions = True
        self.unlimited_aircrafts = True
        self.unlimited_fuel = True
        self.operating_level_air = 10
        self.operating_level_fuel = 10
        self.operating_level_equipment = 10
        self.aircrafts = {}
        self.weapons = {}
        self.suppliers = {}
        self.gasoline_init = 100
        self.methanol_mixture_init = 100
        self.diesel_init = 100
        self.jet_init = 100

    def load_from_dict(self, d):
        self.coalition = d["coalition"]
        self.speed = d["speed"]
        self.size = d["size"]
        self.periodicity = d["periodicity"]
        self.unlimited_munitions = d["unlimitedMunitions"]
        self.unlimited_fuel = d["unlimitedFuel"]
        self.unlimited_aircrafts = d["unlimitedAircrafts"]
        self.operating_level_air = d["OperatingLevel_Air"]
        self.operating_level_equipment = d["OperatingLevel_Eqp"]
        self.operating_level_fuel = d["OperatingLevel_Fuel"]
        self.gasoline_init = d.get("gasoline", {}).get("InitFuel", 100)
        self.diesel_init = d.get("diesel", {}).get("InitFuel", 100)
        self.jet_init = d.get("jet_fuel", {}).get("InitFuel", 100)
        self.methanol_mixture_init = d.get("methanol_mixture", {}).get("InitFuel", 100)
        self.aircrafts = d["aircrafts"]
        self.weapons = d["weapons"]

    def set_blue(self):
        self.set_coalition("BLUE")

    def set_red(self):
        self.set_coalition("RED")

    def set_neutral(self):
        self.set_coalition("NEUTRAL")

    def set_coalition(self, side):
        if side.lower() in ["red", "blue", "neutral"]:
            self.coalition = side.upper()
            return True
        return False

    def is_red(self):
        return self.coalition == "RED"

    def is_blue(self):
        return self.coalition == "BLUE"

    def random_unit_zone(self) -> mapping.Rectangle:
        if self.unit_zones:
            return self.unit_zones[random.randrange(0, len(self.unit_zones))]
        return mapping.Rectangle.from_point(mapping.Point(self.position.x + 500, self.position.y), 200)

    def _free_parking_slots_resolve_v1(self, large: bool, helicopter: bool) -> List[ParkingSlot]:
        slots_index = range(0, len(self.parking_slots))
        free_large_slots = {x for x in slots_index
                            if self.parking_slots[x].unit_id is None and
                            self.parking_slots[x].large}

        large_slots = sorted([self.parking_slots[x] for x in free_large_slots], key=lambda x: x.slot_name)
        if large:
            return large_slots

        free_heli_slots = {x for x in slots_index
                           if self.parking_slots[x].unit_id is None and
                           self.parking_slots[x].helicopter and not self.parking_slots[x].large}

        heli_slots = sorted([self.parking_slots[x] for x in free_heli_slots], key=lambda x: x.slot_name)
        if helicopter:
            return heli_slots + large_slots

        free_slots = list(self.parking_slots[x] for x in slots_index if self.parking_slots[x].unit_id is None and
                          not self.parking_slots[x].large and not self.parking_slots[x].helicopter)
        free_slots = sorted(free_slots, key=lambda x: x.slot_name)
        return free_slots + heli_slots + large_slots

    def _free_parking_slots_resolve_v2(self, aircraft_type: unittype.FlyingType) -> List[ParkingSlot]:
        free_slots = [x for x in self.parking_slots
                      if x.unit_id is None and
                      aircraft_type.width < x.width and
                      aircraft_type.height < (x.height or 1000) and
                      aircraft_type.length < x.length and
                      aircraft_type.helicopter == x.helicopter and
                      not aircraft_type.helicopter == x.airplanes]

        slots_sorted = sorted(free_slots, key=lambda x: x.slot_name)
        return slots_sorted

    def free_parking_slots(self, aircraft_type: unittype.FlyingType) -> List[ParkingSlot]:
        if self.slot_version == 1:
            return self._free_parking_slots_resolve_v1(aircraft_type.large_parking_slot, aircraft_type.helicopter)
        else:
            return self._free_parking_slots_resolve_v2(aircraft_type)

    def free_parking_slot(self, aircraft_type: unittype.FlyingType) -> Optional[ParkingSlot]:
        slots = self.free_parking_slots(aircraft_type)
        if slots:
            return slots[0]
        return None

    def dict(self):
        d = {
            "coalition": self.coalition,
            "speed": self.speed,
            "size": self.size,
            "periodicity": self.periodicity,
            "unlimitedMunitions": self.unlimited_munitions,
            "unlimitedFuel": self.unlimited_fuel,
            "unlimitedAircrafts": self.unlimited_aircrafts,
            "OperatingLevel_Air": self.operating_level_air,
            "OperatingLevel_Eqp": self.operating_level_equipment,
            "OperatingLevel_Fuel": self.operating_level_fuel,
            "gasoline": {"InitFuel": self.gasoline_init},
            "diesel": {"InitFuel": self.diesel_init},
            "jet_fuel": {"InitFuel": self.jet_init},
            "methanol_mixture": {"InitFuel": self.methanol_mixture_init},
            "aircrafts": self.aircrafts,
            "weapons": self.weapons,
            "suppliers": self.suppliers
        }
        return d

    def __repr__(self):
        return "Airport(" + self.name + ")"


class MapView:
    def __init__(self, center: mapping.Point, zoom=1000000):
        self.position = center
        self.zoom = zoom

    def load_from_dict(self, d):
        self.position = mapping.Point(d["centerX"], d["centerY"])
        self.zoom = d["zoom"]

    def dict(self):
        return {
            "centerX": self.position.x,
            "centerY": self.position.y,
            "zoom": self.zoom
        }


class Terrain:
    bounds = None  # type: mapping.Rectangle
    map_view_default = None  # type: MapView

    def __init__(self, name: str):
        self.name = name
        self.center = {"lat": 0, "long": 0}  # WGS84 decimal
        self.bullseye_blue = {"x": 0, "y": 0}
        self.bullseye_red = {"x": 0, "y": 0}
        self.airports = {}  # type: Dict[str,Airport]

    def airport_by_id(self, id: int) -> Airport:
        for x in self.airports:
            if self.airports[x].id == id:
                return self.airports[x]
        return None

    def airport_list(self) -> List[Airport]:
        for x in self.airports:
            yield self.airports[x]


class Warehouses:
    def __init__(self, terrain: Terrain):
        self.terrain = terrain
        self.warehouses = {}

    def load_dict(self, data):
        for x in data.get("airports", {}):
            self.terrain.airport_by_id(x).load_from_dict(data["airports"][x])

    def __str__(self):
        airports = self.terrain.airports
        d = {
            "warehouses": self.warehouses,
            "airports": {airports[x].id: airports[x].dict() for x in airports}
        }
        return lua.dumps(d, "warehouses", 1)
