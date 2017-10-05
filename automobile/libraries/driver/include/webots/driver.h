/*
 * Description:   Driver library to be used with the 'Car' proto (or any proto inherited by 'Car') and the car library
 * Comments:      Sponsored by the CTI project RO2IVSim (http://transport.epfl.ch/simulator-for-mobile-robots-and-intelligent-vehicles)
 */

#ifndef DRIVER_H
#define DRIVER_H

#include <webots/types.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
  OFF,
  RIGHT,
  LEFT
} wbu_indicator_state;

typedef enum {
  SPEED,
  TORQUE
} wbu_control_mode;

typedef enum {
  DOWN,
  SLOW,
  NORMAL,
  FAST
} wbu_wipers_mode;

void wbu_driver_init();
void wbu_driver_cleanup();
int wbu_driver_step();

// positive: turn right, negative: turn left
void wbu_driver_set_steering_angle(double steering_angle);
double wbu_driver_get_steering_angle();

void wbu_driver_set_cruising_speed(double speed);
double wbu_driver_get_target_cruising_speed();

double wbu_driver_get_current_speed();

void wbu_driver_set_throttle(double throttle);
double wbu_driver_get_throttle();

void wbu_driver_set_brake_intensity(double intensity);
double wbu_driver_get_brake_intensity();

void wbu_driver_set_indicator(int state);
void wbu_driver_set_hazard_flashers(bool state);

wbu_indicator_state wbu_driver_get_indicator();
bool wbu_driver_get_hazard_flashers();

void wbu_driver_set_dipped_beams(bool state);
void wbu_driver_set_antifog_lights(bool state);

bool  wbu_driver_get_dipped_beams();
bool  wbu_driver_get_antifog_lights();

double wbu_driver_get_rpm();
int    wbu_driver_get_gear();
void   wbu_driver_set_gear(int gear);
int    wbu_driver_get_gear_number();
wbu_control_mode wbu_driver_get_control_mode();

void wbu_driver_set_wipers_mode(int mode);
wbu_wipers_mode wbu_driver_get_wipers_mode();

// kept for backward compatibility (Webots 8.6)
void wbu_driver_set_brake(double brake);
double wbu_driver_get_brake();

#ifdef __cplusplus
}
#endif

#endif // DRIVER_H
