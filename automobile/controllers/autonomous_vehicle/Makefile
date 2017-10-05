# Webots Makefile system 
#
# You may add some variable definitions hereafter to customize the build process
# See documentation in $(WEBOTS_HOME_PATH)/resources/Makefile.include


CXX_SOURCES = autonomous_vehicle.cpp
USE_C_API = true

### Do not modify: this includes Webots global Makefile.include
space :=
space +=

ifndef WEBOTS_AUTOMOBILE_PATH
WEBOTS_AUTOMOBILE_PATH = $(WEBOTS_HOME)/projects/automobile/libraries
endif

INCLUDE = -I"$(WEBOTS_AUTOMOBILE_PATH)/driver/include"
LIBRARIES = -L"$(WEBOTS_AUTOMOBILE_PATH)/driver" -ldriver -L"$(WEBOTS_AUTOMOBILE_PATH)/car" -lcar

##INCLUDE = -I"C:/opencv/opencv/build/include"
##LIBRARIES = -L"C:/opencv/opencv/build/x64/vc14/lib" -lopencv



##INCLUDE= -I"C:/opencv/include"
##LIBRARIES = -L"C:/opencv/opencv/build/x64/vc14/lib" -lopencv
###LIBRARIES=-L"C:\opencv\lib" -lcv210 -lcvaux210 -lcxcore210 -lcxts210 -lhighgui210 -lml210 -lopencv_ffmpeg210

WEBOTS_HOME_PATH=$(subst $(space),\ ,$(strip $(subst \,/,$(WEBOTS_HOME))))
include $(WEBOTS_HOME_PATH)/resources/Makefile.include
