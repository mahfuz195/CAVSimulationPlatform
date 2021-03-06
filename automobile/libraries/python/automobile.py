# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_automobile')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_automobile')
    _automobile = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_automobile', [dirname(__file__)])
        except ImportError:
            import _automobile
            return _automobile
        try:
            _mod = imp.load_module('_automobile', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _automobile = swig_import_helper()
    del swig_import_helper
else:
    import _automobile
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

import controller
class Driver(controller.Robot):
    __swig_setmethods__ = {}
    for _s in [controller.Robot]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Driver, name, value)
    __swig_getmethods__ = {}
    for _s in [controller.Robot]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Driver, name)
    __repr__ = _swig_repr
    INDICATOR_OFF = _automobile.Driver_INDICATOR_OFF
    INDICATOR_RIGHT = _automobile.Driver_INDICATOR_RIGHT
    INDICATOR_LEFT = _automobile.Driver_INDICATOR_LEFT
    SPEED = _automobile.Driver_SPEED
    TORQUE = _automobile.Driver_TORQUE
    DOWN = _automobile.Driver_DOWN
    SLOW = _automobile.Driver_SLOW
    NORMAL = _automobile.Driver_NORMAL
    FAST = _automobile.Driver_FAST

    def __init__(self):
        this = _automobile.new_Driver()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _automobile.delete_Driver
    __del__ = lambda self: None

    def step(self):
        return _automobile.Driver_step(self)

    def setSteeringAngle(self, steeringAngle):
        return _automobile.Driver_setSteeringAngle(self, steeringAngle)

    def getSteeringAngle(self):
        return _automobile.Driver_getSteeringAngle(self)

    def setCruisingSpeed(self, speed):
        return _automobile.Driver_setCruisingSpeed(self, speed)

    def getTargetCruisingSpeed(self):
        return _automobile.Driver_getTargetCruisingSpeed(self)

    def getCurrentSpeed(self):
        return _automobile.Driver_getCurrentSpeed(self)

    def setThrottle(self, throttle):
        return _automobile.Driver_setThrottle(self, throttle)

    def getThrottle(self):
        return _automobile.Driver_getThrottle(self)

    def setBrakeIntensity(self, intensity):
        return _automobile.Driver_setBrakeIntensity(self, intensity)

    def getBrakeIntensity(self):
        return _automobile.Driver_getBrakeIntensity(self)

    def setIndicator(self, state):
        return _automobile.Driver_setIndicator(self, state)

    def setHazardFlashers(self, state):
        return _automobile.Driver_setHazardFlashers(self, state)

    def getIndicator(self):
        return _automobile.Driver_getIndicator(self)

    def getHazardFlashers(self):
        return _automobile.Driver_getHazardFlashers(self)

    def setDippedBeams(self, state):
        return _automobile.Driver_setDippedBeams(self, state)

    def setAntifogLights(self, state):
        return _automobile.Driver_setAntifogLights(self, state)

    def getDippedBeams(self):
        return _automobile.Driver_getDippedBeams(self)

    def getAntifogLights(self):
        return _automobile.Driver_getAntifogLights(self)

    def getRpm(self):
        return _automobile.Driver_getRpm(self)

    def getGear(self):
        return _automobile.Driver_getGear(self)

    def setGear(self, gear):
        return _automobile.Driver_setGear(self, gear)

    def getGearNumber(self):
        return _automobile.Driver_getGearNumber(self)

    def getControlMode(self):
        return _automobile.Driver_getControlMode(self)

    def setWipersMode(self, mode):
        return _automobile.Driver_setWipersMode(self, mode)

    def getWipersMode(self):
        return _automobile.Driver_getWipersMode(self)

    def setBrake(self, brake):
        return _automobile.Driver_setBrake(self, brake)
Driver_swigregister = _automobile.Driver_swigregister
Driver_swigregister(Driver)

class Car(Driver):
    __swig_setmethods__ = {}
    for _s in [Driver]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Car, name, value)
    __swig_getmethods__ = {}
    for _s in [Driver]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Car, name)
    __repr__ = _swig_repr
    TRACTION = _automobile.Car_TRACTION
    PROPULSION = _automobile.Car_PROPULSION
    FOUR_BY_FOUR = _automobile.Car_FOUR_BY_FOUR
    COMBUTSION_ENGINE = _automobile.Car_COMBUTSION_ENGINE
    ELECTRIC_ENGINE = _automobile.Car_ELECTRIC_ENGINE
    PARALLEL_HYBRID_ENGINE = _automobile.Car_PARALLEL_HYBRID_ENGINE
    POWER_SPLIT_HYBRID_ENGINE = _automobile.Car_POWER_SPLIT_HYBRID_ENGINE
    WHEEL_FRONT_RIGHT = _automobile.Car_WHEEL_FRONT_RIGHT
    WHEEL_FRONT_LEFT = _automobile.Car_WHEEL_FRONT_LEFT
    WHEEL_REAR_RIGHT = _automobile.Car_WHEEL_REAR_RIGHT
    WHEEL_REAR_LEFT = _automobile.Car_WHEEL_REAR_LEFT
    WHEEL_NB = _automobile.Car_WHEEL_NB

    def __init__(self):
        this = _automobile.new_Car()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _automobile.delete_Car
    __del__ = lambda self: None

    def getType(self):
        return _automobile.Car_getType(self)

    def getEngineType(self):
        return _automobile.Car_getEngineType(self)

    def setIndicatorPeriod(self, period):
        return _automobile.Car_setIndicatorPeriod(self, period)

    def getIndicatorPeriod(self):
        return _automobile.Car_getIndicatorPeriod(self)

    def getBackwardsLights(self):
        return _automobile.Car_getBackwardsLights(self)

    def getBrakeLights(self):
        return _automobile.Car_getBrakeLights(self)

    def getTrackFront(self):
        return _automobile.Car_getTrackFront(self)

    def getTrackRear(self):
        return _automobile.Car_getTrackRear(self)

    def getWheelbase(self):
        return _automobile.Car_getWheelbase(self)

    def getFrontWheelRadius(self):
        return _automobile.Car_getFrontWheelRadius(self)

    def getRearWheelRadius(self):
        return _automobile.Car_getRearWheelRadius(self)

    def getWheelEncoder(self, wheel):
        return _automobile.Car_getWheelEncoder(self, wheel)

    def getWheelSpeed(self, wheel):
        return _automobile.Car_getWheelSpeed(self, wheel)

    def getRightSteeringAngle(self):
        return _automobile.Car_getRightSteeringAngle(self)

    def getLeftSteeringAngle(self):
        return _automobile.Car_getLeftSteeringAngle(self)

    def enableLimitedSlipDifferential(self, enable):
        return _automobile.Car_enableLimitedSlipDifferential(self, enable)

    def enableIndicatorAutoDisabling(self, enable):
        return _automobile.Car_enableIndicatorAutoDisabling(self, enable)
Car_swigregister = _automobile.Car_swigregister
Car_swigregister(Car)

# This file is compatible with both classic and new-style classes.


