/*
 * Description:   Implementation of the car library
 * Comments:      Sponsored by the CTI project RO2IVSim (http://transport.epfl.ch/simulator-for-mobile-robots-and-intelligent-vehicles)
 */

#include "webots/car.h"
#include "car_private.h"

#include <webots/camera.h>
#include <webots/display.h>
#include <webots/device.h>
#include <webots/led.h>
#include <webots/motor.h>
#include <webots/position_sensor.h>
#include <webots/robot.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DEFAULT_INDICATOR_PERIOD 0.5
#ifdef _MSC_VER
#ifndef INFINITY
static const double tmp = 1.0;
#define INFINITY (1.0 / (tmp - 1.0))
#endif
#endif

static car *instance = NULL;
car * _wbu_car_get_instance() {
  return instance;
}

static const char *motorNames[] = {
  "right_steer",       "left_steer",
  "right_front_wheel", "left_front_wheel",
  "right_rear_wheel",  "left_rear_wheel"
};

static const char *wheelsSensorsNames[] = {
  "right_steer_sensor", "left_steer_sensor",
  "right_front_sensor", "left_front_sensor",
  "right_rear_sensor",  "left_rear_sensor"
};

static const char *wheelsBrakesNames[] = {
  "right_front_brake", "left_front_brake",
  "right_rear_brake",  "left_rear_brake"
};

static const char *lightNames[LIGHTS_NB] = {
  "front_lights",     "antifog_lights",
  "right_indicators", "left_indicators",
  "rear_lights",      "backwards_lights",
  "brake_ligths"
};

static const char *displayNames[MIRRORS_NB] = {
  "rear_display", "left_wing_display", "right_wing_display"
};

static const char *cameraNames[MIRRORS_NB] = {
  "rear_camera", "left_wing_camera", "right_wing_camera"
};

static const char *steeringWheelName = "steering_wheel_motor";

static const char *wiperMotorNames[WIPERS_NB] = {
  "right_wiper_motor", "left_wiper_motor"
};

static const char *wiperSensorName = "wiper_sensor";

//***********************************//
//        Utility functions          //
//***********************************//

bool _wbu_car_check_initialisation(const char * init_function, const char * calling_function) {
  if (instance == NULL) {
    fprintf(stderr,"Warning: '%s' should be called before to use '%s'.\n", init_function, calling_function);
    return false;
  } else
    return true;
}

bool _wbu_car_get_led_state_if_exist(int index) {
  if (index < LIGHTS_NB && instance->lights[index] != 0 && wb_led_get(instance->lights[index]) != 0)
    return true;
  else
    return false;
}

void _wbu_car_set_led_state_if_exist(int index, bool state) {
  if (index < LIGHTS_NB && instance->lights[index] != 0)
    wb_led_set(instance->lights[index], state);
}

//***********************************//
//          API functions            //
//***********************************//


