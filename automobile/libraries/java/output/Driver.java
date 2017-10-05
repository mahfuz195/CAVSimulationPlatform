/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 3.0.12
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.cyberbotics.webots.automobile;

import com.cyberbotics.webots.controller.Robot;

public class Driver extends Robot {
  private transient long swigCPtr;

  protected Driver(long cPtr, boolean cMemoryOwn) {
    super(automobileJNI.Driver_SWIGUpcast(cPtr), cMemoryOwn);
    swigCPtr = cPtr;
  }

  protected static long getCPtr(Driver obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if (swigCPtr != 0) {
      if (swigCMemOwn) {
        swigCMemOwn = false;
        automobileJNI.delete_Driver(swigCPtr);
      }
      swigCPtr = 0;
    }
    super.delete();
  }

  public Driver() {
    this(automobileJNI.new_Driver(), true);
  }

  public int step() {
    return automobileJNI.Driver_step(swigCPtr, this);
  }

  public void setSteeringAngle(double steeringAngle) {
    automobileJNI.Driver_setSteeringAngle(swigCPtr, this, steeringAngle);
  }

  public double getSteeringAngle() {
    return automobileJNI.Driver_getSteeringAngle(swigCPtr, this);
  }

  public void setCruisingSpeed(double speed) {
    automobileJNI.Driver_setCruisingSpeed(swigCPtr, this, speed);
  }

  public double getTargetCruisingSpeed() {
    return automobileJNI.Driver_getTargetCruisingSpeed(swigCPtr, this);
  }

  public double getCurrentSpeed() {
    return automobileJNI.Driver_getCurrentSpeed(swigCPtr, this);
  }

  public void setThrottle(double throttle) {
    automobileJNI.Driver_setThrottle(swigCPtr, this, throttle);
  }

  public double getThrottle() {
    return automobileJNI.Driver_getThrottle(swigCPtr, this);
  }

  public void setBrakeIntensity(double intensity) {
    automobileJNI.Driver_setBrakeIntensity(swigCPtr, this, intensity);
  }

  public double getBrakeIntensity() {
    return automobileJNI.Driver_getBrakeIntensity(swigCPtr, this);
  }

  public void setIndicator(int state) {
    automobileJNI.Driver_setIndicator(swigCPtr, this, state);
  }

  public void setHazardFlashers(boolean state) {
    automobileJNI.Driver_setHazardFlashers(swigCPtr, this, state);
  }

  public int getIndicator() {
    return automobileJNI.Driver_getIndicator(swigCPtr, this);
  }

  public boolean getHazardFlashers() {
    return automobileJNI.Driver_getHazardFlashers(swigCPtr, this);
  }

  public void setDippedBeams(boolean state) {
    automobileJNI.Driver_setDippedBeams(swigCPtr, this, state);
  }

  public void setAntifogLights(boolean state) {
    automobileJNI.Driver_setAntifogLights(swigCPtr, this, state);
  }

  public boolean getDippedBeams() {
    return automobileJNI.Driver_getDippedBeams(swigCPtr, this);
  }

  public boolean getAntifogLights() {
    return automobileJNI.Driver_getAntifogLights(swigCPtr, this);
  }

  public double getRpm() {
    return automobileJNI.Driver_getRpm(swigCPtr, this);
  }

  public int getGear() {
    return automobileJNI.Driver_getGear(swigCPtr, this);
  }

  public void setGear(int gear) {
    automobileJNI.Driver_setGear(swigCPtr, this, gear);
  }

  public int getGearNumber() {
    return automobileJNI.Driver_getGearNumber(swigCPtr, this);
  }

  public int getControlMode() {
    return automobileJNI.Driver_getControlMode(swigCPtr, this);
  }

  public void setWipersMode(int mode) {
    automobileJNI.Driver_setWipersMode(swigCPtr, this, mode);
  }

  public int getWipersMode() {
    return automobileJNI.Driver_getWipersMode(swigCPtr, this);
  }

  public void setBrake(double brake) {
    automobileJNI.Driver_setBrake(swigCPtr, this, brake);
  }

  public final static int INDICATOR_OFF = 0;
  public final static int INDICATOR_RIGHT = INDICATOR_OFF + 1;
  public final static int INDICATOR_LEFT = INDICATOR_RIGHT + 1;

  public final static int SPEED = 0;
  public final static int TORQUE = SPEED + 1;

  public final static int DOWN = 0;
  public final static int SLOW = DOWN + 1;
  public final static int NORMAL = SLOW + 1;
  public final static int FAST = NORMAL + 1;

}
