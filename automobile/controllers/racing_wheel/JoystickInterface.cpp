#include <webots/Driver.hpp>
#include <webots/Joystick.hpp>
#include <QtCore/QSettings>

#include "JoystickInterface.hpp"

#include <algorithm>
#include <fstream>
#include <sstream>

#define NAXIS       3
#define NAXISBOUNDS 2
#define NBUTTONS    13
#define NGAINS      2

using namespace webots;
using namespace std;

static const char *axesNames[NAXIS] = {
  "Steering", "Throttle", "Brake"
};

static const char *axesBoundNames[NAXISBOUNDS] = {
  "min", "max"
};

static const char *buttonNames[NBUTTONS] = {
  "RightWarning", "LeftWarning", "NextGear", "PreviousGear", "FirstGear",
  "SecondGear", "ThirdGear", "FourthGear", "FifthGear", "SixthGear", "ReverseGear",
  "NextWipersMode", "PreviousWipersMode"
};

static const char *gainNames[NGAINS] = {
  "AutoCentering", "Resistance"
};

#ifdef _WIN32
  static string platformExtension = "windows";
#elif defined(__APPLE__)
  static string platformExtension = "mac";
#elif defined(__linux__)
  static string platformExtension = "linux";
#else
  #error Unsupported OS
#endif

void JoystickInterface::fatal(const string &txt) {
  cerr << txt << endl;
  exit(-1);
}

bool JoystickInterface::fileExists(const string &name) {
  ifstream f(name.c_str());
  return f.good();
}

double JoystickInterface::convertFeedback(int raw, int minimum, int maximum) {
  if (maximum == minimum)
    fatal("Prevent division by 0.");
  return std::max(0.0, std::min(1.0,
    ((double) (raw - minimum)) / ((double) (maximum - minimum))
  ));
}

void JoystickInterface::init(webots::Driver *driver, const char* configFile) {
  cout << "Configuration file: " << configFile << endl;

  mDriver = driver;

  mGear = 1;
  mDriver->setGear(mGear);
  mDriver->setWipersMode(mWipersMode);

  mJoystick = driver->getJoystick();
  mJoystick->enable(mDriver->getBasicTimeStep());
  QSettings settings(configFile, QSettings::IniFormat);
  settings.setIniCodec("UTF-8");
  for (int i = 0; i < NAXIS; ++i)
    mAxesMap[axesNames[i]] = settings.value(QString("Axis/") + QString(axesNames[i]), -1).toInt();
  for (int i = 0; i < NAXIS; ++i) {
    for (int j = 0; j < NAXISBOUNDS; ++j) {
      string boundName = string() + axesBoundNames[j] + axesNames[i];
      mAxesBoundsMap[boundName] = settings.value(QString("AxisBounds/") + QString::fromStdString(boundName), 0).toInt();
    }
  }
  for (int i = 0; i < NBUTTONS; ++i)
    mButtonsMap[buttonNames[i]] = settings.value(QString("Buttons/") + QString(buttonNames[i]), -1).toInt();
  for (int i = 0; i < NGAINS; ++i)
    mGainMap[gainNames[i]] = settings.value(QString("Gains/") + QString(gainNames[i]), 0.0).toDouble();
}

JoystickInterface::JoystickInterface(webots::Driver *driver) {
  // 1. find out "joystick_configuration_file" value of the "setup.cfg" file
  string configurationFile;

  ifstream setupStream("setup.cfg");
  if (!setupStream.good())
    fatal("Cannot open setup.cfg file.");

  string line;
  while (getline(setupStream, line)) {
    istringstream iss(line);
    string key, value;
    if (iss >> key >> value) {
      if (key == "joystick_configuration_file")
        configurationFile = value;
    }
  }

  if (configurationFile == "")
    fatal("Key 'joystick_configuration_file' not found in 'setup.cfg'.");

  // 2. look for platform specific configuration file:
  string platformConfigurationFile = configurationFile;
  platformConfigurationFile.erase(platformConfigurationFile.end() - 4, platformConfigurationFile.end());
  platformConfigurationFile += "." + platformExtension + ".ini";
  if (fileExists(platformConfigurationFile))
    configurationFile = platformConfigurationFile;

  init(driver, configurationFile.c_str());
}

JoystickInterface::JoystickInterface(webots::Driver *driver, const char* configFile) {
  init(driver, configFile);
}

