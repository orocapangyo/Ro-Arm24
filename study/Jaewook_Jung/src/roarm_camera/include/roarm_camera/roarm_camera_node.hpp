#ifndef ROARM_CAMERA_NODE_HPP
#define ROARM_CAMERA_NODE_HPP

#include <chrono>             
#include <functional>         
#include <memory>
#include <sstream>
#include "rclcpp/rclcpp.hpp"     
#include "yaml-cpp/yaml.h"
#include "cv_bridge/cv_bridge.h"
#include "opencv2/opencv.hpp"
#include "image_transport/image_transport.hpp" 
#include "sensor_msgs/msg/image.hpp"
#include "sensor_msgs/msg/camera_info.hpp"
#include "ament_index_cpp/get_package_share_directory.hpp"
// #include "sensor_msgs/msg/compressed_image.hpp"

using namespace std::chrono_literals; 

class RoarmCameraNode : public rclcpp::Node   
{
    public:
      RoarmCameraNode();
      ~RoarmCameraNode();

    private:
      void timerCallback();
      void loadConfigFromFile(const std::string& filename);
      std::vector<double> parseDoubleVector(const YAML::Node &node);
      std::string vectorToString(const std::vector<double> &vec); 

      int width_;
      int height_;
      bool visualize_;
      int exposure_;

      cv::VideoCapture cap_;
      std::string device_;
      std::vector<double> camera_matrix_;
      std::vector<double> distortion_coefficients_;
      std::vector<double> rectification_matrix_;
      std::vector<double> projection_matrix_;

      rclcpp::TimerBase::SharedPtr timer_;
      rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_camera_raw_;
      rclcpp::Publisher<sensor_msgs::msg::CameraInfo>::SharedPtr pub_camera_info_;
      // rclcpp::Publisher<sensor_msgs::msg::CompressedImage>::SharedPtr pub_camera_raw_;
};

#endif // ROARM_CAMERA_NODE_HPP 