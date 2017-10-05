/*
 * Description:   CPP wrapper of the car library
 * Comments:      Sponsored by the CTI project RO2IVSim (http://transport.epfl.ch/simulator-for-mobile-robots-and-intelligent-vehicles)
 */

#include <webots/Car.hpp>
#include <webots/car.h>

using namespace webots;

int Car::getType() {
  return wbu_car_get_type();
}

int Car::getEngineType() {
  return wbu_car_get_engine_type();
}

void Car::setIndicatorPeriod(double period) {
  wbu_car_set_indicator_period(period);
}

double Car::getIndicatorPeriod() {
  return wbu_car_get_indicator_period();
}

bool Car::getBackwardsLights() {
  return wbu_car_get_backwards_lights();
}

bool Car::getBrakeLights() {
  return wbu_car_get_brake_lights();
}

double Car::getTrackFront() {
  return wbu_car_get_track_front();
}

double Car::getTrackRear() {
  return wbu_car_get_track_rear();
}

double Car::getWheelbase() {
  return wbu_car_get_wheelbase();
}

double Car::getFrontWheelRadius() {
  return wbu_car_get_front_wheel_radius();
}

double Car::getRearWheelRadius() {
  return wbu_car_get_rear_wheel_radius();
}

double Car::getWheelEncoder(int wheel) {
  return wbu_car_get_wheel_encoder(wheel);
}

double Car::getWheelSpeed(int wheel) {
  return wbu_car_get_wheel_speed(wheel);
}

double Car::getRightSteeringAngle() {
  return wbu_car_get_right_steering_angle();
}

double Car::getLeftSteeringAngle() {
  return wbu_car_get_left_steering_angle();
}

void Car::enableLimitedSlipDifferential(bool enable) {
  wbu_car_enable_limited_slip_differential(enable);
}

void Car::enableIndicatorAutoDisabling(bool enable) {
  wbu_car_enable_indicator_auto_disabling(enable);
}
