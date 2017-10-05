# Description: Vehicle and TrafficLight classes

from controller import Node, Field
import math
import random

hiddenPosition = 10000

CAR_MODEL = [
    'BmwX5Simple',
    'CitroenCZeroSimple',
    'ToyotaPriusSimple',
    'LincolnMKZSimple',
    'RangeRoverSportSVRSimple'
]
BUS_MODEL = ['BusSimple']
WHEEL_RADIUS = {
    'BmwX5Simple': 0.374,
    'CitroenCZeroSimple': 0.285,
    'ToyotaPriusSimple': 0.317,
    'LincolnMKZSimple': 0.358,
    'RangeRoverSportSVRSimple': 0.358,
    'BusSimple': 0.56
}

COLORS = [
    '0.43 0.11 0.1',
    '0.85 0.85 0.05',
    '0.10 0.15 0.18',
    '0.14 0.29 0.16',
    '0.18 0.28 0.64',
    '0.62 0.62 0.62',
    '0.72 0.52 0.18',
    '0.18 0.50 0.72'
]

class Vehicle:
    def __init__(self, node):
        self.node        = node
        self.translation = self.node.getField("translation")
        self.rotation    = self.node.getField("rotation")
        self.name        = self.node.getField("name")
        self.frontRightWheelAngularVelocity = self.node.getField("frontRightWheelAngularVelocity")
        self.frontLeftWheelAngularVelocity  = self.node.getField("frontLeftWheelAngularVelocity")
        self.rearRightWheelAngularVelocity  = self.node.getField("rearRightWheelAngularVelocity")
        self.rearLeftWheelAngularVelocity   = self.node.getField("rearLeftWheelAngularVelocity")
        self.inUse           = False
        self.currentID       = ""
        self.currentPos      = [hiddenPosition, 0.5, 0]
        self.currentRot      = [0, 1, 0, 0]
        self.currentAngles   = [0, 0, 0]
        self.targetPos       = [hiddenPosition, 0.5, 0]
        self.targetRot       = [0, 1, 0, 0]
        self.currentAngles   = [0, 0, 0]
        self.roll            = 0
        self.pitch           = 0
        self.speed           = 0
        self.type            = self.node.getTypeName()
        self.wheelRadius     = WHEEL_RADIUS[self.type]
        if self.type in CAR_MODEL:
            self.vehicleClass = 'car'
        elif self.type in BUS_MODEL:
            self.vehicleClass = 'bus'
        else:
            print "Vehicle type not supported: " + self.type

    @staticmethod
    def generate_vehicle_string(index, vehicleClass):
        # randomly select the model
        if vehicleClass == 'bus':
            model = BUS_MODEL[0]
        else:
            modelIndex = math.trunc(random.uniform(0, len(CAR_MODEL)))
            model = CAR_MODEL[modelIndex]
        colorIndex = math.trunc(random.uniform(0, len(COLORS)))
        defName = "SUMO_VEHICLE%d" % index
        vehicleString = "#VRML_OBJ V8.6 utf8\n"
        vehicleString += "DEF " + defName + " " + model + " {\n"
        vehicleString += "  translation 10000 0.5 0\n"
        vehicleString += "  color " + COLORS[colorIndex] + "\n"
        vehicleString += "  recognitionColors [ " + COLORS[colorIndex] + " ]\n"
        vehicleString += "}\n"
        return vehicleString, defName

    @staticmethod
    def get_corresponding_vehicle_class(vehicleClass):
        if vehicleClass == 'bus':
            return 'bus'
        else:
            return 'car'

    @staticmethod
    def get_car_models_list():
        return CAR_MODEL

    @staticmethod
    def get_bus_models_list():
        return BUS_MODEL


class TrafficLight:
    def __init__(self):
        self.lightNumber = 0  # In SUMO a traffic light is a set of real traffic light
        self.previousState = ""
        self.LED = {}
        self.trafficLightRecognitionColors = {}