void wbu_car_init() {
  if (instance != NULL)
    return;

  wb_robot_init();
  int i = 0, j = 0;
  instance = (car *)malloc(sizeof(car));
  for (i = 0; i < 4; i++) {
    instance->wheels[i] = 0;
    instance->speeds[i] = 0.0;
  }
  for (i = 0; i < LIGHTS_NB; i++)
    instance->lights[i] = 0;
  for (i = 0; i < MIRRORS_NB; i++) {
    instance->displays[i] = 0;
    instance->cameras[i]  = 0;
  }
  for (i = 0; i < WIPERS_NB; i++)
    instance->wiper_motors[i] = 0;
  instance->steering_wheel            = 0;
  instance->wiper_sensor              = 0;
  instance->indicator_period          = DEFAULT_INDICATOR_PERIOD;
  instance->right_angle               = 0.0;
  instance->left_angle                = 0.0;
  instance->limited_slip_differential = true;
  instance->indicator_auto_disabling  = true;

  // Parse vehicle caracteristics from the beginning of the data string
  char engine_type;
  int engine_sound_length;
  char *sub_data_string = (char *)wb_robot_get_data();
  sscanf(sub_data_string,"%lf %lf %lf %lf %lf %lf %lf %c %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %d %d",
    &instance->wheelbase,
    &instance->track_front,
    &instance->track_rear,
    &instance->front_wheel_radius,
    &instance->rear_wheel_radius,
    &instance->brake_coefficient,
    &instance->defaultDampingConstant,
    &engine_type,
    &instance->engine_max_torque,
    &instance->engine_max_power,
    &instance->engine_min_rpm,
    &instance->engine_max_rpm,
    &instance->engine_coefficients[0],
    &instance->engine_coefficients[1],
    &instance->engine_coefficients[2],
    &instance->hybrid_power_split_ratio,
    &instance->hybrid_power_split_rpm,
    &instance->engine_sound_rpm_reference,
    &instance->gear_number,
    &engine_sound_length);

  // Extract engine type from the char
  if (engine_type == 'E')
    instance->engine_type = WBU_CAR_ELECTRIC_ENGINE;
  else if (engine_type == 'P')
    instance->engine_type = WBU_CAR_PARALLEL_HYBRID_ENGINE;
  else if (engine_type == 'S')
    instance->engine_type = WBU_CAR_POWER_SPLIT_HYBRID_ENGINE;
  else
    instance->engine_type = WBU_CAR_COMBUTSION_ENGINE;

  // Extract the gear ratio from the rest of the string (variable size)
  instance->gear_ratio = (double *)malloc(instance->gear_number * sizeof(double));
  // skip first twenty parameters (beginning of the string already parsed)
  for (i = 0; i < 20; ++i)
    sub_data_string = strchr(sub_data_string,' ') + 1;
  // get all the gear ratio
  for (i = 0; i < instance->gear_number; ++i) {
    sscanf(sub_data_string,"%lf", &instance->gear_ratio[i]);
    sub_data_string = strchr(sub_data_string,' ') + 1;
  }
  // a minimum of two gear ratio is required
  if (instance->gear_number < 2) {
    fprintf(stderr,"Warning: Any car should have a minimum of two gear ratio.");
    exit(0);
  }

  // Extract the engine sound file name
  instance->engine_sound = (char *)malloc(engine_sound_length + 1);
  memcpy(instance->engine_sound, sub_data_string, engine_sound_length);
  instance->engine_sound[engine_sound_length] = '\0';

  // Check for steering motors and position sensors
  instance->steering_motors[0] = wb_robot_get_device(motorNames[0]);
  instance->steering_motors[1] = wb_robot_get_device(motorNames[1]);
  instance->steering_sensors[0] = wb_robot_get_device(wheelsSensorsNames[0]);
  instance->steering_sensors[1] = wb_robot_get_device(wheelsSensorsNames[1]);

  if (instance->steering_motors[0] == 0 || instance->steering_motors[1] == 0) {
    fprintf(stderr,"Warning: Any car should have '%s' and '%s' motors.\n", motorNames[0], motorNames[1]);
    exit(0);
  }

  if (instance->steering_sensors[0] == 0 || instance->steering_sensors[1] == 0) {
    fprintf(stderr,"Warning: Any car should have '%s' and '%s' position sensors.\n", wheelsSensorsNames[0], wheelsSensorsNames[1]);
    exit(0);
  }
  wb_position_sensor_enable(instance->steering_sensors[0], (int)wb_robot_get_basic_time_step());
  wb_position_sensor_enable(instance->steering_sensors[1], (int)wb_robot_get_basic_time_step());

  // Check for motors and lights
  int n_devices = wb_robot_get_number_of_devices();
  for (i = 0; i < n_devices; i++) {
    WbDeviceTag tag = wb_robot_get_device_by_index(i);
    const char *name = wb_device_get_name(tag);
    // Check for motors without warning
    for (j = 0; j < 4; j++) {
      if (strcmp(name, motorNames[j+2]) == 0)
        instance->wheels[j] = tag;
    }
    // Check for lights without warning
    for (j = 0; j < LIGHTS_NB; j++) {
      if (strcmp(name, lightNames[j]) == 0)
        instance->lights[j] = tag;
    }
    // Check for cameras and displays without warning
    for (j = 0; j < MIRRORS_NB; j++) {
      if (strcmp(name, displayNames[j]) == 0)
        instance->displays[j] = tag;
      if (strcmp(name, cameraNames[j]) == 0)
        instance->cameras[j] = tag;
    }
    // Check for steering wheel motor without warning
    if (strcmp(name, steeringWheelName) == 0)
      instance->steering_wheel = tag;

    // Check for wiper motors and sensor without warning
    for (j = 0; j < WIPERS_NB; j++) {
      if (strcmp(name, wiperMotorNames[j]) == 0)
        instance->wiper_motors[j] = tag;
    }
    if (strcmp(name, wiperSensorName) == 0)
      instance->wiper_sensor = tag;
  }

  // Check and enable for wiper sensor
    if (instance->wiper_sensor != 0)
      wb_position_sensor_enable(instance->wiper_sensor, (int)wb_robot_get_basic_time_step());

  // Check for type
  if (instance->wheels[0] != 0 && instance->wheels[1] != 0 && instance->wheels[2] != 0 && instance->wheels[3] != 0)
    instance->type = WBU_CAR_FOUR_BY_FOUR;
  else if (instance->wheels[0] != 0 && instance->wheels[1] != 0)
    instance->type = WBU_CAR_TRACTION;
  else if (instance->wheels[2] != 0 && instance->wheels[3] != 0)
    instance->type = WBU_CAR_PROPULSION;
  else {
    fprintf(stderr,"Warning: this car does not have the required motors\n");
    exit(0);
  }

  // Get positionSensors
  for (i = 0; i < 4; i++) {
    instance->sensors[i] = wb_robot_get_device(wheelsSensorsNames[i+2]);
    if (instance->sensors[i] == 0) {
      fprintf(stderr,"Warning: this car does not have the required position sensors\n");
      exit(0);
    }
  }

  // Get Brake device
  for (i = 0; i < 4; i++) {
    instance->brakes[i] = wb_robot_get_device(wheelsBrakesNames[i]);
    if (instance->brakes[i] == 0) {
      fprintf(stderr,"Warning: this car does not have the required brake devices\n");
      exit(0);
    }
  }

  // Attach cameras to displays
  for (i = 0; i < MIRRORS_NB; i++) {
    if (instance->displays[i] != 0 && instance->cameras[i] != 0) {
      int display_width = wb_display_get_width(instance->displays[i]);
      int display_height = wb_display_get_height(instance->displays[i]);
      int camera_width = wb_camera_get_width(instance->cameras[i]);
      int camera_height = wb_camera_get_height(instance->cameras[i]);
      if (display_width == camera_width && display_height == camera_height) {
        int step = wb_robot_get_basic_time_step();
        while (step < 40) // maximum 25Hz at real-time
          step += wb_robot_get_basic_time_step();
        wb_camera_enable(instance->cameras[i], step);
        wb_display_attach_camera(instance->displays[i], instance->cameras[i]);
        wb_display_set_alpha(instance->displays[i], 0.0);
        wb_display_fill_rectangle(instance->displays[i], 0, 0, display_width, display_height);
        wb_display_set_alpha(instance->displays[i], 1.0);
      }
    }
  }

  // Set target position to infinite (we are not going to use control in position, but only speed and torque)
  if (instance->type == WBU_CAR_TRACTION || instance->type == WBU_CAR_FOUR_BY_FOUR) {
    wb_motor_set_position(instance->wheels[0], INFINITY);
    wb_motor_set_position(instance->wheels[1], INFINITY);
    wb_motor_set_velocity(instance->wheels[0], 0.0);
    wb_motor_set_velocity(instance->wheels[1], 0.0);
  }
  if (instance->type == WBU_CAR_PROPULSION || instance->type == WBU_CAR_FOUR_BY_FOUR) {
    wb_motor_set_position(instance->wheels[2], INFINITY);
    wb_motor_set_position(instance->wheels[3], INFINITY);
    wb_motor_set_velocity(instance->wheels[2], 0.0);
    wb_motor_set_velocity(instance->wheels[3], 0.0);
  }
}

