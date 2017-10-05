%module automobile

%pragma(java) jniclasscode=%{
  static {
    try {
      System.loadLibrary("automobile");
    } catch (UnsatisfiedLinkError e) {
      System.err.println("Native code library failed to load. See the chapter on Dynamic Linking Problems in the SWIG Java documentation for help.\n" + e);
      System.exit(1);
    }
  }
%}

%{
#include <webots/Driver.hpp>
#include <webots/Car.hpp>
%}

%import "controller.i"

%typemap(javaimports) SWIGTYPE %{
import com.cyberbotics.webots.controller.Robot;
%}

%include <webots/Driver.hpp>
%include <webots/Car.hpp>
