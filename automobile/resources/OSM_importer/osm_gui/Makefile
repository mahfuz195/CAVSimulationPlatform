# Webots Makefile system 
#
# You may add some variable definitions hereafter to customize the build process
# See documentation in $(WEBOTS_HOME_PATH)/resources/Makefile.include

### Do not modify: this includes Webots global Makefile.include
include $(WEBOTS_HOME)/resources/Makefile.os.include

QT = core gui widgets network

CXX_SOURCES = main.cpp OSMImportWindow.cpp
HPP_FILES_TO_MOC = OSMImportWindow.hpp

ifneq ($(OSTYPE),windows)
CFLAGS = -fPIC
endif

CURDIR = controllers/osm_gui # hawful hack to generate an executable outside of the 'controllers' directory

space :=
space +=
WEBOTS_HOME_PATH=$(subst $(space),\ ,$(strip $(subst \,/,$(WEBOTS_HOME))))
include $(WEBOTS_HOME_PATH)/resources/Makefile.include
