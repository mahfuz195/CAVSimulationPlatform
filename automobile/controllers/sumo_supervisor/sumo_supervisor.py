# Description: Python Supervisor interface with SUMO using TraCI

from SumoSupervisor import SumoSupervisor

import optparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sumoPath = os.environ.get("WEBOTS_HOME") + "/projects/automobile/resources/sumo/"
    sumoPath.replace('/', os.sep)
    os.putenv("SUMO_HOME", sumoPath)
    if sys.platform.startswith('darwin'):
        libraryVariablePath = "DYLD_LIBRARY_PATH"

        # Fix the following error (shown on "El Capitan"):
        #    ./projects/automobile/resources/sumo/sumo-gui
        #    Fontconfig error: Cannot load default config file
        #    Quitting (on unknown error).
        if os.path.exists('/opt/local/etc/fonts/fonts.conf'):
            os.putenv('FONTCONFIG_PATH', '/opt/local/etc/fonts/')
        elif os.path.exists('/opt/X11/lib/X11/fontconfig/fonts.conf'):
            os.putenv('FONTCONFIG_PATH', '/opt/X11/lib/X11/fontconfig/')

    elif sys.platform.startswith('linux'):
        libraryVariablePath = "LD_LIBRARY_PATH"
    else:
        libraryVariablePath = "PATH"
    path = os.environ.get(libraryVariablePath)
    if path is None:
        os.putenv(libraryVariablePath, (sumoPath + "/bin").replace('/', os.sep))
    else:
        os.putenv(libraryVariablePath, (sumoPath + "/bin" + ';' + path).replace('/', os.sep))
    sys.path.append(sumoPath + os.sep + "tools")
    import traci
    import sumolib
except ImportError:
    sys.exit("It seems sumo is not present in your Webots projects folder.")

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--no-gui", dest="noGUI", action="store_true", default=False, help="runs the command line version of sumo")
    optParser.add_option("--verbose", dest="verbose", action="store_true", default=False, help="prints sumo output in Webots console")
    optParser.add_option("--no-netconvert", dest="noNetconvert", action="store_true", default=False, help="does not run netconvert before launching sumo")
    optParser.add_option("--disable-traffic-lights", dest="disableTrafficLights", action="store_true", default=False, help="disables the update of the traffic lights state in Webots")
    optParser.add_option("--step", type="int", dest="step", default=200, help="specifies the time step of sumo [ms]")
    optParser.add_option("--max-vehicles", type="int", dest="maxVehicles", default=100, help="specifies the maximum vehicles to add on Webots side")
    optParser.add_option("--rotate-wheels", dest="rotateWheels", action="store_true", default=False, help="enables the wheels rotation.")
    optParser.add_option("--radius", type="int", dest="radius", default=-1, help="specifies the visibility radius of the vehicles in meters (-1 means no limit)")
    optParser.add_option("--enable-height", dest="enableHeight", action="store_true", default=False, help="specifies if height information should be extracted from the edge name")
    optParser.add_option("--directory", dest="directory", default="", help="specifies the directory where are located the files defining the network")
    optParser.add_option("--port", type="int", dest="port", default=8873, help="specifies which port to use")
    optParser.add_option("--seed", type="int", dest="seed", default=1, help="specifies the seed of the SUMO random number generator (0 for the '--random' option of SUMO)")
    optParser.add_option("--use-display", dest="useDisplay", action="store_true", default=False, help="displays the gui view of SUMO in a Webots display (only working in gui mode)")
    optParser.add_option("--display-refresh-rate", type="int", dest="displayRefreshRate", default=1000, help="specifies the refresh rate of the SUMO display in Webots")
    optParser.add_option("--display-zoom", type="float", dest="displayZoom", default=1.0, help="specifies the initial zoom of the SUMO display in Webots (100 means no scaling)")
    optParser.add_option("--display-fit-size", dest="displayFitSize", action="store_true", default=False, help="specifies if the image should be resized to fit the SUMO display size or not")
    optParser.add_option("--sumo-arguments", dest="sumoArguments", default="", help="specifies additional SUMO arguments.")
    options, args = optParser.parse_args()
    return options

# The main program starts from here

# Start sumo as a server and then connect and run
controller = SumoSupervisor()
options = get_options()

useDisplay = False
if options.noGUI:
    sumoBinary = sumoPath + "bin" + os.sep + "sumo"
