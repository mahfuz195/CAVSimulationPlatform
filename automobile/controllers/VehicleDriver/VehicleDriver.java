import com.cyberbotics.webots.controller.Robot;
import com.cyberbotics.webots.automobile.Driver;

public class VehicleDriver {
  public static void main(String[] args) {
    Driver driver = new Driver();
    driver.setCruisingSpeed(20.0);

    while (driver.step() != -1) {
      double angle = 0.3 * Math.cos(driver.getTime());
      driver.setSteeringAngle(angle);
    };
  }
}
