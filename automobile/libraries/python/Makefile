WEBOTS_PATH = ../../../..

include $(WEBOTS_PATH)/resources/Makefile.os.include

MODULE_NAME = automobile

INTERFACE          = $(MODULE_NAME).i
SOURCE_HEADERS     = $(wildcard ../CppDriver/include/webots/*.hpp) $(wildcard ../CppCar/include/webots/*.hpp)
SWIG               = swig
SWIG_OPTS          = -c++ -python -outdir "." -I../../../../resources/languages/python/
WRAPPER            = $(MODULE_NAME).cpp
WRAPPER_OBJECT     = $(WRAPPER:.cpp=.o)
PYOUT              = $(MODULE_NAME).py
PYTHON_VERSION    ?= 2.7
INCLUDES           = -I"../CppDriver/include/" -I"../CppCar/include/" -I"../../../../include/controller/c/" -I"../../../../include/controller/cpp/"
LIB                = -L"../CppCar" -lCppCar -L"../CppDriver" -lCppDriver


ifeq ($(OSTYPE),linux)
C_FLAGS         = -c -Wall -fPIC -Wno-unused-but-set-variable
LD_FLAGS        = -shared
LIBRARY         = _$(MODULE_NAME).so
PYTHON_INCLUDES = -I"/usr/include/python$(PYTHON_VERSION)"
LIB            += -L"$(WEBOTS_PATH)/lib" -lController -lCppController
endif

ifeq ($(OSTYPE),windows)
ifndef PYTHON_HOME
$(error PYTHON_HOME is not defined => "export PYTHON_HOME=/C/Python27")
endif
C_FLAGS         = -c -O -Wall -DMS_WIN64
LD_FLAGS        = -shared -Wl,--enable-auto-import
LIBRARY         = _$(MODULE_NAME).pyd
PYTHON_INCLUDES = -I$(PYTHON_HOME)/include
LIB            += -L"$(WEBOTS_PATH)/msys64/mingw64/bin" -lController -lCppController -L$(PYTHON_HOME)/libs -lpython27
endif

ifeq ($(OSTYPE),darwin)

PYTHON_PATH ?= /System/Library/Frameworks/Python.framework/Versions/$(PYTHON_VERSION)

C_FLAGS         = -c -Wall -fPIC -mmacosx-version-min=$(MACOSX_MIN_SDK_VERSION) -stdlib=libc++
ifeq ($(findstring llvm-g++,$(shell ls -lF $(shell which c++))),)
C_FLAGS        += -Wno-self-assign
endif
LD_FLAGS        = -dynamiclib -install_name @rpath/lib/python/_$(INTERFACE:.i=.so) -Wl,-rpath,@loader_path/$(WEBOTS_PATH) -compatibility_version 1.0 -current_version 1.0.0 -mmacosx-version-min=$(MACOSX_MIN_SDK_VERSION) -stdlib=libc++
PYTHON_INCLUDES = -I$(PYTHON_PATH)/Headers
LIB            += -L"$(WEBOTS_PATH)/lib" -lController -lCppController -L"$(PYTHON_PATH)/lib" -lpython$(PYTHON_VERSION)
LIBRARY         = _$(MODULE_NAME).so
endif

TARGET = $(PYOUT) $(LIBRARY)

release debug profile: $(TARGET)

$(PYOUT) $(WRAPPER):$(INTERFACE) $(SOURCE_HEADERS)
	$(SWIG) $(SWIG_OPTS) $(INCLUDES) -o $(WRAPPER) $<

$(LIBRARY):$(WRAPPER_OBJECT)
	$(CXX) $(LD_FLAGS) $< $(DEF) $(LIB) -o "$@"

$(WRAPPER_OBJECT):$(WRAPPER)
	$(CXX) $(C_FLAGS) $(INCLUDES) $(PYTHON_INCLUDES) $< -o $@

clean:
	@rm -fr $(WRAPPER) $(WRAPPER_OBJECT) $(PYOUT) $(LIBRARY)
