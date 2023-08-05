from .unit import FlyingUnit
from .helicopters import HelicopterType, Ka_50


class Helicopter(FlyingUnit):
    def __init__(self, _id=None, name=None, _type: HelicopterType=Ka_50, _country=None):
        super(Helicopter, self).__init__(_id, name, _type, _country)
        self.rope_length = 15

    def load_from_dict(self, d):
        super(Helicopter, self).load_from_dict(d)
        self.rope_length = d["ropeLength"]

    def dict(self):
        d = super(Helicopter, self).dict()
        d["ropeLength"] = self.rope_length
        return d
