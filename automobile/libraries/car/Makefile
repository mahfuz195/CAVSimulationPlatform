space :=
space +=
WEBOTS_HOME_PATH=$(subst $(space),\ ,$(strip $(subst \,/,$(WEBOTS_HOME))))
include $(WEBOTS_HOME_PATH)/resources/Makefile.os.include

LIBRARY_SOURCES_PATH = ./src
LIBRARY_INCLUDE_PATH = ./include

C_SOURCES = $(wildcard $(LIBRARY_SOURCES_PATH)/*.c)
INCLUDE = -I"$(LIBRARY_INCLUDE_PATH)"

include $(WEBOTS_HOME_PATH)/resources/Makefile.include
