import zipfile
import sys
import os
import tempfile
import copy
from enum import Enum
from typing import List, Dict, Union, Optional
from datetime import datetime, timezone
from . import lua
from . import unitgroup
from . import unittype
from .country import Country
from . import countries
from .point import StaticPoint, MovingPoint
from .unit import Plane, Helicopter, Ship, Vehicle, Static
from .translation import Translation
from .terrain import Terrain, Caucasus, Nevada, ParkingSlot, Airport
from .goals import Goals
from . import mapping
from . import planes
from . import helicopters
from . import task
from . import weather
from .forcedoptions import ForcedOptions
from .groundcontrol import GroundControl


class Options:
    def __init__(self):
        self.options = {}

    def load_from_dict(self, d):
        self.options = d

    def __str__(self):
        return lua.dumps(self.options, "options", 1)

    def __repr__(self):
        return repr(self.options)


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


class Coalition:
    def __init__(self, name, bullseye=None):
        self.name = name
        self.countries = {}  # type: Dict[str, Country]
        self.bullseye = bullseye
        self.nav_points = []  # TODO

    def set_bullseye(self, bulls):
        self.bullseye = bulls

    def add_country(self, country):
        self.countries[country.name] = country
        return country

    def remove_country(self, name):
        return self.countries.pop(name)

    def swap_country(self, coalition, name):
        return coalition.add_country(self.remove_country(name))

    def country(self, country_name: str):
        return self.countries.get(country_name, None)

    def find_group(self, group_name, search="exact"):
        for c in self.countries:
            g = self.countries[c].find_group(group_name, search)
            if g:
                return g

        return None

    def dict(self):
        d = {"name": self.name}
        if self.bullseye:
            d["bullseye"] = self.bullseye
        d["country"] = {}
        i = 1
        for country in sorted(self.countries.keys()):
            d["country"][i] = self.country(country).dict()
            i += 1
        d["nav_points"] = {}
        return d


class TriggerZone:
    def __init__(self, _id, position: mapping.Point, radius=1500, hidden=False, name=""):
        self.id = _id
        self.radius = radius
        self.position = copy.copy(position)
        self.hidden = hidden
        self.name = name
        self.color = {1: 1, 2: 1, 3: 1, 4: 0.15}

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


class StartType(Enum):
    Cold = 1
    Warm = 2
    Runway = 3

    @staticmethod
    def from_string(s):
        st_map = {
            "cold": StartType.Cold,
            "warm": StartType.Warm,
            "runway": StartType.Runway
        }
        return st_map[s.lower()]


