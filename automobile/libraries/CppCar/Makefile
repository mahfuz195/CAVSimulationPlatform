space :=
space +=
WEBOTS_HOME_PATH=$(subst $(space),\ ,$(strip $(subst \,/,$(WEBOTS_HOME))))
include $(WEBOTS_HOME_PATH)/resources/Makefile.os.include

LIBRARY_SOURCES_PATH = ./src
LIBRARY_INCLUDE_PATH = ./include

CAR_LIBRARY_PATH = ../car
DRIVERCPP_LIBRARY_PATH = ../CppDriver

CXX_SOURCES = $(wildcard $(LIBRARY_SOURCES_PATH)/*.cpp)
INCLUDE = -I"$(WEBOTS_HOME)/include/controller/c" -I"$(LIBRARY_INCLUDE_PATH)" -I"$(CAR_LIBRARY_PATH)/include" -I"$(DRIVERCPP_LIBRARY_PATH)/include"
LIBRARIES = -L"$(CAR_LIBRARY_PATH)" -lcar

include $(WEBOTS_HOME_PATH)/resources/Makefile.include
