LIBRARIES=car.Makefile driver.Makefile CppDriver.Makefile CppCar.Makefile java.Makefile python.Makefile

.PHONY: release debug profile clean

release debug profile clean: $(LIBRARIES)

# list library dependencies

driver.Makefile: car.Makefile

CppDriver.Makefile: driver.Makefile

CppCar.Makefile: car.Makefile

java.Makefile: CppCar.Makefile CppDriver.Makefile

python.Makefile: CppCar.Makefile CppDriver.Makefile

%.Makefile:
	+@echo "# make" $(MAKECMDGOALS) $(@:.Makefile=)
	+@make -s -C $(@:.Makefile=) $(MAKECMDGOALS)
