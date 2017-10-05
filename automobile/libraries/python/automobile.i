%module automobile

%{
#include <webots/DifferentialWheels.hpp> // avoid '‘DifferentialWheels’ is not a member of ‘webots’' error
#include <webots/Supervisor.hpp>         // avoid '‘Supervisor’ is not a member of ‘webots’' error
#include <webots/Driver.hpp>
#include <webots/Car.hpp>
%}

%import "controller.i"

%include <webots/Driver.hpp>
%include <webots/Car.hpp>
