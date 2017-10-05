#include "OSMImportWindow.hpp"

#include <QtWidgets/QApplication>
#include <string.h>

int main(int argc, char *argv[]) {
  QDir libDir(qgetenv("WEBOTS_HOME") + "/lib/qt/plugins");
  QApplication::addLibraryPath(libDir.absolutePath()); // required for for loading libqxcb
  QApplication app(argc, argv);
  char scriptPath[512] = "";
  if (argc > 1)
    strcpy(scriptPath, argv[1]);

  OSMImportWindow window(scriptPath);
  window.show();
  return app.exec();
}