class Mission:
    """This class represents the whole dcs .miz file.

    A .miz file is a zip file containing all needed files to run a mission.
    example.miz:

      * mission
      * options
      * warehouses
      * i10n

        * DEFAULT
        * dictionary

          * mapResource
          * [localized resource files, .wav, .jpg, ...]
    """
    COUNTRY_IDS = {x for x in range(0, 13)} | {x for x in range(15, 47)}

    def __init__(self, terrain: Union[Caucasus, Nevada]=None):
        if terrain is None:
            terrain = Caucasus()

        self.current_unit_id = 0
        self.current_group_id = 0
        self.current_dict_id = 0
        self.filename = None

        self.translation = Translation(self)
        self.map_resource = MapResource(self)

        self._description_text = self.string("dcs mission")
        self._description_bluetask = self.string("blue task")
        self._description_redtask = self.string("red task")
        self.sortie = self.string("sortie text")
        self.pictureFileNameR = []
        self.pictureFileNameB = []
        self.version = 11
        self.currentKey = 0
        self.start_time = datetime.fromtimestamp(1306886400 + 43200, timezone.utc)  # 01-06-2011 12:00:00 UTC
        self.season_from_start_time = True
        self.terrain = terrain
        self.trigrules = {}
        self.triggers = Triggers()
        self.options = Options()
        self.warehouses = Warehouses(self.terrain)
        self.goals = Goals()
        blue = Coalition("blue")
        blue.add_country(countries.Australia())
        blue.add_country(countries.Belgium())
        blue.add_country(countries.Canada())
        blue.add_country(countries.Croatia())
        blue.add_country(countries.CzechRepublic())
        blue.add_country(countries.Denmark())
        blue.add_country(countries.France())
        blue.add_country(countries.Georgia())
        blue.add_country(countries.Germany())
        blue.add_country(countries.Israel())
        blue.add_country(countries.Italy())
        blue.add_country(countries.Norway())
        blue.add_country(countries.Poland())
        blue.add_country(countries.SouthKorea())
        blue.add_country(countries.Spain())
        blue.add_country(countries.TheNetherlands())
        blue.add_country(countries.UK())
        blue.add_country(countries.USA())
        blue.add_country(countries.Turkey())

        red = Coalition("red")
        red.add_country(countries.Abkhazia())
        red.add_country(countries.Belarus())
        red.add_country(countries.China())
        red.add_country(countries.Iran())
        red.add_country(countries.Kazakhstan())
        red.add_country(countries.NorthKorea())
        red.add_country(countries.Russia())
        red.add_country(countries.Serbia())
        red.add_country(countries.SouthOssetia())
        red.add_country(countries.Syria())
        red.add_country(countries.Ukraine())

        blue.bullseye = terrain.bullseye_blue
        red.bullseye = terrain.bullseye_red

        self.coalition = {"blue": blue, "red": red}  # type: Dict[str, Coalition]

        self.map = {
            "zoom": self.terrain.map_view_default["zoom"],
            "centerY": self.terrain.map_view_default["center"].y,
            "centerX": self.terrain.map_view_default["center"].x
        }

        self.failures = {}
        self.trig = {}
        self.groundControl = GroundControl()
        self.forced_options = ForcedOptions()
        self.resourceCounter = {}  # keep default or empty, old format
        self.needModules = {}
        self.weather = weather.Weather(self.terrain)
        # TODO used modules
        self.usedModules = {
            'Su-25A by Eagle Dynamics': True,
            'MiG-21Bis AI by Leatherneck Simulations': True,
            'UH-1H Huey by Belsimtek': True,
            'Su-25T by Eagle Dynamics': True,
            'F-86F Sabre by Belsimtek': True,
            'Su-27 Flanker by Eagle Dynamics': True,
            'Hawk T.1A AI by VEAO Simulations': True,
            'MiG-15bis AI by Eagle Dynamics': True,
            'Ka-50 Black Shark by Eagle Dynamics': True,
            'Combined Arms by Eagle Dynamics': True,
            'L-39C/ZA by Eagle Dynamics': True,
            'A-10C Warthog by Eagle Dynamics': True,
            'F-5E/E-3 by Belsimtek': True,
            'C-101 Aviojet': True,
            'TF-51D Mustang by Eagle Dynamics': True,
            './CoreMods/aircraft/MQ-9 Reaper': True,
            'C-101 Aviojet by AvioDev': True,
            'P-51D Mustang by Eagle Dynamics': True,
            'A-10A by Eagle Dynamics': True,
            'L-39C': True,
            'World War II AI Units by Eagle Dynamics': True,
            'MiG-15bis by Belsimtek': True,
            'F-15C': True,
            'Flaming Cliffs by Eagle Dynamics': True,
            'Bf 109 K-4 by Eagle Dynamics': True,
            'Mi-8MTV2 Hip by Belsimtek': True,
            'MiG-21Bis by Leatherneck Simulations': True,
            'M-2000C by RAZBAM Sims': True,
            'M-2000C AI by RAZBAM Sims': True,
            'FW-190D9 Dora by Eagle Dynamics': True,
            'Caucasus': True,
            'Hawk T.1A by VEAO Simulations': True,
            'F-86F Sabre AI by Eagle Dynamics': True
        }

    def _import_moving_point(self, group: unitgroup.Group, imp_group) -> unitgroup.Group:
        for imp_point_idx in imp_group["route"]["points"]:
            imp_point = imp_group["route"]["points"][imp_point_idx]
            point = MovingPoint()
            point.load_from_dict(imp_point, self.translation)
            group.add_point(point)
        return group

    def _import_static_point(self, group: unitgroup.Group, imp_group) -> unitgroup.Group:
        for imp_point_idx in imp_group["route"]["points"]:
            imp_point = imp_group["route"]["points"][imp_point_idx]
            point = StaticPoint()
            point.load_from_dict(imp_point, self.translation)
            group.add_point(point)
        return group

    def _imp_coalition(self, coalition, key):
        if key not in coalition:
            return None
        imp_col = coalition[key]
        col = Coalition(key, imp_col["bullseye"])
        for country_idx in imp_col["country"]:
            imp_country = imp_col["country"][country_idx]
            _country = countries.get_by_id(imp_country["id"])

            if "vehicle" in imp_country:
                for vgroup_idx in imp_country["vehicle"]["group"]:
                    vgroup = imp_country["vehicle"]["group"][vgroup_idx]
                    vg = unitgroup.VehicleGroup(vgroup["groupId"], self.translation.get_string(vgroup["name"]),
                                                vgroup["start_time"])
                    vg.load_from_dict(vgroup)
                    self.current_group_id = max(self.current_group_id, vg.id)

                    self._import_moving_point(vg, vgroup)

                    # units
                    for imp_unit_idx in vgroup["units"]:
                        imp_unit = vgroup["units"][imp_unit_idx]
                        unit = Vehicle(
                            id=imp_unit["unitId"],
                            name=self.translation.get_string(imp_unit["name"]),
                            _type=imp_unit["type"])
                        unit.load_from_dict(imp_unit)

                        self.current_unit_id = max(self.current_unit_id, unit.id)
                        vg.add_unit(unit)
                    _country.add_vehicle_group(vg)

            if "ship" in imp_country:
                for group_idx in imp_country["ship"]["group"]:
                    imp_group = imp_country["ship"]["group"][group_idx]
                    vg = unitgroup.ShipGroup(imp_group["groupId"], self.translation.get_string(imp_group["name"]),
                                             imp_group["start_time"])
                    vg.load_from_dict(imp_group)
                    self.current_group_id = max(self.current_group_id, vg.id)

                    self._import_moving_point(vg, imp_group)

                    # units
                    for imp_unit_idx in imp_group["units"]:
                        imp_unit = imp_group["units"][imp_unit_idx]
                        unit = Ship(
                            id=imp_unit["unitId"],
                            name=self.translation.get_string(imp_unit["name"]),
                            _type=imp_unit["type"])
                        unit.load_from_dict(imp_unit)

                        self.current_unit_id = max(self.current_unit_id, unit.id)
                        vg.add_unit(unit)
                    _country.add_ship_group(vg)

            if "plane" in imp_country:
                for pgroup_idx in imp_country["plane"]["group"]:
                    pgroup = imp_country["plane"]["group"][pgroup_idx]
                    plane_group = unitgroup.PlaneGroup(pgroup["groupId"], self.translation.get_string(pgroup["name"]),
                                                       pgroup["start_time"])
                    plane_group.load_from_dict(pgroup)
                    self.current_group_id = max(self.current_group_id, plane_group.id)

                    self._import_moving_point(plane_group, pgroup)

                    # units
                    for imp_unit_idx in pgroup["units"]:
                        imp_unit = pgroup["units"][imp_unit_idx]
                        plane = Plane(
                            _id=imp_unit["unitId"],
                            name=self.translation.get_string(imp_unit["name"]),
                            _type=planes.plane_map[imp_unit["type"]],
                            _country=_country)
                        plane.load_from_dict(imp_unit)

                        self.current_unit_id = max(self.current_unit_id, plane.id)
                        plane_group.add_unit(plane)
                    _country.add_plane_group(plane_group)

            if "helicopter" in imp_country:
                for pgroup_idx in imp_country["helicopter"]["group"]:
                    pgroup = imp_country["helicopter"]["group"][pgroup_idx]
                    helicopter_group = unitgroup.HelicopterGroup(
                        pgroup["groupId"],
                        self.translation.get_string(pgroup["name"]),
                        pgroup["start_time"])
                    helicopter_group.load_from_dict(pgroup)
                    self.current_group_id = max(self.current_group_id, helicopter_group.id)

                    self._import_moving_point(helicopter_group, pgroup)

                    # units
                    for imp_unit_idx in pgroup["units"]:
                        imp_unit = pgroup["units"][imp_unit_idx]
                        heli = Helicopter(
                            _id=imp_unit["unitId"],
                            name=self.translation.get_string(imp_unit["name"]),
                            _type=helicopters.helicopter_map[imp_unit["type"]],
                            _country=_country)
                        heli.load_from_dict(imp_unit)

                        self.current_unit_id = max(self.current_unit_id, heli.id)
                        helicopter_group.add_unit(heli)
                    _country.add_helicopter_group(helicopter_group)

            if "static" in imp_country:
                for sgroup_idx in imp_country["static"]["group"]:
                    sgroup = imp_country["static"]["group"][sgroup_idx]
                    static_group = unitgroup.StaticGroup(sgroup["groupId"], self.translation.get_string(sgroup["name"]))
                    static_group.load_from_dict(sgroup)
                    self.current_group_id = max(self.current_group_id, static_group.id)

                    self._import_static_point(static_group, sgroup)

                    # units
                    for imp_unit_idx in sgroup["units"]:
                        imp_unit = sgroup["units"][imp_unit_idx]
                        static = Static(
                            id=imp_unit["unitId"],
                            name=self.translation.get_string(imp_unit["name"]),
                            _type=imp_unit["type"])
                        static.load_from_dict(imp_unit)

                        self.current_unit_id = max(self.current_unit_id, static.id)
                        static_group.add_unit(static)
                    _country.add_static_group(static_group)
            col.add_country(_country)
        return col

    def load_file(self, filename):
        self.filename = filename
        mission_dict = {}
        options_dict = {}
        warehouse_dict = {}
        dictionary_dict = {}

        def loaddict(fname, mizfile):
            with mizfile.open(fname) as mfile:
                data = mfile.read()
                data = data.decode()
                return lua.loads(data)

        with zipfile.ZipFile(filename, 'r') as miz:
            mission_dict = loaddict('mission', miz)
            if mission_dict["mission"]["version"] < 9:
                print("Mission file is using an old format, be aware!", file=sys.stderr)
            options_dict = loaddict('options', miz)
            warehouse_dict = loaddict('warehouses', miz)
            dictionary_dict = loaddict('l10n/DEFAULT/dictionary', miz)
            if 'l10n/DEFAULT/mapResource' in miz.namelist():
                mapresource_dict = loaddict('l10n/DEFAULT/mapResource', miz)
                self.map_resource.load_from_dict(mapresource_dict, miz)

        imp_mission = mission_dict["mission"]

        # import translations
        self.translation = Translation(self)
        translation_dict = dictionary_dict["dictionary"]
        for sid in translation_dict:
            self.translation.set_string(sid, translation_dict[sid], 'DEFAULT')

        self.current_dict_id = imp_mission["maxDictId"]

        # print(self.translation)

        # setup terrain
        if imp_mission["theatre"] == 'Caucasus':
            self.terrain = Caucasus()
        elif imp_mission["theatre"] == 'Nevada':
            self.terrain = Nevada()
        else:
            raise RuntimeError("Unknown theatre: '{theatre}'".format(theatre=imp_mission["theatre"]))

        # import options
        self.options = Options()
        self.options.load_from_dict(options_dict["options"])

        # import warehouses
        self.warehouses = Warehouses(self.terrain)
        self.warehouses.load_dict(warehouse_dict["warehouses"])

        # import base values
        self._description_text = self.translation.get_string(imp_mission["descriptionText"])
        self._description_bluetask = self.translation.get_string(imp_mission["descriptionBlueTask"])
        self._description_redtask = self.translation.get_string(imp_mission["descriptionRedTask"])
        self.sortie = self.translation.get_string(imp_mission["sortie"])
        for pic in sorted(imp_mission["pictureFileNameR"]):
            self.pictureFileNameR.append(imp_mission["pictureFileNameR"][pic])
        for pic in sorted(imp_mission["pictureFileNameB"]):
            self.pictureFileNameB.append(imp_mission["pictureFileNameB"][pic])
        self.version = imp_mission["version"]
        self.currentKey = imp_mission["currentKey"]
        self.start_time = datetime.fromtimestamp(1306886400 + imp_mission["start_time"], timezone.utc)
        self.usedModules = imp_mission["usedModules"]
        self.needModules = imp_mission["needModules"]

        # groundControl
        self.groundControl = GroundControl()
        self.groundControl.load_from_dict(imp_mission.get("groundControl"))

        # goals
        self.goals = Goals()
        self.goals.load_from_dict(imp_mission["goals"])

        # trig
        self.trig = imp_mission["trig"]  # TODO

        # triggers
        self.triggers = Triggers()
        self.triggers.load_from_dict(imp_mission["triggers"])

        # trigrules
        self.trigrules = imp_mission["trigrules"]  # TODO

        # failures
        self.failures = imp_mission["failures"]  # TODO

        # forced options
        self.forced_options.load_from_dict(imp_mission["forcedOptions"])

        # map
        self.map = imp_mission["map"]

        # weather
        self.season_from_start_time = False
        imp_weather = imp_mission["weather"]
        self.weather = weather.Weather(self.terrain)
        self.weather.load_from_dict(imp_weather)

        # import coalition with countries and units
        self.coalition["blue"] = self._imp_coalition(imp_mission["coalition"], "blue")
        self.coalition["red"] = self._imp_coalition(imp_mission["coalition"], "red")
        neutral_col = self._imp_coalition(imp_mission["coalition"], "neutral")
        if neutral_col:
            self.coalition["neutral"] = neutral_col

        return True

    def description_text(self):
        return str(self._description_text)

    def set_description_text(self, text):
        self._description_text.set(text)

    def description_bluetask_text(self):
        return str(self._description_bluetask)

    def set_description_bluetask_text(self, text):
        self._description_bluetask.set(text)

    def description_redtask_text(self):
        return str(self._description_redtask)

    def set_description_redtask_text(self, text):
        self._description_redtask.set(text)

    def add_picture_red(self, filepath):
        self.pictureFileNameR.append(self.map_resource.add_resource_file(filepath))

    def add_picture_blue(self, filepath):
        self.pictureFileNameB.append(self.map_resource.add_resource_file(filepath))

    def next_group_id(self):
        self.current_group_id += 1
        return self.current_group_id

    def next_unit_id(self):
        self.current_unit_id += 1
        return self.current_unit_id

    def next_dict_id(self):
        self.current_dict_id += 1
        return self.current_dict_id

    def string(self, s, lang='DEFAULT'):
        """
        Create a new String() object for translation
        :param s: string for lang
        :param lang: language for s
        :return: A new String() object for string s
        """
        return self.translation.create_string(s, lang)

    def vehicle(self, name, _type: unittype.VehicleType):
        if not issubclass(_type, unittype.VehicleType):
            raise TypeError("_type not a unittype.VehicleType class: " + repr(_type))
        return Vehicle(self.next_unit_id(), self.string(name), _type.id)

    def vehicle_group(self, _country, name, _type: unittype.VehicleType, position: mapping.Point,
                      heading=0, group_size=1, action="Off Road",
                      formation=unitgroup.VehicleGroup.Formation.Line) -> unitgroup.VehicleGroup:
        vg = unitgroup.VehicleGroup(self.next_group_id(), self.string(name))

        for i in range(1, group_size + 1):
            v = self.vehicle(name + " Unit #{nr}".format(nr=i), _type)
            v.position.x = position.x
            v.position.y = position.y + (i - 1) * 20
            v.heading = heading
            vg.add_unit(v)

        wp = vg.add_waypoint(vg.units[0].position, action, 0)
        wp.ETA_locked = True
        if _type.eplrs:
            wp.tasks.append(task.EPLRS(1))

        vg.formation(formation)

        _country.add_vehicle_group(vg)
        return vg

    def vehicle_group_platoon(self, _country, name, types: List[unittype.VehicleType], position: mapping.Point, heading=0, action="Off Road",
                              formation=unitgroup.VehicleGroup.Formation.Line) -> unitgroup.VehicleGroup:
        vg = unitgroup.VehicleGroup(self.next_group_id(), self.string(name))

        eplrs = False
        for i in range(0, len(types)):
            utype = types[i]
            v = self.vehicle(name + " Unit #{nr}".format(nr=i + 1), utype)
            v.position.x = position.x
            v.position.y = position.y + i * 20
            v.heading = heading
            if utype.eplrs:
                eplrs = True
            vg.add_unit(v)

        wp = vg.add_waypoint(vg.units[0].position, action, 0)
        wp.ETA_locked = True
        if eplrs:
            wp.tasks.append(task.EPLRS(1))

        vg.formation(formation)

        _country.add_vehicle_group(vg)
        return vg

    def ship(self, name, _type):
        return Ship(self.next_unit_id(), self.string(name), _type)

    def ship_group(self, _country, name, _type: str, position: mapping.Point, heading=0, group_size=1) -> unitgroup.ShipGroup:
        sg = unitgroup.ShipGroup(self.next_group_id(), self.string(name))

        for i in range(1, group_size + 1):
            v = self.ship(name + " Unit #{nr}".format(nr=i), _type)
            v.position.x = position.x
            v.position.y = position.y + (i - 1) * 20
            v.heading = heading
            sg.add_unit(v)

        wp = sg.add_waypoint(position, 20)
        wp.ETA_locked = True

        _country.add_ship_group(sg)
        return sg

    def plane_group(self, name) -> unitgroup.PlaneGroup:
        """This creates a plain plane group without any units or starting points.

        This method is a advanced interface method not intended for simple use.
        For adding full featured plane group see

         * :py:meth:`flight_group`
         * :py:meth:`flight_group_inflight`
         * :py:meth:`flight_group_from_airport`

        :param name: Group name
        :return: A new :py:class:`dcs.unitgroup.PlaneGroup`
        """
        return unitgroup.PlaneGroup(self.next_group_id(), self.string(name))

    def plane(self, name, _type: planes.PlaneType, country: Country):
        """Creates a new plane unit.

        This method is a advanced interface method not intended for simple usage.
        For adding full a featured plane group see

         * :py:meth:`flight_group`
         * :py:meth:`flight_group_inflight`
         * :py:meth:`flight_group_from_airport`

        :param name: unit name
        :param _type: type of the plane
        :param country: the plane belongs, needed for default liveries
        :return: A new :py:class:`dcs.unit.Plane`
        """
        return Plane(self.next_unit_id(), self.string(name), _type, country)

    def helicopter(self, name, _type: helicopters.HelicopterType, country: Country):
        """Creates a new helicopter unit.

        This method is a advanced interface method not intended for simple usage.
        For adding full a featured helicopter group see

         * :py:meth:`flight_group`
         * :py:meth:`flight_group_inflight`
         * :py:meth:`flight_group_from_airport`

        :param name: unit name
        :param _type: type of the helicopter
        :param country: the helicopter belongs, needed for default liveries
        :return: A new :py:class:`dcs.unit.Helicopter`
        """
        return Helicopter(self.next_unit_id(), self.string(name), _type, country)

    def aircraft(self, name, _type: unittype.FlyingType, country: Country) -> Union[Plane, Helicopter]:
        """Creates a new plane or helicopter unit, depending on the _type.

        This method is a advanced interface method not intended for simple usage.
        For adding full a featured plane/helicopter group see

         * :py:meth:`flight_group`
         * :py:meth:`flight_group_inflight`
         * :py:meth:`flight_group_from_airport`

        :param name: unit name
        :param _type: type of the aircraft
        :param country: the aircraft belongs, needed for default liveries
        :return: A new :py:class:`dcs.unit.Plane` or :py:class:`dcs.unit.Helicopter`
        """
        if _type.helicopter:
            return Helicopter(self.next_unit_id(), self.string(name), _type, country)
        return Plane(self.next_unit_id(), self.string(name), _type, country)

    def helicopter_group(self, name) -> unitgroup.HelicopterGroup:
        """Creates a plain helicopter group without any units or starting points.

        This method is a advanced interface method not intended for simple usage.
        For adding a full featured helicopter group see

         * :py:meth:`flight_group`
         * :py:meth:`flight_group_inflight`
         * :py:meth:`flight_group_from_airport`

        :param name: Group name
        :return: A new :py:class:`dcs.unitgroup.HelicopterGroup`
        """
        return unitgroup.HelicopterGroup(self.next_group_id(), self.string(name))

    @classmethod
    def _assign_callsign(cls, _country, group):
        callsign_name = None
        category = group.units[0].unit_type.category
        if category in _country.callsign:
            callsign_name = _country.next_callsign_category(category)

        i = 1
        for unit in group.units:
            if category in _country.callsign:
                unit.callsign_dict["name"] = callsign_name + str(1) + str(i)
                unit.callsign_dict[3] = i
            else:
                unit.callsign = _country.next_callsign_id()
            i += 1

    @staticmethod
    def _load_tasks(mp: MovingPoint, maintask: task.MainTask, eplrs: bool):
        for t in maintask.perform_task:
            ptask = t()
            ptask.auto = True
            mp.tasks.append(ptask)
        if eplrs:
            mp.tasks.append(task.EPLRS(1))
        return mp

    def _flying_group_from_airport(self, _country, group: unitgroup.FlyingGroup,
                                   maintask: task.MainTask,
                                   airport: Airport,
                                   start_type: StartType=StartType.Cold,
                                   parking_slots: List[ParkingSlot] = None) -> unitgroup.FlyingGroup:

        for unit in group.units:
            spos = airport.position
            if start_type != StartType.Runway:
                parking_slot = parking_slots.pop(0) if parking_slots else airport.free_parking_slot(
                    unit.unit_type.large_parking_slot, unit.unit_type.helicopter)
                if parking_slot is None:
                    raise RuntimeError("No free parking slot at " + airport.name)
                spos = parking_slot.position
                unit.set_parking(parking_slot)
            unit.position = copy.copy(spos)

        group.load_task_default_loadout(maintask)

        self._assign_callsign(_country, group)

        point_start_type_map = {
            StartType.Cold: ("TakeOffParking", "From Parking Area"),
            StartType.Warm: ("TakeOffParkingHot", "From Parking Area Hot"),
            StartType.Runway: ("TakeOff", "From Runway")
        }
        mp = MovingPoint()
        mp.type = point_start_type_map[start_type][0]
        mp.action = point_start_type_map[start_type][1]
        mp.position = copy.copy(group.units[0].position)
        mp.airdrome_id = airport.id
        mp.alt = group.units[0].alt
        Mission._load_tasks(mp, maintask, group.units[0].unit_type.eplrs)

        group.add_point(mp)

        return group

    def _flying_group_inflight(self, _country, group: unitgroup.FlyingGroup,
                               maintask: task.MainTask, altitude, speed) -> unitgroup.FlyingGroup:

        i = 0
        for unit in group.units:
            unit.alt = altitude
            unit.position.x += i * 10
            unit.speed = speed / 3.6
            i += 1

        self._assign_callsign(_country, group)

        group.load_task_default_loadout(maintask)

        mp = MovingPoint()
        mp.type = "Turning Point"
        mp.action = mp.type
        mp.position = copy.copy(group.units[0].position)
        mp.alt = altitude
        mp.speed = speed / 3.6

        Mission._load_tasks(mp, maintask, group.units[0].unit_type.eplrs)

        group.add_point(mp)

        return group

    def flight_group_inflight(self,
                              country,
                              name: str,
                              aircraft_type: unittype.FlyingType,
                              position: mapping.Point,
                              altitude: int,
                              speed=None,
                              maintask: Optional[task.MainTask] = None,
                              group_size: int=1
                              ) -> Union[unitgroup.PlaneGroup, unitgroup.HelicopterGroup]:
        """Add a new Plane/Helicopter group inflight.

        The type of the resulting group depends on the given aircraft_type.

        :param country: the new group will belong to
        :param name: of the new group
        :param aircraft_type: type of all units in the group
        :param position: :py:class:`Point` where the new group will be placed
        :param altitude: of the new group
        :param speed: of the new group, if none a default will be picked
        :param maintask: if none the default task for the aircraft_type wil be used
        :param group_size: number of units in the group(maximum 4 or 1 for certain types)
        :return: a new :py:class:`dcs.unitgroup.PlaneGroup` or :py:class:`dcs.unitgroup.HelicopterGroup`
        """
        if maintask is None:
            maintask = aircraft_type.task_default

        if aircraft_type.helicopter:
            ag = self.helicopter_group(name)
            speed = speed if speed else 200
        else:
            ag = self.plane_group(name)
            speed = speed if speed else 600
        ag.task = maintask.name
        group_size = min(group_size, aircraft_type.group_size_max)

        for i in range(1, group_size + 1):
            p = self.aircraft(name + " Pilot #{nr}".format(nr=i), aircraft_type, country)
            p.position = copy.copy(position)
            p.fuel *= 0.9
            ag.add_unit(p)

        country.add_aircraft_group(self._flying_group_inflight(country, ag, maintask, altitude, speed))
        return ag

    def flight_group_from_airport(self,
                                  country: Country,
                                  name,
                                  aircraft_type: unittype.FlyingType,
                                  airport: Airport,
                                  maintask: task.MainTask = None,
                                  start_type: StartType=StartType.Cold,
                                  group_size=1,
                                  parking_slots: List[ParkingSlot] = None) -> \
            Union[unitgroup.PlaneGroup, unitgroup.HelicopterGroup]:
        """Add a new Plane/Helicopter group at the given airport.

        Runway, warm/cold start depends on the given start_type.

        :param country: Country object the plane group belongs to
        :param name: Name of the aircraft group
        :param maintask: Task of the aircraft group
        :param aircraft_type: FlyingType class that describes the aircraft_type
        :param airport: Airport object on which to spawn the helicopter
        :param start_type: Start from runway, cold or warm parking position
        :param parking_slots: List of parking slots to use for aircrafts
        :param group_size: number of units in the group(maximum 4 or 1 for certain types)
        :return: a new :py:class:`dcs.unitgroup.PlaneGroup` or :py:class:`dcs.unitgroup.HelicopterGroup`
        """
        if maintask is None:
            maintask = aircraft_type.task_default

        ag = self.helicopter_group(name) if aircraft_type.helicopter else self.plane_group(name)
        ag.task = maintask.name
        group_size = min(group_size, aircraft_type.group_size_max)

        for i in range(1, group_size + 1):
            p = self.aircraft(name + " Pilot #{nr}".format(nr=i), aircraft_type, country)
            ag.add_unit(p)

        country.add_aircraft_group(
            self._flying_group_from_airport(country, ag, maintask, airport, start_type, parking_slots))
        return ag

    def flight_group(self,
                     country: Country,
                     name: str,
                     aircraft_type: unittype.FlyingType,
                     airport: Optional[Airport],
                     position: Optional[mapping.Point],
                     altitude=3000,
                     speed=500,
                     maintask: Optional[task.MainTask]=None,
                     start_type: StartType=StartType.Runway,
                     group_size=1
                     ) -> unitgroup.FlyingGroup:
        if airport:
            fg = self.flight_group_from_airport(country, name, aircraft_type,
                                                airport, maintask, start_type, group_size)
        else:
            fg = self.flight_group_inflight(country, name, aircraft_type,
                                            position, altitude, speed, maintask, group_size)

        return fg

    def awacs_flight(self,
                     _country: Country,
                     name: str,
                     plane_type: planes.PlaneType,
                     airport: Optional[Airport],
                     position: mapping.Point,
                     race_distance=30 * 1000,
                     heading=90,
                     altitude=4500,
                     speed=550,
                     start_type: StartType=StartType.Cold,
                     frequency=140) -> unitgroup.PlaneGroup:
        if airport:
            awacs = self.flight_group_from_airport(_country, name, plane_type, airport, task.AWACS, start_type)
            wp = awacs.add_runway_waypoint(airport)
        else:
            p = position.point_from_heading((heading + 180) % 360, 2000)
            awacs = self.flight_group_inflight(_country, name, plane_type, p, altitude, speed, task.AWACS)
            p = position.point_from_heading(heading + 180, 1000)
            wp = awacs.add_waypoint(p, altitude, speed)

        wp.tasks.append(task.SetFrequencyCommand(frequency))

        wp = awacs.add_waypoint(position, altitude, speed)
        wp.tasks.append(task.OrbitAction(altitude, speed, task.OrbitAction.OrbitPattern.RaceTrack))

        p = position.point_from_heading(heading, race_distance)
        awacs.add_waypoint(p, altitude, speed)

        return awacs

    def refuel_flight(self,
                      _country,
                      name: str,
                      plane_type: planes.PlaneType,
                      airport: Optional[Airport],
                      position: mapping.Point,
                      race_distance=30 * 1000,
                      heading=90,
                      altitude=4500,
                      speed=407,
                      start_type: StartType=StartType.Cold,
                      frequency=140,
                      tacanchannel="10X") -> unitgroup.PlaneGroup:
        if airport:
            tanker = self.flight_group_from_airport(_country, name, plane_type, airport,
                                                    task.Refueling, start_type=start_type)
            wp = tanker.add_runway_waypoint(airport)
        else:
            p = position.point_from_heading((heading + 180) % 360, 2000)
            tanker = self.flight_group_inflight(_country, name, plane_type, p, altitude, speed, task.Refueling)
            p = position.point_from_heading(heading + 180, 1000)
            wp = tanker.add_waypoint(p, altitude, speed)

        wp.tasks.append(task.SetFrequencyCommand(frequency))

        if plane_type.tacan:
            channel = int(tacanchannel[:-1])
            modechannel = tacanchannel[-1]
            tanker.points[0].tasks.append(task.ActivateBeaconCommand(channel, modechannel))

        wp = tanker.add_waypoint(position, altitude, speed)
        wp.tasks.append(task.OrbitAction(altitude, speed, task.OrbitAction.OrbitPattern.RaceTrack))

        p = position.point_from_heading(heading, race_distance)
        tanker.add_waypoint(p, altitude, speed)

        return tanker

    def escort_flight(self,
                      _country,
                      name: str,
                      escort_type: planes.PlaneType,
                      airport: Optional[Airport],
                      group_to_escort: unitgroup.FlyingGroup,
                      start_type: StartType=StartType.Cold,
                      group_size=2):

        second_point_group = group_to_escort.points[1]
        if airport:
            eg = self.flight_group_from_airport(
                _country, name, escort_type, airport, task.Escort, start_type=start_type, group_size=group_size
            )
            eg.add_runway_waypoint(airport)
        else:
            eg = self.flight_group_inflight(
                _country, name, escort_type,
                mapping.Point(group_to_escort.points[0].position.x - 10 * 1000, group_to_escort.points[0].position.y),
                second_point_group.alt + 200,
                maintask=task.Escort,
                group_size=group_size
            )

        eg.add_waypoint(second_point_group.position, second_point_group.alt)
        eg.points[0].tasks.clear()
        eg.points[0].tasks.append(task.EscortTaskAction(group_to_escort.id, lastwpt=len(group_to_escort.points)))

        return eg

    def patrol_flight(self,
                      _country,
                      name: str,
                      patrol_type: planes.PlaneType,
                      airport: Optional[Airport],
                      pos1,
                      pos2,
                      start_type: StartType=StartType.Cold,
                      speed=600,
                      altitude=4000,
                      max_engage_distance=60*1000,
                      group_size=2):
        if airport:
            eg = self.flight_group_from_airport(
                _country, name, patrol_type, airport, maintask=task.CAP, start_type=start_type, group_size=group_size
            )
            eg.add_runway_waypoint(airport)
        else:
            eg = self.flight_group_inflight(
                _country, name, patrol_type,
                mapping.Point(pos1.x - 10 * 1000, pos1.y),
                altitude,
                maintask=task.CAP,
                group_size=group_size
            )
        eg.points[0].tasks.clear()
        eg.points[0].tasks.append(task.EngageTargets(max_engage_distance, [task.Targets.All.Air]))
        wp = eg.add_waypoint(pos1, altitude, speed)
        wp.tasks.append(task.OrbitAction(altitude, speed, task.OrbitAction.OrbitPattern.RaceTrack))
        eg.add_waypoint(pos2, altitude, speed)

        return eg

    def country(self, name):
        for k in self.coalition:
            c = self.coalition[k].country(name)
            if c:
                return c
        return None

    def find_group(self, group_name, search="exact"):
        for k in self.coalition:
            g = self.coalition[k].find_group(group_name, search)
            if g:
                return g
        return None

    def is_red(self, _country: Country):
        return _country.name in self.coalition["red"].countries

    def is_blue(self, _country: Country):
        return _country.name in self.coalition["blue"].countries

    def stats(self) -> Dict:
        d = {
            "red": {},
            "blue": {},
            "unit_count": 0,
            "count": 0
        }

        def count_group(field, group):
            d[col_name]["count"] += len(group)
            d[col_name][field]["count"] += len(group)
            for g in group:
                for u in g.units:
                    _unit = d[col_name][field]["units"].get(u.type, 0)
                    d[col_name][field]["units"][u.type] = _unit + 1
                    d[col_name]["unit_count"] += 1
            d[col_name][field]["unit_count"] = sum(d[col_name][field]["units"].values())

        for col_name in ["red", "blue"]:
            d[col_name]["unit_count"] = 0
            d[col_name]["count"] = 0
            col = self.coalition[col_name]
            d[col_name]["plane_groups"] = {"count": 0, "units": {}}
            d[col_name]["helicopter_groups"] = {"count": 0, "units": {}}
            d[col_name]["vehicle_groups"] = {"count": 0, "units": {}}
            d[col_name]["ship_groups"] = {"count": 0, "units": {}}
            for k, v in col.countries.items():
                count_group("plane_groups", v.plane_group)
                count_group("helicopter_groups", v.helicopter_group)
                count_group("vehicle_groups", v.vehicle_group)
                count_group("ship_groups", v.ship_group)
            d["unit_count"] += d[col_name]["unit_count"]
            d["count"] += d[col_name]["count"]

        # import pprint
        # pp = pprint.PrettyPrinter(indent=2)
        # pp.pprint(d)
        return d

    def print_stats(self, d):
        print("Mission Statistics")
        print(self.start_time.strftime("%d. %b %H:%M:%S"))
        print("-"*60)
        output = {"red": [], "blue": []}
        for x in ["Blue", "Red"]:
            low = x.lower()
            output[low].append("{group:<15s} groups units".format(group=x))
            output[low].append("{group:<15s} {gc:6d} {u:5d}".format(
                group="Plane",
                gc=d[low]["plane_groups"]["count"], u=d[low]["plane_groups"]["unit_count"]))
            output[low].append("{group:<15s} {gc:6d} {u:5d}".format(
                group="Helicopter",
                gc=d[low]["helicopter_groups"]["count"], u=d[low]["helicopter_groups"]["unit_count"]))
            output[low].append("{group:<15s} {gc:6d} {u:5d}".format(
                group="Vehicle",
                gc=d[low]["vehicle_groups"]["count"], u=d[low]["vehicle_groups"]["unit_count"]))
            output[low].append("{group:<15s} {gc:6d} {u:5d}".format(
                group="Ship",
                gc=d[low]["ship_groups"]["count"], u=d[low]["ship_groups"]["unit_count"]))
            output[low].append("-"*28)
            output[low].append("{group:<15s} {gc:6d} {u:5d}".format(group="Sum", gc=d[low]["count"], u=d[low]["unit_count"]))

        # merge tables
        for i in range(0, len(output["blue"])):
            print(output["blue"][i], "  ", output["red"][i])
        print("Total {g} groups with {u} units".format(g=d["count"], u=d["unit_count"]))

    def reload(self):
        if self.filename:
            return self.load_file(self.filename)
        raise RuntimeError("Currently no file loaded to reload.")

    def save(self, filename=None, show_stats=False):
        filename = self.filename if filename is None else filename
        if not filename:
            raise RuntimeError("No filename given.")
        self.filename = filename  # store filename

        with zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            # options
            zipf.writestr('options', str(self.options))

            # warehouses
            zipf.writestr('warehouses', str(self.warehouses))

            # translation files
            dicttext = lua.dumps(self.translation.dict('DEFAULT'), "dictionary", 1)
            zipf.writestr('l10n/DEFAULT/dictionary', dicttext)

            mapresource = self.map_resource.store(zipf, 'DEFAULT')
            # print(mapresource)
            zipf.writestr('l10n/DEFAULT/mapResource', lua.dumps(mapresource, "mapResource", 1))

            zipf.writestr('mission', str(self))

        if show_stats:
            self.print_stats(self.stats())
        return True

    def dict(self):
        m = {
            "trig": self.trig
        }
        m["start_time"] = self.start_time.timestamp() - 1306886400
        if m["start_time"] < 0:
            raise RuntimeError("Mission start time is < 0.")
        if self.season_from_start_time:
            self.weather.set_season_from_datetime(self.start_time)
        m["groundControl"] = self.groundControl.dict()
        m["usedModules"] = self.usedModules
        m["resourceCounter"] = self.resourceCounter
        m["triggers"] = self.triggers.dict()
        m["weather"] = self.weather.dict()
        m["theatre"] = self.terrain.name
        m["needModules"] = self.needModules
        m["map"] = self.map
        m["descriptionText"] = self._description_text.id
        m["pictureFileNameR"] = {}
        for i in range(0, len(self.pictureFileNameR)):
            m["pictureFileNameR"][i + 1] = self.pictureFileNameR[i]
        m["pictureFileNameB"] = {}
        for i in range(0, len(self.pictureFileNameB)):
            m["pictureFileNameB"][i + 1] = self.pictureFileNameB[i]
        m["descriptionBlueTask"] = self._description_bluetask.id
        m["descriptionRedTask"] = self._description_redtask.id
        m["trigrules"] = self.trigrules
        m["coalition"] = {}
        for col in self.coalition.keys():
            m["coalition"][col] = self.coalition[col].dict()
        col_blue = {self.coalition["blue"].country(x).id for x in self.coalition["blue"].countries.keys()}
        col_red = {self.coalition["red"].country(x).id for x in self.coalition["red"].countries.keys()}
        col_neutral = list(Mission.COUNTRY_IDS - col_blue - col_red)
        col_blue = list(col_blue)
        col_red = list(col_red)
        m["coalitions"] = {
            "neutral": {x + 1: col_neutral[x] for x in range(0, len(col_neutral))},
            "blue": {x + 1: col_blue[x] for x in range(0, len(col_blue))},
            "red": {x + 1: col_red[x] for x in range(0, len(col_red))}
        }
        m["sortie"] = self.sortie.id
        m["version"] = self.version
        m["goals"] = self.goals.dict()
        m["result"] = self.goals.generate_result()
        m["currentKey"] = self.currentKey
        m["maxDictId"] = self.current_dict_id
        m["forcedOptions"] = self.forced_options.dict()
        m["failures"] = self.failures

        return m

    def __str__(self):
        return lua.dumps(self.dict(), "mission", 1)

    def __repr__(self):
        rep = {"base": str(self), "options": self.options, "translation": self.translation}
        return repr(rep)


