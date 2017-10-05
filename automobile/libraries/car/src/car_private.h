#ifndef CAR_PRIVATE_HPP
#define CAR_PRIVATE_HPP

#include <webots/robot.h>
#include "webots/car.h"

#define MIRRORS_NB 3
#define WIPERS_NB 2

enum {
  FRONT_LIGHT_INDEX,
  ANTIFOG_LIGHT_INDEX,
  RIGHT_INDICATOR_INDEX,
  LEFT_INDICATOR_INDEX,
  REAR_LIGHT_INDEX,
  BACKWARDS_LIGHT_INDEX,
  BRAKE_LIGHT_INDEX,
  LIGHTS_NB
} LIGHT_INDEX;

typedef struct {
  // Devices
  WbDeviceTag steering_motors[2]; // refeer to steering Motors, 0: right, 1: left
  WbDeviceTag steering_sensors[2]; // refeer to steering PositionSensors, 0: right, 1: left
  WbDeviceTag wheels[4];    // refeer to Motors, 0: front_right, 1: front_left, 2: rear_right, 3: rear_left
  WbDeviceTag sensors[4];    // refeer to PositionSensors, 0: front_right, 1: front_left, 2: rear_right, 3: rear_left
  WbDeviceTag brakes[4];    // refeer to Brakes, 0: front_right, 1: front_left, 2: rear_right, 3: rear_left
  WbDeviceTag lights[LIGHTS_NB];  // refeer to LEDs
  WbDeviceTag displays[MIRRORS_NB];  // mirror displays
  WbDeviceTag cameras[MIRRORS_NB];  // mirror camera
  WbDeviceTag steering_wheel;  // steering wheel motor
  WbDeviceTag wiper_motors[WIPERS_NB]; // windshield wiper motors,  0: right, 1: left
  WbDeviceTag wiper_sensor; // windshield wiper sensor
  // Commands
  double indicator_period;
  bool limited_slip_differential;
  bool indicator_auto_disabling;
  // Vehicle caracteristics
  wbu_car_type type;
  wbu_car_engine_type engine_type;
  double track_front;
  double track_rear;
  double wheelbase;
  double front_wheel_radius;
  double rear_wheel_radius;
  double brake_coefficient;
  double defaultDampingConstant;
  char  *engine_sound;
  double engine_sound_rpm_reference;
  double engine_min_rpm;
  double engine_max_rpm;
  double engine_coefficients[3]; // combustion engine
  double engine_max_torque;      // electric engine
  double engine_max_power;       // electric engine
  double hybrid_power_split_ratio;  // hybrid power-split engine
  double hybrid_power_split_rpm;    // hybrid power-split engine
  int gear_number;       // including reverse
  double *gear_ratio;  // 0 is reverse
  // Mesures
  double speeds[4];  // rad/s, 0: front_right, 1: front_left, 2: rear_right, 3: rear_left
  double max_acceleration;  // current bigger acceleration of all the actuated wheels [rad/s2]
  // Internal
  double right_angle;
  double left_angle;
} car;

car * _wbu_car_get_instance();
void _wbu_car_set_led_state_if_exist(int index, bool state);
bool _wbu_car_get_led_state_if_exist(int index);
bool _wbu_car_check_initialisation(const char * init_function, const char * calling_function);

#endif // CAR_PRIVATE_HPP
