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


SERVICE_FILES = $(wildcard include/srv/*.srv)
SERVICE_HEADERS = $(SERVICE_FILES:include/srv/%.srv=include/webots_ros/%.h)

include $(WEBOTS_HOME_PATH)/resources/Makefile.os.include

ifeq ($(OSTYPE),windows)
 CFLAGS = -Wno-unused-local-typedefs
endif

ifeq ($(OSTYPE),linux)
 CFLAGS = -Wno-unused-local-typedefs -Wno-deprecated-declarations -std=c++11
endif

ifeq ($(OSTYPE),darwin)
 USE_STD_CXX = true
endif

CXX_SOURCES = $(wildcard *.cpp)
CXX_SOURCES += $(wildcard $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/Ros*.cpp)

ifeq ($(OSTYPE),windows)
 ros_automobile.exe: $(CXX_SOURCES:.cxx=.d)
else
 ros_automobile: $(CXX_SOURCES:.cxx=.d)
endif

$(CXX_SOURCES:.cxx=.d): $(SERVICE_HEADERS) $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/include/templateHeader.h $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/include/templateRequest.h $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/include/templateResponse.h

include/webots_ros/%.h : include/srv/%.srv $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/include/templateHeader.h $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/include/templateRequest.h $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/include/templateResponse.h $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/headersFromSRV.py $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/headersGenerator.py
	@echo "# generating ROS header" $(notdir $<)
	$(SILENT)python $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/headersFromSRV.py $< $(WEBOTS_HOME_PATH)/projects/default/controllers/ros/include


INCLUDE = -I"include" -I"$(WEBOTS_HOME_PATH)/projects/default/controllers/ros" -I"$(WEBOTS_HOME_PATH)/projects/default/controllers/ros/include" -I"$(WEBOTS_AUTOMOBILE_PATH)/CppDriver/include" -I"$(WEBOTS_AUTOMOBILE_PATH)/CppCar/include"

LIBRARIES += -L"$(WEBOTS_AUTOMOBILE_PATH)/CppDriver" -lCppDriver -L"$(WEBOTS_AUTOMOBILE_PATH)/CppCar" -lCppCar -L"$(WEBOTS_AUTOMOBILE_PATH)/driver" -ldriver -L"$(WEBOTS_AUTOMOBILE_PATH)/car" -lcar


# include ros libraries

LIBRARIES += -L"$(WEBOTS_HOME_PATH)/projects/default/libraries/ros" -lroscpp -lrosconsole -lroscpp_serialization  -lrostime
ifeq ($(OSTYPE),windows)
 LIBRARIES += -lws2_32
 ifeq ($(MAKECMDGOALS),debug)
  # The following option is fixing the following error
  # appearing only on Windows 64 bits in debug mode
  # (probably that the number of templates is causing this)
  # RosSupervisor.o: too many sections
  CFLAGS += -Wa,-mbig-obj
 endif
endif

ifeq ($(OSTYPE),linux)
 LIBRARIES += -Wl,-rpath,"$(WEBOTS_HOME_PATH)/projects/default/libraries/ros"
endif

# Hide Boost warnings
ifeq ($(OSTYPE),darwin)
CFLAGS += -Wno-unused-local-typedefs
endif

FILES_TO_REMOVE += include/webots_ros

### Do not modify: this includes Webots global Makefile.include

space :=
space +=
WEBOTS_HOME_PATH=$(subst $(space),\ ,$(strip $(subst \,/,$(WEBOTS_HOME))))
include $(WEBOTS_HOME_PATH)/resources/Makefile.include
