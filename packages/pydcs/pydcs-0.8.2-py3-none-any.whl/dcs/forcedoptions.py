from enum import Enum


class ForcedOptions:

    class Views(Enum):
        OnlyMap = "optview_onlymap"
        MyAircraft = "optview_myaircraft"
        Allies = "optview_allies"
        OnlyAllies = "optview_onlyallies"
        All = "optview_all"

    class CivilTraffic(Enum):
        Off = ""
        Low = "low"
        Medium = "medium"
        High = "high"

    class GEffect(Enum):
        None_ = ""
        Game = "game"
        Realistic = "realistic"

    def __init__(self):
        self.fuel = None
        self.easy_radar = None
        self.mini_hud = None
        self.accidental_failures = None
        self.options_view = None  # type: ForcedOptions.Views
        self.permit_crash = None
        self.immportal = None
        self.easy_communication = None
        self.cockpit_visual_recon_mode = None
        self.easy_flight = None
        self.radio = None
        self.tips = None
        self.geffect = None
        self.external_views = None
        self.birds = None
        self.civil_traffic = None  # type: ForcedOptions.CivilTraffic
        self.weapons = None
        self.padlock = None
        self.scenes = None
        self.labels = None

    def load_from_dict(self, d):
        self.fuel = d.get("fuel")
        self.easy_radar = d.get("easyRadar")
        self.mini_hud = d.get("miniHUD")
        self.accidental_failures = d.get("accidental_failures")
        if d.get("optionsView"):
            self.options_view = ForcedOptions.Views(d["optionsView"])
        self.permit_crash = d.get("permitCrash")
        self.immportal = d.get("immortal")
        self.easy_communication = d.get("easyCommunication")
        self.cockpit_visual_recon_mode = d.get("cockpitVisualRM")
        self.easy_flight = d.get("easyFlight")
        self.radio = d.get("radio")
        self.tips = d.get("tips")
        if d.get("geffect"):
            self.geffect = ForcedOptions.GEffect(d["geffect"])
        self.external_views = d.get("externalViews")
        self.birds = d.get("birds")
        if d.get("civTraffic"):
            self.civil_traffic = ForcedOptions.CivilTraffic(d["civTraffic"])
        self.weapons = d.get("weapons")
        self.padlock = d.get("padlock")
        self.labels = d.get("labels")
        self.scenes = d.get("scenes")

    def dict(self):
        d = {}
        if self.fuel:
            d["fuel"] = self.fuel
        if self.easy_radar:
            d["easyRadar"] = self.easy_radar
        if self.mini_hud:
            d["miniHUD"] = self.mini_hud
        if self.accidental_failures:
            d["accidental_failures"] = self.accidental_failures
        if self.options_view:
            d["optionsView"] = self.options_view.value
        if self.permit_crash:
            d["permitCrash"] = self.permit_crash
        if self.immportal:
            d["immortal"] = self.immportal
        if self.easy_communication:
            d["easyCommunication"] = self.easy_communication
        if self.cockpit_visual_recon_mode:
            d["cockpitVisualRM"] = self.cockpit_visual_recon_mode
        if self.easy_flight:
            d["easyFlight"] = self.easy_flight
        if self.radio:
            d["radio"] = self.radio
        if self.tips:
            d["tips"] = self.tips
        if self.geffect:
            d["geffect"] = self.geffect.value
        if self.external_views:
            d["externalViews"] = self.external_views
        if self.birds:
            d["birds"] = self.birds
        if self.civil_traffic:
            d["civTraffic"] = self.civil_traffic.value
        if self.weapons:
            d["weapons"] = self.weapons
        if self.padlock:
            d["padlock"] = self.padlock
        if self.labels:
            d["labels"] = self.labels
        if self.scenes:
            d["scenes"] = self.scenes
        return d
