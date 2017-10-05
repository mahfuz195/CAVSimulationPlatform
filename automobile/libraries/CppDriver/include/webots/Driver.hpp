/*
 * Description:   CPP wrapper of the driver library
 * Comments:      Sponsored by the CTI project RO2IVSim (http://transport.epfl.ch/simulator-for-mobile-robots-and-intelligent-vehicles)
 */

#ifndef DRIVER_HPP
#define DRIVER_HPP

#include <webots/Robot.hpp>

namespace webots {
  class Driver : public Robot {
    public:
      enum {
        INDICATOR_OFF,
        INDICATOR_RIGHT,
        INDICATOR_LEFT
      };

      enum {
        SPEED,
        TORQUE
      };

      enum {
        DOWN,
        SLOW,
        NORMAL,
        FAST
      };

      Driver();
      virtual ~Driver();

      virtual int step();

      // positive: turn right, negative: turn left
      void   setSteeringAngle(double steeringAngle);
      double getSteeringAngle();

      void   setCruisingSpeed(double speed);
      double getTargetCruisingSpeed();

      double getCurrentSpeed();

      void   setThrottle(double throttle);
      double getThrottle();

      void   setBrakeIntensity(double intensity);
      double getBrakeIntensity();

      void setIndicator(int state);
      void setHazardFlashers(bool state);

      int getIndicator();
      bool getHazardFlashers();

      void setDippedBeams(bool state);
      void setAntifogLights(bool state);

      bool getDippedBeams();
      bool getAntifogLights();

      double getRpm();
      int    getGear();
      void   setGear(int gear);
      int    getGearNumber();
      int    getControlMode();

      void setWipersMode(int mode);
      int getWipersMode();

      // kept for backward compatibility only
      void   setBrake(double brake);

    private:
      virtual int step(int t) { return Robot::step(t); }
  };
}

#endif // DRIVER_HPP