else:
    if sys.platform.startswith('darwin') and not os.path.exists("/opt/X11"):
        sys.stderr.write("X11 is not installed and is required to launch the gui version of SUMO.\n")
        sys.stderr.write("You can easily install X11 following this link: https://support.apple.com/en-us/HT201341\n")
        sys.stderr.write("Starting command line version of SUMO instead.\n")
        sumoBinary = sumoPath + "bin" + os.sep + "sumo"
    else:
        sumoBinary = sumoPath + "bin" + os.sep + "sumo-gui"
        if options.useDisplay:
            useDisplay = True

# check if the target directory is in the WEBOTS_HOME path or not set, and adjust path if it is the case
directory = options.directory
if directory.startswith("WEBOTS_HOME"):
    directory = directory.replace("WEBOTS_HOME", os.environ.get("WEBOTS_HOME"))
elif directory == "":  # no directory set, use standard directory (same name of the world ending with '_net')
    directory = re.sub(r'.wbt$', '_net', controller.getWorldPath())
if not os.path.isdir(directory):
    sys.exit("You should specify in which directory are stored the network files associated to this world.")

# generate temporary directory and move network file in it
tmpDirectory = tempfile.mkdtemp()
for item in os.listdir(directory):
    s = os.path.join(directory, item)
    d = os.path.join(tmpDirectory, item)
    if os.path.isdir(s):
        shutil.copytree(s, d, True)
    else:
        shutil.copy2(s, d)

# generate the net file with the 'netconvert' utility
if not options.noNetconvert:
    # check if default configuration file exist
    netConfigurationFile = (tmpDirectory + "/sumo.netccfg").replace('/', os.sep)
    if not os.path.isfile(netConfigurationFile):
        fileFound = ""
        # no default configuration file, try to find another one
        for file in os.listdir(tmpDirectory):
            if file.endswith(".netccfg"):
                if fileFound == "":
                    netConfigurationFile = (tmpDirectory + "/" + file).replace('/', os.sep)
                    fileFound = file
                else:
                    print "More than one NETCONVERT configuration file found, using: " + fileFound + "\n"
                    break
    if not os.path.isfile(netConfigurationFile):
        shutil.rmtree(tmpDirectory)
        sys.exit("Could not find any NETCONVERT configuration file (*.netccfg).")
    if not subprocess.call([sumoPath + "bin" + os.sep + "netconvert", "-c", netConfigurationFile, "--xml-validation", "never"], stdout=sys.stdout, stderr=sys.stderr) == 0:
        sys.exit("NETCONVERT failed to generate the network file.")
print "Temporary network files generated in " + tmpDirectory + "\n"

# this is the normal way of using traci. sumo is started as a
# subprocess and then the python script connects and runs
FNULL = open(os.devnull, 'w')
# check if default configuration file exist
configurationFile = (tmpDirectory + "/sumo.sumocfg").replace('/', os.sep)
if not os.path.isfile(configurationFile):
    fileFound = ""
    for file in os.listdir(tmpDirectory):
        # no default configuration file, try to find another one
        if file.endswith(".sumocfg"):
            if fileFound == "":
                configurationFile = (tmpDirectory + "/" + file).replace('/', os.sep)
                fileFound = file
            else:
                print "More than one SUMO configuration file found, using: " + fileFound + "\n"
                break
if not os.path.isfile(configurationFile):
    shutil.rmtree(tmpDirectory)
    sys.exit("Could not find any SUMO configuration file (*.sumocfg).")

arguments = [sumoBinary, "-c", configurationFile, "--start", "--quit-on-end=true", "--step-length=" + str(options.step/1000.0), "--remote-port", str(options.port)]

if options.seed == 0:
    arguments.append("--random")
else:
    arguments.append("--seed=" + str(options.seed))

if options.verbose:
    arguments.append("--verbose")

if os.path.isfile(tmpDirectory + "/gui-settings.cfg") and not options.noGUI:
    arguments.extend(["--gui-settings-file", (tmpDirectory + "/gui-settings.cfg").replace('/', os.sep)])

if options.sumoArguments != "":
    arguments.extend(options.sumoArguments.split())

sumoProcess = subprocess.Popen(arguments, stdout=FNULL, stderr=subprocess.STDOUT)
controller.run(options.port, options.disableTrafficLights, tmpDirectory,
               options.step, options.rotateWheels, options.maxVehicles,
               options.radius, options.enableHeight, useDisplay,
               options.displayRefreshRate, options.displayZoom,
               options.displayFitSize, traci, sumolib)
sumoProcess.terminate()

# remove temporary folder
print "Removing temporary network files in " + tmpDirectory + "\n"
shutil.rmtree(tmpDirectory)
