# Description: WebotsVehicle class (used to close the loop with SUMO)

import math


class WebotsVehicle:
    def __init__(self, node, id):
        self.previousPosition = [0, 0, 0]
        self.vehicleLength = 6
        self.vehicleHeight = 0.4
        self.node = node
        self.name = "webotsVehicle%d" % id

    def get_position(self, xOffset, yOffset):
        # get position
        position = self.node.getPosition()
        matrix = self.node.getOrientation()
        angle1 = math.acos(matrix[8])
        angle2 = math.atan(-matrix[6] / (math.sqrt(math.pow(matrix[7], 2) + math.pow(matrix[8], 2))))
        if angle2 < 0:
            angle1 = -angle1
        # compute position in sumo coordinate frame
        position[0] = -position[0] + xOffset - 0.5 * self.vehicleLength * math.sin(angle1)
        position[1] =  position[1] - self.vehicleHeight
        position[2] =  position[2] + yOffset + 0.5 * self.vehicleLength * math.cos(angle1)
        return position

    def get_angle(self):
        # get pitch angle
        matrix = self.node.getOrientation()
        angle1 = math.acos(matrix[8])
        angle2 = math.atan(-matrix[6] / (math.sqrt(math.pow(matrix[7], 2) + math.pow(matrix[8], 2))))
        angle = angle1
        if angle2 > 0:
            angle = -angle1
        return angle

    def is_on_road(self, xOffset, yOffset, maxDistance, net):
        # get position
        self.currentPosition = self.get_position(xOffset, yOffset)
        # get pitch angle
        self.angle = self.get_angle()

        # get all the edges in a radius of 5 meters from the vehicle position
        edges = net.getNeighboringEdges(self.currentPosition[0], self.currentPosition[2], maxDistance, False)
        # remove edges starting by ':' (internal edge of SUMO)
        for i in range(len(edges)-1, -1, -1):
            if (edges[i][0]).getID().startswith(":"):
                edges.pop([i])

        # find the closest edge
        if len(edges) > 0:
            # correct distance using the third dimension
            for i in range(0, len(edges)):
                edge = (edges[i][0]).getID()
                # get height of this edge
                height = 0.0
                tags = edge.split('_')
                del tags[0]  # remove first which is the 'id' of the edge
                for tag in tags:
                    if tag.startswith('height'):
                        height = float(tag.split('height', 1)[1])
                newDist = math.sqrt(math.pow(edges[i][1], 2) + math.pow(self.currentPosition[1] - height, 2))
                edges[i] = (edges[i][0], newDist)

            # sort edges by distances to get the closest one
            self.currentDistancesToEdges = sorted([(dist, edge) for edge, dist in edges])
            if self.currentDistancesToEdges[0][0] < maxDistance:
                return True
        return False

    def update_position(self, time, net, traci, sumolib, xOffset, yOffset):
        # get position
        self.currentPosition = self.get_position(xOffset, yOffset)
        # get pitch angle
        self.angle = self.get_angle()
        # compute current speed and convert it to m/s
        speed = math.sqrt(math.pow(self.currentPosition[0] - self.previousPosition[0], 2) + math.pow(self.currentPosition[2] - self.previousPosition[2], 2))
        self.previousPosition = self.currentPosition
        speed = speed / 0.2
        # if vehicle is not present in the network add it
        if self.name not in traci.vehicle.getIDList():
            try:
                traci.vehicle.add(vehID=self.name, routeID=traci.route.getIDList()[0])
                traci.vehicle.setColor(self.name, [0, 255, 0, 0])
            except:
                pass
        try:
            traci.vehicle.setSpeed(self.name, speed)
        except:
            pass
        try:
            traci.vehicle.moveToXY(vehID=self.name, edgeID='', lane=0, x=self.currentPosition[0], y=self.currentPosition[2], angle=180 * self.angle / math.pi, keepRoute=0)
        except:
            pass
        self.previousPosition = self.currentPosition
