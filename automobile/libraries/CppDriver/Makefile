space :=
space +=
WEBOTS_HOME_PATH=$(subst $(space),\ ,$(strip $(subst \,/,$(WEBOTS_HOME))))
include $(WEBOTS_HOME_PATH)/resources/Makefile.os.include

LIBRARY_SOURCES_PATH = ./src
LIBRARY_INCLUDE_PATH = ./include

CAR_LIBRARY_PATH = ../car
DRIVER_LIBRARY_PATH = ../driver

CXX_SOURCES = $(wildcard $(LIBRARY_SOURCES_PATH)/*.cpp)
INCLUDE = -I"$(WEBOTS_HOME)/include/controller/c" -I"$(LIBRARY_INCLUDE_PATH)" -I"$(DRIVER_LIBRARY_PATH)/include"
LIBRARIES = -L"$(CAR_LIBRARY_PATH)" -lcar -L"$(DRIVER_LIBRARY_PATH)" -ldriver 

include $(WEBOTS_HOME_PATH)/resources/Makefile.include
