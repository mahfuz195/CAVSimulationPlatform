.PHONY: release debug profile clean

release debug profile clean: controllers.Makefile plugins.Makefile resources.Makefile

controllers.Makefile: libraries.Makefile
	@echo "#"; echo "# *** controllers ***"
	+@make -s -C controllers $(MAKECMDGOALS)

plugins.Makefile:
	@echo "#"; echo "# *** robot windows ***"
	+@make -s -C plugins/robot_windows $(MAKECMDGOALS)

resources.Makefile:
	@echo "#"; echo "# *** resources ***"
	+@make -s -C resources $(MAKECMDGOALS)
	+@make -s -C resources/OSM_importer $(MAKECMDGOALS)

libraries.Makefile:
	@echo "#"; echo "# *** libraries ***"
	+@make -s -C libraries $(MAKECMDGOALS)