void wbu_car_cleanup() {
  if (instance == NULL)
    return;
  if (instance->gear_ratio != NULL) {
    free(instance->gear_ratio);
    instance->gear_ratio = NULL;
  }
  if (instance->engine_sound != NULL) {
    free(instance->engine_sound);
    instance->engine_sound = NULL;
  }
  free(instance);
  instance = NULL;
  wb_robot_cleanup();
}

wbu_car_type wbu_car_get_type() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_type()"))
    return (wbu_car_type)0;
  return instance->type;
}

wbu_car_engine_type wbu_car_get_engine_type() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_engine_type()"))
    return (wbu_car_engine_type)0;
  return instance->engine_type;
}

double wbu_car_get_track_front() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_track_front()"))
    return 0;
  return instance->track_front;
}

double wbu_car_get_track_rear() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_track_rear()"))
    return 0;
  return instance->track_rear;
}

double wbu_car_get_wheelbase() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_wheelbase()"))
    return 0;
  return instance->wheelbase;
}

double wbu_car_get_front_wheel_radius() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_front_wheel_radius()"))
    return 0;
  return instance->front_wheel_radius;
}

double wbu_car_get_rear_wheel_radius() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_rear_wheel_radius()"))
    return 0;
  return instance->rear_wheel_radius;
}

