/*
 * Description:   CPP wrapper of the car library
 * Comments:      Sponsored by the CTI project RO2IVSim (http://transport.epfl.ch/simulator-for-mobile-robots-and-intelligent-vehicles)
 */

#ifndef CAR_HPP
#define CAR_HPP

#include <webots/Driver.hpp>

namespace webots {
  class Car : public Driver {
    public:

      enum {
        TRACTION=0,
        PROPULSION=1,
        FOUR_BY_FOUR=2
      };

      enum {
        COMBUTSION_ENGINE=0,
        ELECTRIC_ENGINE=1,
        PARALLEL_HYBRID_ENGINE=2,
        POWER_SPLIT_HYBRID_ENGINE=3
      };

      enum {
        WHEEL_FRONT_RIGHT=0,
        WHEEL_FRONT_LEFT=1,
        WHEEL_REAR_RIGHT=2,
        WHEEL_REAR_LEFT=3,
        WHEEL_NB
      };

      Car() : Driver() {}
      virtual ~Car() {}

      int getType();
      int getEngineType();

      void   setIndicatorPeriod(double period);
      double getIndicatorPeriod();

      bool getBackwardsLights();
      bool getBrakeLights();

      double getTrackFront();
      double getTrackRear();
      double getWheelbase();
      double getFrontWheelRadius();
      double getRearWheelRadius();

      double getWheelEncoder(int wheel);
      double getWheelSpeed(int wheel);
      double getRightSteeringAngle();
      double getLeftSteeringAngle();

      void enableLimitedSlipDifferential(bool enable);
      void enableIndicatorAutoDisabling(bool enable);
  };
}

#endif // CAR_HPP
