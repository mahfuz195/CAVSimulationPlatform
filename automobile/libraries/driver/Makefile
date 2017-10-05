space :=
space +=
WEBOTS_HOME_PATH=$(subst $(space),\ ,$(strip $(subst \,/,$(WEBOTS_HOME))))
include $(WEBOTS_HOME_PATH)/resources/Makefile.os.include

LIBRARY_SOURCES_PATH = ./src
LIBRARY_INCLUDE_PATH = ./include

CAR_INCLUDE_PATH         = ../car/include
CAR_PRIVATE_INCLUDE_PATH = ../car/src
CAR_LIBRARY_PATH         = ../car

C_SOURCES = $(wildcard $(LIBRARY_SOURCES_PATH)/*.c)
INCLUDE = -I"$(LIBRARY_INCLUDE_PATH)" -I"$(CAR_INCLUDE_PATH)" -I"$(CAR_PRIVATE_INCLUDE_PATH)"
LIBRARIES = -L"$(CAR_LIBRARY_PATH)" -lcar

include $(WEBOTS_HOME_PATH)/resources/Makefile.include
