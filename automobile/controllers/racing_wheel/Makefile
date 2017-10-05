# Webots Makefile system 
#
# You may add some variable definitions hereafter to customize the build process
# See documentation in $(WEBOTS_HOME_PATH)/resources/Makefile.include

space :=
space +=
WEBOTS_HOME_PATH=$(subst $(space),\ ,$(strip $(subst \,/,$(WEBOTS_HOME))))

include $(WEBOTS_HOME_PATH)/resources/Makefile.os.include

ifeq ($(OSTYPE),linux)
CFLAGS = -fPIC
endif


ifndef WEBOTS_AUTOMOBILE_PATH
WEBOTS_AUTOMOBILE_PATH = $(WEBOTS_HOME)/projects/automobile/libraries
endif

INCLUDE = -I"$(WEBOTS_AUTOMOBILE_PATH)/CppDriver/include"
LIBRARIES = -L"$(WEBOTS_AUTOMOBILE_PATH)/driver" -ldriver -L"$(WEBOTS_AUTOMOBILE_PATH)/car" -lcar -L"$(WEBOTS_AUTOMOBILE_PATH)/CppDriver" -lCppDriver

QT = core
CXX_SOURCES = $(wildcard *.cpp)

# Do not modify the following: this includes Webots global Makefile.include
include $(WEBOTS_HOME_PATH)/resources/Makefile.include
