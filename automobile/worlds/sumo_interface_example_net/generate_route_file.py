#!/usr/bin/env python

import random

#random.seed(42) # make reproducible
N = 36000 # number of time steps
# demand per second from different directions
pWE = 1./9
pEW = 1./12
pNS = 1./20
with open("./sumo.rou.xml", "w") as routes:
  print >> routes, """<routes>
  <vType id="typeWEslow" accel="0.6" decel="4.5" sigma="0.5" length="6" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
  <vType id="typeWEfast" accel="0.8" decel="4.5" sigma="0.5" length="6" minGap="2.5" maxSpeed="30" guiShape="passenger"/>
  <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.8" length="17" minGap="3" maxSpeed="25" guiShape="bus"/>

  <route id="right" edges="51o 1i 2o 52i" />
  <route id="left" edges="52o 2i 1o 51i" />
  <route id="rightInitial" edges="1i 2o 52i" />
  <route id="leftInitial" edges="2i 1o 51i" />
  <route id="down" edges="54o 4i 3o 53i" />
  """
  lastVeh = 0
  vehNr = 0
  # add 10 vehicles at the beginning of simulation
  for i in range(5):
    print >> routes, '  <vehicle id="right_initial_%i" type="typeWEfast" route="rightInitial" depart="0" departPos="%i" departSpeed="max" />' % (i, i * 120)
    print >> routes, '  <vehicle id="left_initial_%i" type="typeWEfast" route="leftInitial" depart="0" departPos="%i" departSpeed="max" />' % (i, i * 120)
  for i in range(N):
    # West -> Est
    if random.uniform(0,1) < pWE:
      if random.uniform(0,1) < 0.5:
        print >> routes, '  <vehicle id="right_%i" type="typeWEslow" route="right" depart="%i" />' % (vehNr, i)
      else:
        print >> routes, '  <vehicle id="right_%i" type="typeWEfast" route="right" depart="%i" />' % (vehNr, i)
      vehNr += 1
      lastVeh = i
    # Est -> West
    if random.uniform(0,1) < pEW:
      if random.uniform(0,1) < 0.5:
        print >> routes, '  <vehicle id="left_%i" type="typeWEslow" route="left" depart="%i" />' % (vehNr, i)
      else:
        print >> routes, '  <vehicle id="left_%i" type="typeWEfast" route="left" depart="%i" />' % (vehNr, i)
      vehNr += 1
      lastVeh = i
    # North -> South
    if random.uniform(0,1) < pNS:
      print >> routes, '  <vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,0,0"/>' % (vehNr, i)
      vehNr += 1
      lastVeh = i
  print >> routes, "</routes>"
