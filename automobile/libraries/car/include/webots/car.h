/*
 * Description:   Car library to be used with the 'Car' proto (or any proto inherited by 'Car')
 * Comments:      Sponsored by the CTI project RO2IVSim (http://transport.epfl.ch/simulator-for-mobile-robots-and-intelligent-vehicles)
 */

#ifndef CAR_H
#define CAR_H

#include <webots/types.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
  WBU_CAR_TRACTION=0,
  WBU_CAR_PROPULSION=1,
  WBU_CAR_FOUR_BY_FOUR=2
} wbu_car_type;

typedef enum {
  WBU_CAR_COMBUTSION_ENGINE=0,
  WBU_CAR_ELECTRIC_ENGINE=1,
  WBU_CAR_PARALLEL_HYBRID_ENGINE=2,
  WBU_CAR_POWER_SPLIT_HYBRID_ENGINE=3
} wbu_car_engine_type;

typedef enum {
  WBU_CAR_WHEEL_FRONT_RIGHT=0,
  WBU_CAR_WHEEL_FRONT_LEFT=1,
  WBU_CAR_WHEEL_REAR_RIGHT=2,
  WBU_CAR_WHEEL_REAR_LEFT=3,
  WBU_CAR_WHEEL_NB
} wbu_car_wheel_index;

void wbu_car_init();
void wbu_car_cleanup();

wbu_car_type wbu_car_get_type();
wbu_car_engine_type wbu_car_get_engine_type();

void wbu_car_set_indicator_period(double period);
double wbu_car_get_indicator_period();

bool  wbu_car_get_backwards_lights();
bool  wbu_car_get_brake_lights();

double wbu_car_get_track_front();
double wbu_car_get_track_rear();
double wbu_car_get_wheelbase();
double wbu_car_get_front_wheel_radius();
double wbu_car_get_rear_wheel_radius();

double wbu_car_get_wheel_encoder(int wheel_index);
double wbu_car_get_wheel_speed(int wheel_index);
double wbu_car_get_right_steering_angle();
double wbu_car_get_left_steering_angle();

void wbu_car_enable_limited_slip_differential(bool enable);
void wbu_car_enable_indicator_auto_disabling(bool enable);

#ifdef __cplusplus
}
#endif

#endif // CAR_H