void wbu_car_set_indicator_period(double period) {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_set_indicator_period()"))
    return;
  instance->indicator_period = period;
}

double wbu_car_get_indicator_period() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_indicator_period()"))
    return 0;
  return instance->indicator_period;
}

bool wbu_car_get_backwards_lights() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_backwards_lights()"))
    return false;
  return _wbu_car_get_led_state_if_exist(BACKWARDS_LIGHT_INDEX);
}

bool wbu_car_get_brake_lights() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_brake_lights()"))
    return false;
  return _wbu_car_get_led_state_if_exist(BRAKE_LIGHT_INDEX);
}

double wbu_car_get_wheel_encoder(int wheel_index) {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_wheel_encoder()"))
    return 0.0;
  if (wheel_index >= WBU_CAR_WHEEL_NB) {
    fprintf(stderr,"Warning: maximum wheel index is %d.\n", WBU_CAR_WHEEL_NB);
    return 0.0;
  }
  // check if needed to be enable
  if(wb_position_sensor_get_sampling_period(instance->sensors[wheel_index]) == 0)
    wb_position_sensor_enable(instance->sensors[wheel_index], (int)wb_robot_get_basic_time_step());
  return wb_position_sensor_get_value(instance->sensors[wheel_index]);
}

double wbu_car_get_wheel_speed(int wheel_index) {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_wheel_speed()"))
    return 0.0;
  if (wheel_index >= WBU_CAR_WHEEL_NB) {
    fprintf(stderr,"Warning: maximum wheel index is %d.\n", WBU_CAR_WHEEL_NB);
    return 0.0;
  }
  return instance->speeds[wheel_index];
}

double wbu_car_get_right_steering_angle() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_right_steering_angle()"))
    return 0.0;
  return wb_position_sensor_get_value(instance->steering_sensors[0]);
}

double wbu_car_get_left_steering_angle() {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_get_left_steering_angle()"))
    return 0.0;
  return wb_position_sensor_get_value(instance->steering_sensors[1]);
}

void wbu_car_enable_limited_slip_differential(bool enable) {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_limited_slip_differential()"))
    return;
  instance->limited_slip_differential = enable;
}

void wbu_car_enable_indicator_auto_disabling(bool enable) {
  if (!_wbu_car_check_initialisation("wbu_car_init()", "wbu_car_enable_indicator_auto_disabling()"))
    return;
  instance->indicator_auto_disabling = enable;
}