bool JoystickInterface::step() {
  if (!mJoystick->isConnected())
    return false;

  // useful debug code: display joystick state
  /*
  cout << "axes:" << endl;
  for (int i = 0; i < mJoystick->getNumberOfAxes(); ++i)
    cout << "- axe " << i << " " << mJoystick->getAxisValue(i) << endl;
  int b = mJoystick->getPressedButton();
  cout << "buttons:" << endl;
  while (b >= 0) {
    cout << b << " ";
    b = mJoystick->getPressedButton();
  }
  cout << endl << endl;
  */

  // update steering, throttle, and brake based on axes value

  // raw data
  int steeringFeedback = mJoystick->getAxisValue(mAxesMap["Steering"]);
  int throttleFeedback = mJoystick->getAxisValue(mAxesMap["Throttle"]);
  int brakeFeedback = mJoystick->getAxisValue(mAxesMap["Brake"]);

  // bounded scaled data [0, 1]
  double steeringAngle = convertFeedback(steeringFeedback, mAxesBoundsMap["minSteering"], mAxesBoundsMap["maxSteering"]);
  double throttle = convertFeedback(throttleFeedback, mAxesBoundsMap["minThrottle"], mAxesBoundsMap["maxThrottle"]);
  double brake = convertFeedback(brakeFeedback, mAxesBoundsMap["minBrake"], mAxesBoundsMap["maxBrake"]);
  // useful debug code: display the resulting scaled data before sending it to the driver library
  // cout << "steering:" << steeringAngle << " throttle:" << throttle << " brake:" << brake << endl;

  // to automobile API
  mDriver->setSteeringAngle(steeringAngle - 0.5); // convert to [-0.5, 0.5] radian range
  mDriver->setThrottle(throttle);
  mDriver->setBrakeIntensity(brake);

  // update gear and indicator based on buttons state
  int button = mJoystick->getPressedButton();
  int gear = mGear;
  int wipersMode = mWipersMode;
  static bool wasSwitchingToNextGear = false;
  static bool wasSwitchingToPreviousGear = false;
  bool isSwitchingToNextGear = false;
  bool isSwitchingToPreviousGear = false;
  static bool wasLeftBlinkerOn = false;
  static bool wasRightBlinkerOn = false;
  bool isLeftBlinkerOn = false;
  bool isRightBlinkerOn = false;
  static bool wasSwitchingToNextWipersMode = false;
  static bool wasSwitchingToPreviousWipersMode = false;
  bool isSwitchingToNextWipersMode = false;
  bool isSwitchingToPreviousWipersMode = false;

  while (button >= 0) {
    if (button == mButtonsMap["NextGear"]) {
      if (!wasSwitchingToNextGear)
        gear += 1;
      isSwitchingToNextGear = true;
    } else if (button == mButtonsMap["PreviousGear"]) {
        if (!wasSwitchingToPreviousGear)
          gear -= 1;
        isSwitchingToPreviousGear = true;
    } else if (button == mButtonsMap["FirstGear"])
      gear = 1;
    else if (button == mButtonsMap["SecondGear"])
      gear = 2;
    else if (button == mButtonsMap["ThirdGear"])
      gear = 3;
    else if (button == mButtonsMap["FourthGear"])
      gear = 4;
    else if (button == mButtonsMap["FifthGear"])
      gear = 5;
    else if (button == mButtonsMap["SixthGear"])
      gear = 6;
    else if (button == mButtonsMap["ReverseGear"])
      gear = -1;
    else if (button == mButtonsMap["RightWarning"]) {
      if (!wasRightBlinkerOn) // not pressed previous step
        mDriver->getIndicator() == Driver::INDICATOR_RIGHT ? mDriver->setIndicator(Driver::INDICATOR_OFF) : mDriver->setIndicator(Driver::INDICATOR_RIGHT);
      isRightBlinkerOn = true;
    } else if (button == mButtonsMap["LeftWarning"]) {
      if (!wasLeftBlinkerOn) // not pressed previous step
        mDriver->getIndicator() == Driver::INDICATOR_LEFT ? mDriver->setIndicator(Driver::INDICATOR_OFF) : mDriver->setIndicator(Driver::INDICATOR_LEFT);
      isLeftBlinkerOn = true;
    } else if (button == mButtonsMap["NextWipersMode"] || wipersMode < Driver::FAST) {
      if (!wasSwitchingToNextWipersMode)
        wipersMode += 1;
      isSwitchingToNextWipersMode = true;
    } else if (button == mButtonsMap["PreviousWipersMode"] || wipersMode > Driver::DOWN) {
      if (!wasSwitchingToPreviousWipersMode)
        wipersMode -= 1;
      isSwitchingToPreviousWipersMode = true;
    }

    button = mJoystick->getPressedButton();
  }
  wasSwitchingToNextGear = isSwitchingToNextGear;
  wasSwitchingToPreviousGear = isSwitchingToPreviousGear;
  wasLeftBlinkerOn = isLeftBlinkerOn;
  wasRightBlinkerOn = isRightBlinkerOn;
  wasSwitchingToNextWipersMode = isSwitchingToNextWipersMode;
  wasSwitchingToPreviousWipersMode = isSwitchingToPreviousWipersMode;

  gear = std::max(-1, std::min(mDriver->getGearNumber(), gear));
  if (gear != mGear) {
    mGear = gear;
    cout << "gear: " << mGear << endl;
    mDriver->setGear(mGear);
  }

  if (wipersMode != mWipersMode) {
    mWipersMode = wipersMode;
    mDriver->setWipersMode(mWipersMode);
  }

  // update resistance and auto-centering gain based on speed
  static const double maxSpeed = 60.0; // speed from which the max gain is applied
  double speed = mDriver->getCurrentSpeed();
  if (mGainMap["AutoCentering"] > 0.0)
    mJoystick->setAutoCenteringGain(speed > maxSpeed ? mGainMap["AutoCentering"] : mGainMap["AutoCentering"] * speed / maxSpeed);
  if (mGainMap["Resistance"] > 0.0)
    mJoystick->setResistanceGain(speed > maxSpeed ? 0.0 : mGainMap["Resistance"] * (1.0 - speed / maxSpeed));

  return true;
}
