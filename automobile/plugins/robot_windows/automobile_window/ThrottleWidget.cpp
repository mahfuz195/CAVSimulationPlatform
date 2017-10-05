#include "ThrottleWidget.hpp"

#include <graph2d/Point2D.hpp>

#include <webots/driver.h>
#include <webots/robot.h>

using namespace std;

ThrottleWidget::ThrottleWidget(QWidget *parent): AbstractWidget(parent)
{
  mGraph->setYLabel("Throttle [%]");
}

ThrottleWidget::~ThrottleWidget() {
}

void ThrottleWidget::update() {
  if (!mEnableCheckBox->isChecked())
    return;

  if (wbu_driver_get_control_mode() == TORQUE) {
    double throttle = wbu_driver_get_throttle();
    mValueLabel->setText(QString::number(throttle, 'f', 3));
    mGraph->addPoint2D(Point2D(wb_robot_get_time(), throttle));
    mGraph->updateXRange();
    mGraph->extendYRange();
    mGraph->keepNPoints(pointsKeptNumber());
  } else
    mValueLabel->setText("No engine model in speed control");
}
