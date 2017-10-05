# Description: SumoSupervisor class inheriting from Supervisor

from controller import Robot, LED, Supervisor, Node, Field
from Objects import Vehicle, TrafficLight
from WebotsVehicle import WebotsVehicle
from SumoDisplay import SumoDisplay

import os
import sys
import math

hiddenPosition = 10000


def rotation_from_yaw_pitch_roll(yaw, pitch, roll):
    rotation = [0, 1, 0, 0]
    # construct rotation matrix
    # a b c
    # d e f
    # g h i
    a = math.cos(roll) * math.cos(yaw)
    b = -math.sin(roll)
    c = math.cos(roll) * math.sin(yaw)
    d = math.sin(roll) * math.cos(yaw) * math.cos(pitch) + math.sin(yaw) * math.sin(pitch)
    e = math.cos(roll) * math.cos(pitch)
    f = math.sin(roll) * math.sin(yaw) * math.cos(pitch) - math.cos(yaw) * math.sin(pitch)
    g = math.sin(roll) * math.cos(yaw) * math.sin(pitch) - math.sin(yaw) * math.cos(pitch)
    h = math.cos(roll) * math.sin(pitch)
    i = math.sin(roll) * math.sin(yaw) * math.sin(pitch) + math.cos(yaw) * math.cos(pitch)
    # convert it to rotation vector
    cosAngle = 0.5 * (a + e + i - 1.0)
    if math.fabs(cosAngle) > 1:
        return rotation
    else:
        rotation[0] = f - h
        rotation[1] = g - c
        rotation[2] = b - d
        rotation[3] = math.acos(cosAngle)
        # normalize vector
        length = math.sqrt(rotation[0] * rotation[0] + rotation[1] * rotation[1] + rotation[2] * rotation[2])
        if length != 0:
            rotation[0] = rotation[0] / length
            rotation[1] = rotation[1] / length
            rotation[2] = rotation[2] / length
        if rotation[0] == 0 and rotation[1] == 0 and rotation[2] == 0:
            return [0, 1, 0, 0]
        else:
            return rotation


