NSGREEN = "GrGr"
NSYELLOW = "yryr"
WEGREEN = "rGrG"
WEYELLOW = "ryry"

PROGRAM = [WEYELLOW,WEYELLOW,WEYELLOW,NSGREEN,NSGREEN,NSGREEN,NSGREEN,NSGREEN,NSGREEN,NSGREEN,NSGREEN,NSYELLOW,NSYELLOW,WEGREEN]

class SumoSupervisorPlugin:
    def __init__(self, supervisor, traci, net):
        self.traci = traci
        self.runned = 0
        self.programPointer = len(PROGRAM)-1
        # Subscribe to the induction loop (road sensor)
        self.traci.inductionloop.subscribe("0", [traci.constants.LAST_STEP_VEHICLE_NUMBER])

    def run(self, duration):
        self.runned = self.runned + duration
        # At least once second has passed since last update of the traffic lights
        if self.runned >= 1000:
            self.runned = self.runned - 1000
            self.programPointer = min(self.programPointer+1, len(PROGRAM)-1)
            numPriorityVehicles = self.traci.inductionloop.getSubscriptionResults()["0"][self.traci.constants.LAST_STEP_VEHICLE_NUMBER]
            if numPriorityVehicles > 0:
                if self.programPointer == len(PROGRAM)-1:
                    # we are in the WEGREEN phase. start the priority phase sequence
                    self.programPointer = 0
                elif PROGRAM[self.programPointer] != WEYELLOW:
                    # horizontal traffic is already stopped. restart priority phase
                    # sequence at green
                    self.programPointer = 3
                else:
                    # we are in the WEYELLOW phase. continue sequence
                    pass
            self.traci.trafficlights.setRedYellowGreenState("0", PROGRAM[self.programPointer])
