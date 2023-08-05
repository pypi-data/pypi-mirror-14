# dcs python mission framework

dcs is a python framework for creating and editing mission files
from digital combat simulator.

Possible use cases are:

 * assisting mission creators
 * random mission creation
 * write an external mission editor on top of it
 * data export from existing missions
 * ...

## Sample

    m = dcs.mission.Mission()

    batumi = m.terrain.batumi()
    batumi.set_blue()

    usa = m.country("USA")
    m.awacs_flight(
       usa, "AWACS", dcs.planes.E_3A,
       batumi, dcs.Point(batumi.x + 20000, batumi.y + 80000),
       race_distance=120 * 1000, heading=90)

    m.save("sample.miz")

This code generates a mission with a AWACS flight starting cold from batumi.

## Install

    pip install pydcs

## TODO

 * Triggers are entirely missing
 * Failures
 * Forced options
 * Farps
 * Airgroup on ships