class SumoSupervisor (Supervisor):
    def get_viewpoint_position_field(self):
        children = self.getRoot().getField("children")
        number = children.getCount()
        for i in range(0, number):
            node = children.getMFNode(i)
            if node.getType() == Node.VIEWPOINT:
                return node.getField("position")
        return None

    def get_initial_vehicles(self):
        for i in range(0, self.vehiclesLimit):
            defName = "SUMO_VEHICLE%d" % self.vehicleNumber
            node = self.getFromDef(defName)
            if node:
                self.vehicles[i] = Vehicle(node)
                self.vehicleNumber += 1
            else:
                break
        for i in range(0, self.vehiclesLimit):
            defName = "WEBOTS_VEHICLE%d" % self.webotsVehicleNumber
            node = self.getFromDef(defName)
            if node:
                self.webotsVehicles[i] = WebotsVehicle(node, self.webotsVehicleNumber)
                self.webotsVehicleNumber += 1
            else:
                break

    def generate_new_vehicle(self, vehicleClass):
        # load the new vehicle
        vehicleString, defName = Vehicle.generate_vehicle_string(self.vehicleNumber, vehicleClass)
        self.rootChildren.importMFNodeFromString(-1, vehicleString)
        self.vehicles[self.vehicleNumber] = Vehicle(self.getFromDef(defName))
        self.vehicleNumber += 1

    def get_vehicle_index(self, id, generateIfneeded=True):
        for i in range(0, self.vehicleNumber):
            if self.vehicles[i].currentID == id:
                # the vehicle was already here at last step
                return i
        # the vehicle was not present last step
        # check if a corresponding vehicle is already in the simulation
        node = self.getFromDef(id)
        if node and (node.getTypeName() in Vehicle.get_car_models_list() or node.getTypeName() in Vehicle.get_bus_models_list()):
            self.vehicles[self.vehicleNumber] = Vehicle(node)
            self.vehicleNumber += 1
            return (self.vehicleNumber - 1)
        # check if a vehicle is available
        vehicleClass = self.get_vehicle_class(id)
        for i in range(0, self.vehicleNumber):
            if not self.vehicles[i].inUse and self.vehicles[i].vehicleClass == vehicleClass:
                # if a vehicle is available assign it to this id
                self.vehicles[i].currentID = id
                self.vehicles[i].name.setSFString(id)
                return i
        # no vehicle available => generate a new one if limit is not reached
        if generateIfneeded and (self.vehicleNumber < self.vehiclesLimit):
            vehicleClass = self.get_vehicle_class(id)
            self.generate_new_vehicle(vehicleClass)
            return (self.vehicleNumber - 1)
        else:
            return -1

    def get_vehicle_class(self, id):
        if id in self.vehiclesClass:
            return self.vehiclesClass[id]
        else:
            vehicleClass = Vehicle.get_corresponding_vehicle_class(self.traci.vehicle.getVehicleClass(id))
            self.vehiclesClass[id] = vehicleClass
            return vehicleClass

    def disable_unused_vehicles(self, subscriptionResult):
        IDlist = subscriptionResult.keys()
        for i in range(0, self.vehicleNumber):
            if self.vehicles[i].inUse:
                if self.vehicles[i].currentID not in IDlist:
                    self.vehicles[i].inUse = False
                    self.vehicles[i].name.setSFString("")

    def hide_unused_vehicles(self):
        for i in range(0, self.vehicleNumber):
            if not self.vehicles[i].inUse:
                if self.vehicles[i].targetPos != [hiddenPosition, 0.5, i * 10] and self.vehicles[i].targetRot != [0, 1, 0, 0]:
                    self.vehicles[i].targetPos     = [hiddenPosition, 0.5, i * 10]
                    self.vehicles[i].currentPos    = [hiddenPosition, 0.5, i * 10]
                    self.vehicles[i].currentRot    = [0, 1, 0, 0]
                    self.vehicles[i].targetRot     = [0, 1, 0, 0]
                    self.vehicles[i].currentAngles = [0, 0, 0]
                    self.vehicles[i].targetAngles  = [0, 0, 0]
                    self.vehicles[i].translation.setSFVec3f([hiddenPosition, 0.5, i * 10])
                    self.vehicles[i].node.setVelocity([0, 0, 0, 0, 0, 0])
                    self.vehicles[i].frontRightWheelAngularVelocity.setSFVec3f([0, 0, 0])
                    self.vehicles[i].frontLeftWheelAngularVelocity.setSFVec3f([0, 0, 0])
                    self.vehicles[i].rearRightWheelAngularVelocity.setSFVec3f([0, 0, 0])
                    self.vehicles[i].rearLeftWheelAngularVelocity.setSFVec3f([0, 0, 0])

    def stop_all_vehicles(self):
        for i in range(0, self.vehicleNumber):
            self.vehicles[i].node.setVelocity([0, 0, 0, 0, 0, 0])
            self.vehicles[i].frontRightWheelAngularVelocity.setSFVec3f([0, 0, 0])
            self.vehicles[i].frontLeftWheelAngularVelocity.setSFVec3f([0, 0, 0])
            self.vehicles[i].rearRightWheelAngularVelocity.setSFVec3f([0, 0, 0])
            self.vehicles[i].rearLeftWheelAngularVelocity.setSFVec3f([0, 0, 0])

    def get_vehicles_position(self, subscriptionResult, xOffset, yOffset):
        for id in subscriptionResult.keys():
            height = 0.4
            roll = 0.0
            pitch = 0.0
            sumoPos   = subscriptionResult[id][self.traci.constants.VAR_POSITION]
            sumoAngle = subscriptionResult[id][self.traci.constants.VAR_ANGLE]
            pos   = [-sumoPos[0] + xOffset, height, sumoPos[1] - yOffset]
            angle = math.pi * sumoAngle / 180
            dx    = -math.cos(angle)
            dy    = -math.sin(angle)
            yaw   = -math.atan2(dy, -dx)
            # correct position (origin of the car is not the same in Webots / sumo)
            pos[0] = pos[0] + 0.5 * subscriptionResult[id][self.traci.constants.VAR_LENGTH] * math.sin(angle)
            pos[2] = pos[2] - 0.5 * subscriptionResult[id][self.traci.constants.VAR_LENGTH] * math.cos(angle)
            # if needed check the vehicle is in the visibility radius
            if self.radius > 0:
                viewpointPosition = self.viewpointPosition.getSFVec3f()
                xDiff = viewpointPosition[0] - pos[0]
                yDiff = viewpointPosition[1]
                zDiff = viewpointPosition[2] - pos[2]
                distance = math.sqrt(xDiff * xDiff + yDiff * yDiff + zDiff * zDiff)
                if distance > self.radius:
                    index = self.get_vehicle_index(id, generateIfneeded=False)
                    if index >= 0:
                        self.vehicles[index].inUse = False
                        self.vehicles[index].name.setSFString("")
                    continue
            index = self.get_vehicle_index(id)
            if index >= 0:
                height = self.vehicles[index].wheelRadius
                if self.enableHeight:
                    roadID = subscriptionResult[id][self.traci.constants.VAR_ROAD_ID]
                    roadPos = subscriptionResult[id][self.traci.constants.VAR_LANEPOSITION]
                    if roadID.startswith(":"):
                        # this is a lane change it does not contains edge information
                        # in that case, use previous height, roll and pitch
                        height = self.vehicles[index].currentPos[1]
                        roll = self.vehicles[index].roll
                        pitch = self.vehicles[index].pitch
                    else:
                        tags = roadID.split('_')
                        del tags[0]  # remove the first one which is the 'id' of the road
                        for tag in tags:
                            if tag.startswith('height'):
                                height = height + float(tag.split('height', 1)[1])
                            elif tag.startswith('roll'):
                                roll = float(tag.split('roll', 1)[1])
                            elif tag.startswith('pitch'):
                                pitch = float(tag.split('pitch', 1)[1])
                        self.vehicles[index].pitch = pitch
                        self.vehicles[index].roll = roll
                        # ajust height according to the pitch
                        if not pitch == 0:
                            height = height + roadPos * math.sin(pitch)
                        # ajust height according to the roll and lateral position of the vehicle
                        if not roll == 0.0:
                            laneIndex = subscriptionResult[id][self.traci.constants.VAR_LANE_INDEX]
                            laneID = subscriptionResult[id][self.traci.constants.VAR_LANE_ID]
                            laneWidth = self.traci.lane.getWidth(laneID)
                            edge = self.net.getEdge(roadID)
                            numberOfLane = edge.getLaneNumber()
                            # compute lateral distance from the center of the lane
                            distance = math.fabs((laneIndex - numberOfLane / 2) + 0.5) * laneWidth
                            if laneIndex >= (numberOfLane/2):
                                height = height - distance * math.sin(roll)
                            else:
                                height = height + distance * math.sin(roll)
                pos[1] = height
                rot = rotation_from_yaw_pitch_roll(yaw, pitch, roll)
                if not self.vehicles[index].inUse:
                    # this vehicle was previously not used, move it directly to the correct initial location
                    self.vehicles[index].inUse = True
                    self.vehicles[index].currentPos    = pos
                    self.vehicles[index].currentRot    = rot
                    self.vehicles[index].currentAngles = [roll, yaw, pitch]
                else:
                    self.vehicles[index].currentPos    = self.vehicles[index].targetPos
                    self.vehicles[index].currentRot    = self.vehicles[index].targetRot
                    self.vehicles[index].currentAngles = self.vehicles[index].targetAngles
                self.vehicles[index].targetPos    = pos
                self.vehicles[index].targetRot    = rot
                self.vehicles[index].targetAngles = [roll, yaw, pitch]
                if self.traci.constants.VAR_SPEED in subscriptionResult[id]:
                    self.vehicles[index].speed = subscriptionResult[id][self.traci.constants.VAR_SPEED]

    def update_vehicles_position_and_velocity(self, step, rotateWheels):
        for i in range(0, self.vehicleNumber):
            if self.vehicles[i].inUse:
                self.vehicles[i].translation.setSFVec3f(self.vehicles[i].currentPos)
                self.vehicles[i].rotation.setSFRotation(self.vehicles[i].currentRot)
                velocity = []
                velocity.append(self.vehicles[i].targetPos[0] - self.vehicles[i].currentPos[0])
                velocity.append(self.vehicles[i].targetPos[1] - self.vehicles[i].currentPos[1])
                velocity.append(self.vehicles[i].targetPos[2] - self.vehicles[i].currentPos[2])
                for j in range(0, 3):
                    diffAngle = self.vehicles[i].currentAngles[j] - self.vehicles[i].targetAngles[j]
                    if diffAngle > math.pi:
                        diffAngle = diffAngle - 2 * math.pi
                    elif diffAngle < -math.pi:
                        diffAngle = diffAngle + 2 * math.pi
                    velocity.append(diffAngle)
                velocity[:] = [1000 * x / step for x in velocity]
                self.vehicles[i].node.setVelocity(velocity)
                if rotateWheels:
                    angularVelocity = [self.vehicles[i].speed / self.vehicles[i].wheelRadius, 0, 0]
                    self.vehicles[i].frontRightWheelAngularVelocity.setSFVec3f(angularVelocity)
                    self.vehicles[i].frontLeftWheelAngularVelocity.setSFVec3f(angularVelocity)
                    self.vehicles[i].rearRightWheelAngularVelocity.setSFVec3f(angularVelocity)
                    self.vehicles[i].rearLeftWheelAngularVelocity.setSFVec3f(angularVelocity)

    def update_webots_vehicles(self, xOffset, yOffset):
        for i in range(0, self.webotsVehicleNumber):
            if self.webotsVehicles[i].is_on_road(xOffset, yOffset, self.maxWebotsVehicleDistanceToLane, self.net):
                self.webotsVehicles[i].update_position(self.getTime(), self.net, self.traci, self.sumolib, xOffset, yOffset)
            else:
                # the controlled vehicle is not on any road
                # => we remove it from sumo network
                if self.webotsVehicles[i].name in self.traci.vehicle.getIDList():
                    self.traci.vehicle.remove(self.webotsVehicles[i].name)

    def get_traffic_light(self, IDlist):
        self.trafficLightNumber = len(IDlist)
        self.trafficLights = {}
        LEDNames = []
        for i in range(0, self.getNumberOfDevices()):
            device = self.getDeviceByIndex(i)
            if device.getNodeType() == Node.LED:
                LEDNames.append(device.getName())
        for i in range(0, self.trafficLightNumber):
            id = IDlist[i]
            self.trafficLights[id] = TrafficLight()
            self.trafficLights[id].lightNumber = len(self.traci.trafficlights.getRedYellowGreenState(id))
            for j in range(0, self.trafficLights[id].lightNumber):
                trafficLightNode = self.getFromDef("TLS_" + id + "_" + str(j))
                if trafficLightNode is not None:
                    self.trafficLights[id].trafficLightRecognitionColors[j] = trafficLightNode.getField("recognitionColors")
                ledName = id + "_" + str(j) + "_"
                if (ledName + "r") in LEDNames:
                    self.trafficLights[id].LED[3*j + 0] = self.getLED(ledName + "r")
                else:
                    self.trafficLights[id].LED[3*j + 0] = None
                if (ledName + "y") in LEDNames:
                    self.trafficLights[id].LED[3*j + 1] = self.getLED(ledName + "y")
                else:
                    self.trafficLights[id].LED[3*j + 1] = None
                if (ledName + "g") in LEDNames:
                    self.trafficLights[id].LED[3*j + 2] = self.getLED(ledName + "g")
                else:
                    self.trafficLights[id].LED[3*j + 2] = None

    def update_traffic_light_state(self, subscriptionResult):
        for id in subscriptionResult.keys():
            currentState = subscriptionResult[id][self.traci.constants.TL_RED_YELLOW_GREEN_STATE]
            # update light LED state if traffic light state has changed
            if self.trafficLights[id].previousState != currentState:
                self.trafficLights[id].previousState = currentState
                for j in range(0, self.trafficLights[id].lightNumber):
                    # Update red LED if it exists
                    if self.trafficLights[id].LED[3*j + 0]:
                        if currentState[j] == 'r' or currentState[j] == 'R':
                            self.trafficLights[id].LED[3*j + 0].set(1)
                            # update recognition colors
                            if j in self.trafficLights[id].trafficLightRecognitionColors:
                                self.trafficLights[id].trafficLightRecognitionColors[j].setMFColor(1, [1, 0, 0])
                        else:
                            self.trafficLights[id].LED[3*j + 0].set(0)
                    # Update yellow LED if it exists
                    if self.trafficLights[id].LED[3*j + 1]:
                        if currentState[j] == 'y' or currentState[j] == 'Y':
                            self.trafficLights[id].LED[3*j + 1].set(1)
                            # update recognition colors
                            if j in self.trafficLights[id].trafficLightRecognitionColors:
                                self.trafficLights[id].trafficLightRecognitionColors[j].setMFColor(1, [1, 0.5, 0])
                        else:
                            self.trafficLights[id].LED[3*j + 1].set(0)
                    # Update green LED if it exists
                    if self.trafficLights[id].LED[3*j + 2]:
                        if currentState[j] == 'g' or currentState[j] == 'G':
                            self.trafficLights[id].LED[3*j + 2].set(1)
                            # update recognition colors
                            if j in self.trafficLights[id].trafficLightRecognitionColors:
                                self.trafficLights[id].trafficLightRecognitionColors[j].setMFColor(1, [0, 1, 0])
                        else:
                            self.trafficLights[id].LED[3*j + 2].set(0)

    def run(self, port, disableTrafficLight, directory, step, rotateWheels, maxVehicles, radius, enableHeight, useDisplay, displayRefreshRate, displayZoom, displayFitSize, traci, sumolib):
        try:
            traci.init(port)
        except:
            sys.exit("Unable to connect to SUMO, please make sure any previous instance of SUMO is closed.\n You can try changing SUMO port using the '--port' argument.")

        self.traci   = traci
        self.sumolib = sumolib
        self.radius  = radius
        self.enableHeight = enableHeight
        self.sumoClosed = False
        self.temporaryDirectory = directory
        self.rootChildren = self.getRoot().getField("children")
        self.viewpointPosition = self.get_viewpoint_position_field()
        self.maxWebotsVehicleDistanceToLane = 5
        self.webotsVehicleNumber = 0
        self.webotsVehicles = {}
        self.vehicleNumber = 0
        self.vehicles = {}
        self.vehiclesLimit = maxVehicles
        self.vehiclesClass = {}

        # get sumo vehicles already present in the world
        self.get_initial_vehicles()

        # parse the net and get the offsets
        self.net = sumolib.net.readNet((directory + "/sumo.net.xml").replace('/', os.sep))
        xOffset = self.net.getLocationOffset()[0]
        yOffset = self.net.getLocationOffset()[1]

        # Load plugin to the generic SUMO Supervisor (if any)
        self.usePlugin = False
        if os.path.exists((directory + "/plugin.py").replace('/', os.sep)):
            self.usePlugin = True
            sys.path.append(directory)
            import plugin
            sumoSupervisorPlugin = plugin.SumoSupervisorPlugin(self, self.traci, self.net)

        # Get all the LEDs of the traffic lights
        if not disableTrafficLight:
            trafficLightsList = self.traci.trafficlights.getIDList()
            self.get_traffic_light(trafficLightsList)
            for id in trafficLightsList:
                # subscribe to traffic lights state
                self.traci.trafficlights.subscribe(id, [self.traci.constants.TL_RED_YELLOW_GREEN_STATE])

        # Subscribe to new vehicles entering the simulation
        self.traci.simulation.subscribe([self.traci.constants.VAR_DEPARTED_VEHICLES_IDS, self.traci.constants.VAR_MIN_EXPECTED_VEHICLES])

        # Create the vehicle variable subscription list
        self.vehicleVariableList = [self.traci.constants.VAR_POSITION, self.traci.constants.VAR_ANGLE, self.traci.constants.VAR_LENGTH]
        if rotateWheels:
            self.vehicleVariableList.append(self.traci.constants.VAR_SPEED)
        if enableHeight:
            self.vehicleVariableList.extend([self.traci.constants.VAR_ROAD_ID, self.traci.constants.VAR_LANEPOSITION, self.traci.constants.VAR_LANE_INDEX, self.traci.constants.VAR_LANE_ID])

        # create the SUMO display
        self.sumoDisplay = None
        if useDisplay:
            view = self.traci.gui.getIDList()[0]
            display = self.getDisplay('sumo')
            if display is not None:
                self.sumoDisplay = SumoDisplay(display, displayZoom, view, directory, displayRefreshRate, displayFitSize, self.traci)

        # Main simulation loop
        while self.step(step) >= 0:
            if self.usePlugin:
                sumoSupervisorPlugin.run(step)

            if self.sumoDisplay is not None:
                self.sumoDisplay.step(step)

            # try to perform a SUMO step, if it fails it means SUMO has been closed by the user
            try:
                self.traci.simulationStep()
            except self.traci.exceptions.FatalTraCIError:
                print "Sumo closed"
                self.sumoClosed = True
                break

            result = self.traci.simulation.getSubscriptionResults()

            # SUMO simulation over (no more vehicle are expected)
            if result[self.traci.constants.VAR_MIN_EXPECTED_VEHICLES] == 0:
                break

            # subscribe to new vehicle
            for id in result[self.traci.constants.VAR_DEPARTED_VEHICLES_IDS]:
                if not id.startswith("webotsVehicle"):
                    self.traci.vehicle.subscribe(id, self.vehicleVariableList)
                elif self.sumoDisplay is not None and len(self.webotsVehicles) == 1:
                    # Only one vehicle controlled by Webots => center the view on it
                    self.traci.gui.trackVehicle(view, 'webotsVehicle0')

            # get result from the vehicle subscription and apply it
            subscriptionResult = self.traci.vehicle.getSubscriptionResults()
            self.get_vehicles_position(subscriptionResult, xOffset, yOffset)
            self.disable_unused_vehicles(subscriptionResult)

            # hide unused vehicles
            self.hide_unused_vehicles()

            if not disableTrafficLight:
                self.update_traffic_light_state(self.traci.trafficlights.getSubscriptionResults())

            self.update_vehicles_position_and_velocity(step, rotateWheels)
            self.update_webots_vehicles(xOffset, yOffset)

        if not self.sumoClosed:
            self.traci.close()
        else:
            self.stop_all_vehicles()
        sys.stdout.flush()
