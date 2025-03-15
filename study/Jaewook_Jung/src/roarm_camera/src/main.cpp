#include "roarm_camera/roarm_camera_node.hpp"

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<RoarmCameraNode>();
  rclcpp::spin(node); 
  rclcpp::shutdown();
  return 0;
}
