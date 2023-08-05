from .unit import FlyingUnit
from .planes import PlaneType, A_10C


class Plane(FlyingUnit):
    def __init__(self, _id=None, name=None, _type: PlaneType=A_10C, _country=None):
        super(Plane, self).__init__(_id, name, _type, _country)
