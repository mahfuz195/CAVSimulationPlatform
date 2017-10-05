WEBOTS_PATH = ../../../..

include $(WEBOTS_PATH)/resources/Makefile.os.include

MODULE_NAME = automobile

INTERFACE = $(MODULE_NAME).i
SOURCE_HEADERS = $(wildcard ../CppDriver/include/webots/*.hpp) $(wildcard ../CppCar/include/webots/*.hpp)
JAVA_FILES = Driver.java Car.java automobile.java automobileJNI.java

WRAPPER = $(MODULE_NAME).cpp
WRAPPER_OBJECT = $(WRAPPER:.cpp=.o)
JAR = $(MODULE_NAME).jar
INCLUDES = -I"../CppDriver/include/" -I"../CppCar/include/" -I"../../../../include/controller/c/" -I"../../../../include/controller/cpp/"
LIB = -L"../CppCar" -lCppCar -L"../CppDriver" -lCppDriver

SWIG_OUTPUT = output
MODULE_PATH  = com/cyberbotics/webots/automobile
JAVA_SOURCES = $(addprefix $(SWIG_OUTPUT)/,$(JAVA_FILES))

ifeq ($(OSTYPE),linux)
JAVA_INCLUDES = -I"$(JAVA_HOME)/include" -I"$(JAVA_HOME)/include/linux"
CFLAGS2       = -c -Wall -Wno-unused-function -fPIC
LIBRARY       = libautomobile.so
LIB          += -L"$(WEBOTS_PATH)/lib" -lController -lCppController
endif

ifeq ($(OSTYPE),windows)
JAVA_INCLUDES = -I"$(JAVA_HOME)/include" -I"$(JAVA_HOME)/include/win32"
CFLAGS2       = -c -Wall -Wno-unused-function -O
LIBRARY       = automobile.dll
LIB          += -L"$(WEBOTS_PATH)/msys64/mingw64/bin" -lController -lCppController
endif

ifeq ($(OSTYPE),darwin)
JAVA_INCLUDES = -I"$(MACOSX_SDK_PATH)/System/Library/Frameworks/JavaVM.framework/Versions/Current/Headers"
CFLAGS1 = -isysroot $(MACOSX_SDK_PATH) -mmacosx-version-min=$(MACOSX_MIN_SDK_VERSION) -stdlib=libc++ -Wl,-rpath,@loader_path/$(WEBOTS_PATH)
CFLAGS2 = -c -Wall -isysroot $(MACOSX_SDK_PATH) -mmacosx-version-min=$(MACOSX_MIN_SDK_VERSION) -stdlib=libc++ -Wno-unused-function
LIBRARY = libautomobile.jnilib
LIB    += -L"$(WEBOTS_PATH)/lib" -lController -lCppController
endif

.PHONY: JAVA_CLASSES all

all release debug profile: $(JAR) $(LIBRARY)

$(JAR): JAVA_CLASSES
	@jar cfv $@ $(MODULE_PATH)/*.class > /dev/null

JAVA_CLASSES: $(JAVA_SOURCES)
	@javac -target 1.8 -classpath "$(WEBOTS_PATH)/lib/Controller.jar" $(JAVA_SOURCES) -d .

$(JAVA_SOURCES): $(WRAPPER)

$(WRAPPER): $(INTERFACE) $(SOURCE_HEADERS)
	@mkdir -p $(SWIG_OUTPUT)
	@swig -c++ -java -package $(subst /,.,$(MODULE_PATH)) -outdir $(SWIG_OUTPUT) -I$(WEBOTS_PATH)/resources/languages/java/ $(INCLUDES) -o $@ $<

$(WRAPPER_OBJECT): $(WRAPPER)
	@$(CXX) $(CFLAGS2) $(INCLUDES) $(JAVA_INCLUDES) $< -o $@

%.so: $(WRAPPER_OBJECT)
	@$(CXX) -shared $< $(LIB) -o $@

%.dll: $(WRAPPER_OBJECT)
	@$(CXX)  -shared -mwindows -Wl,--add-stdcall-alias -Wl,--enable-auto-import -O -lm $< $(LIB) -o $@

%.jnilib: $(WRAPPER_OBJECT)
	@$(CXX) $(CFLAGS1) -bundle $< $(LIB) -o $@

clean:
	@rm -fr com $(SWIG_OUTPUT) $(JAR) $(WRAPPER) $(LIBRARY) $(WRAPPER_OBJECT)
