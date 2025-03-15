cmake_minimum_required(VERSION 3.8)
project(roarm_camera)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

include_directories(
  include
)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)                                              
find_package(sensor_msgs REQUIRED)                                                                             
find_package(OpenCV REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(ament_index_cpp REQUIRED)
find_package(yaml-cpp REQUIRED)

###### NODES ######
add_executable(roarm_camera_node src/main.cpp src/roarm_camera_node.cpp)
ament_target_dependencies(roarm_camera_node rclcpp sensor_msgs OpenCV cv_bridge image_transport yaml-cpp)      
target_link_libraries(roarm_camera_node ${OpenCV_LIBS} yaml-cpp)

install(TARGETS
  roarm_camera_node
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY 
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
