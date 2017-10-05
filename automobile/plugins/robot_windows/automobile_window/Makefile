# Webots Makefile system 
#
# You may add some variable definitions hereafter to customize the build process
# See documentation in $(WEBOTS_HOME_PATH)/resources/Makefile.include

space :=
space +=
WEBOTS_HOME_PATH=$(subst $(space),\ ,$(strip $(subst \,/,$(WEBOTS_HOME))))

ifndef WEBOTS_AUTOMOBILE_PATH
  WEBOTS_AUTOMOBILE_PATH = $(WEBOTS_HOME)/projects/automobile/libraries
endif

CXX_SOURCES = entry_points.cpp Viewer.cpp AbstractWidget.cpp GeneralInformationWidget.cpp SpeedWidget.cpp RPMWidget.cpp SteeringWidget.cpp EncodersWidget.cpp ThrottleWidget.cpp BrakeWidget.cpp OSMImportWidget.cpp
HPP_FILES_TO_MOC = GeneralInformationWidget.hpp AbstractWidget.hpp OSMImportWidget.hpp

QT = core gui widgets
USE_C_API = true

QT_UTILS = $(WEBOTS_HOME)/resources/projects/libraries/qt_utils
INCLUDE = -I"$(QT_UTILS)" -I"$(WEBOTS_AUTOMOBILE_PATH)/driver/include" -I"$(WEBOTS_AUTOMOBILE_PATH)/car/include"
LIBRARIES = -L"$(QT_UTILS)" -lqt_utils -L"$(WEBOTS_AUTOMOBILE_PATH)/driver" -ldriver -L"$(WEBOTS_AUTOMOBILE_PATH)/car" -lcar

include $(WEBOTS_HOME_PATH)/resources/Makefile.include
