#ifndef JOYSTICK_INTERFACE__HPP
#define JOYSTICK_INTERFACE__HPP

#include <map>

namespace webots {
  class Driver;
  class Joystick;
}

class JoystickInterface {
public:
  JoystickInterface(webots::Driver *driver);
  JoystickInterface(webots::Driver *driver, const char* configFile);
  virtual ~JoystickInterface() {};

  bool step();

private:
  static void fatal(const std::string &txt);
  static bool fileExists(const std::string &name);
  static double convertFeedback(int raw, int minimum, int maximum);

  void init(webots::Driver *driver, const char* configFile);

  int mGear;
  int mWipersMode;

  webots::Driver*   mDriver;
  webots::Joystick* mJoystick;

  std::map<const std::string, int> mAxesMap;
  std::map<const std::string, int> mAxesBoundsMap;
  std::map<const std::string, int> mButtonsMap;
  std::map<const std::string, double> mGainMap;
};

#endif // JOYSTICK_INTERFACE__HPP
