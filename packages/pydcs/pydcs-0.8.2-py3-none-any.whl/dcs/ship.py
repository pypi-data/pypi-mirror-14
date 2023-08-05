from .unit import Unit


class Ship(Unit):
    def __init__(self, id=None, name=None, _type="speedboat"):
        super(Ship, self).__init__(id, name, _type)
        self.transportable = {"randomTransportable": False}

    def load_from_dict(self, d):
        super(Ship, self).load_from_dict(d)
        self.transportable = d["transportable"]

    def dict(self):
        d = super(Ship, self).dict()
        d["transportable"] = self.transportable
        return d
