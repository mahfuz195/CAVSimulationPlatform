TARGETS=autonomous_vehicle.Makefile ros_automobile.Makefile racing_wheel.Makefile VehicleDriver.Makefile

.PHONY: release debug profile clean

release debug profile clean: $(TARGETS)

%.Makefile:
	+@echo "# make" $(MAKECMDGOALS) $(@:.Makefile=)
	+@make -s -C $(@:.Makefile=) $(MAKECMDGOALS)