class MapResource:
    def __init__(self, mission: Mission):
        self.files = {}
        self.mission = mission

    def load_from_dict(self, _dict, zipf: zipfile.ZipFile, lang='DEFAULT'):
        _dict = _dict["mapResource"]

        for key in _dict:
            filename = _dict[key]
            extractedpath = zipf.extract('l10n/{lang}/{fn}'.format(lang=lang, fn=filename), tempfile.gettempdir())
            self.add_resource_file(extractedpath, lang, key)

    def add_resource_file(self, filepath, lang='DEFAULT', key=None):
        abspath = os.path.abspath(filepath)
        resource_key = key if key else "ResKey_" + str(self.mission.next_dict_id())
        if lang not in self.files:
            self.files[lang] = {}
        self.files[lang][abspath] = {
            "path": abspath,
            "reskey": resource_key
        }
        return resource_key

    def store(self, zipf: zipfile.ZipFile, lang='DEFAULT'):
        d = {}
        if lang in self.files:
            for x in self.files[lang]:
                mr = self.files[lang][x]
                filepath = mr["path"]
                if os.path.isabs(filepath):
                    nameinzip = os.path.basename(filepath)
                    zipf.write(filepath, "l10n/{lang}/{name}".format(lang=lang, name=nameinzip))
                    d[mr["reskey"]] = nameinzip

        return d
