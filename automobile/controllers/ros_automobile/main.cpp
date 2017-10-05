#include "RosAutomobile.hpp"

int main(int argc, char **argv)
{

  RosAutomobile *controller = new RosAutomobile();
  controller->run(argc, argv);
  delete controller;
  return 0;
}
