/*
 * Description:   CPP wrapper of the driver library
 * Comments:      Sponsored by the CTI project RO2IVSim (http://transport.epfl.ch/simulator-for-mobile-robots-and-intelligent-vehicles)
 */

#include <webots/Driver.hpp>
#include <webots/driver.h>

using namespace webots;

Driver::Driver() {
  wbu_driver_init();
}

Driver::~Driver() {
  wbu_driver_cleanup();
}

int Driver::step() {
  return wbu_driver_step();
}

void Driver::setSteeringAngle(double steeringAngle) {
  wbu_driver_set_steering_angle(steeringAngle);
}

double Driver::getSteeringAngle() {
  return wbu_driver_get_steering_angle();
}

void Driver::setCruisingSpeed(double speed) {
  wbu_driver_set_cruising_speed(speed);
}

double Driver::getTargetCruisingSpeed() {
  return wbu_driver_get_target_cruising_speed();
}

double Driver::getCurrentSpeed() {
  return wbu_driver_get_current_speed();
}

void Driver::setThrottle(double throttle) {
  wbu_driver_set_throttle(throttle);
}

double Driver::getThrottle() {
  return wbu_driver_get_throttle();
}

void Driver::setBrakeIntensity(double intensity) {
  wbu_driver_set_brake_intensity(intensity);
}

double Driver::getBrakeIntensity() {
  return wbu_driver_get_brake_intensity();
}

void Driver::setBrake(double brake) {
  std::cerr << "Warning: Deprecated 'setBrake' use 'setBrakeIntensity' instead." << std::endl;
  setBrakeIntensity(brake);
}

void Driver::setIndicator(int state) {
  wbu_driver_set_indicator(state);
}

void Driver::setHazardFlashers(bool state) {
  wbu_driver_set_hazard_flashers(state);
}

int Driver::getIndicator() {
  return wbu_driver_get_indicator();
}

bool Driver::getHazardFlashers() {
  return wbu_driver_get_hazard_flashers();
}

void Driver::setDippedBeams(bool state) {
  wbu_driver_set_dipped_beams(state);
}

void Driver::setAntifogLights(bool state) {
  wbu_driver_set_antifog_lights(state);
}

bool Driver::getDippedBeams() {
  return wbu_driver_get_dipped_beams();
}

bool Driver::getAntifogLights() {
  return wbu_driver_get_antifog_lights();
}

double Driver::getRpm() {
  return wbu_driver_get_rpm();
}

int Driver::getGear() {
  return wbu_driver_get_gear();
}

void Driver::setGear(int gear) {
  wbu_driver_set_gear(gear);
}

int Driver::getGearNumber() {
  return wbu_driver_get_gear_number();
}

int Driver::getControlMode() {
  return wbu_driver_get_control_mode();
}

void Driver::setWipersMode(int mode) {
  wbu_driver_set_wipers_mode(mode);
}

int Driver::getWipersMode() {
  return wbu_driver_get_wipers_mode();
}
