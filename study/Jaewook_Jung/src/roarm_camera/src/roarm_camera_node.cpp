#include "roarm_camera/roarm_camera_node.hpp"


RoarmCameraNode::RoarmCameraNode() 
  : Node("roarm_camera_node")
{
    rclcpp::QoS qos(rclcpp::KeepLast(10));
    qos.best_effort();

    pub_camera_raw_ = this->create_publisher<sensor_msgs::msg::Image>("/roarm/vision/image_raw", qos);
    pub_camera_info_ = this->create_publisher<sensor_msgs::msg::CameraInfo>("/roarm/vision/camera_info", 10);
    
    // 필요한 파라미터 선언 (기본값 설정)
    this->declare_parameter<int>("width", 0);
    this->declare_parameter<int>("height", 0);
    this->declare_parameter<bool>("visualize", false);
    this->declare_parameter<std::string>("device", "");
    this->declare_parameter<int>("exposure", 0);
    this->declare_parameter<std::vector<double>>("camera_matrix", std::vector<double>());
    this->declare_parameter<std::vector<double>>("distortion_coefficients", std::vector<double>());
    this->declare_parameter<std::vector<double>>("rectification_matrix", std::vector<double>());
    this->declare_parameter<std::vector<double>>("projection_matrix", std::vector<double>());

    // config.yaml 파일에서 파라미터를 직접 불러오기
    std::string pkg_share_dir = ament_index_cpp::get_package_share_directory("roarm_camera");
    std::string config_file = pkg_share_dir + "/config/params.yaml";
    loadConfigFromFile(config_file);
    
    cap_.open(device_, cv::CAP_V4L2);
    if (!cap_.isOpened()) {
      RCLCPP_ERROR(this->get_logger(), "Failed to open camera");
      return;
    }

    cap_.set(cv::CAP_PROP_FOURCC, cv::VideoWriter::fourcc('M', 'J', 'P', 'G'));
    cap_.set(cv::CAP_PROP_FRAME_WIDTH, width_);
    cap_.set(cv::CAP_PROP_FRAME_HEIGHT, height_);
    cap_.set(cv::CAP_PROP_EXPOSURE, exposure_);

    // 30 fps
    timer_ = this->create_wall_timer(33ms, std::bind(&RoarmCameraNode::timerCallback, this));
}

RoarmCameraNode::~RoarmCameraNode()
{
    if (cap_.isOpened()) {
        cap_.release();
    }
    cv::destroyAllWindows();
}

// 파라미터 값들을 파일에서 불러오기
void RoarmCameraNode::loadConfigFromFile(const std::string &file_path)
{
  try {
    // YAML 파일 로드
    YAML::Node base = YAML::LoadFile(file_path);
    YAML::Node config;

    // camera_pub 내의 ros__parameters가 있으면 그 내부를 사용
    if (base["roarm_camera_node"] && base["roarm_camera_node"]["ros__parameters"])
      config = base["roarm_camera_node"]["ros__parameters"];
    else
      config = base;

    if (config["image_width"]) {
      width_ = config["image_width"].as<int>();
      this->set_parameter(rclcpp::Parameter("width", width_));
    }
    if (config["image_height"]) {
      height_ = config["image_height"].as<int>();
      this->set_parameter(rclcpp::Parameter("height", height_));
    }
    if (config["visualize"]) {
      visualize_ = config["visualize"].as<bool>();
      this->set_parameter(rclcpp::Parameter("visualize", visualize_));
    }
    if (config["device"]) {
      device_ = config["device"].as<std::string>();
      this->set_parameter(rclcpp::Parameter("device", device_));
    }
    if (config["exposure"]) {
      exposure_ = config["exposure"].as<int>();
      this->set_parameter(rclcpp::Parameter("exposure", exposure_));
    }

    // 매트릭스 파라미터는 "data" 시퀀스를 직접 파싱
    if (config["camera_matrix"] && config["camera_matrix"]["data"]) {
      camera_matrix_ = parseDoubleVector(config["camera_matrix"]["data"]);
      this->set_parameter(rclcpp::Parameter("camera_matrix", camera_matrix_));
    }
    if (config["distortion_coefficients"] && config["distortion_coefficients"]["data"]) {
      distortion_coefficients_ = parseDoubleVector(config["distortion_coefficients"]["data"]);
      this->set_parameter(rclcpp::Parameter("distortion_coefficients", distortion_coefficients_));
    }
    if (config["rectification_matrix"] && config["rectification_matrix"]["data"]) {
      rectification_matrix_ = parseDoubleVector(config["rectification_matrix"]["data"]);
      this->set_parameter(rclcpp::Parameter("rectification_matrix", rectification_matrix_));
    }
    if (config["projection_matrix"] && config["projection_matrix"]["data"]) {
      projection_matrix_ = parseDoubleVector(config["projection_matrix"]["data"]);
      this->set_parameter(rclcpp::Parameter("projection_matrix", projection_matrix_));
    }
    
    RCLCPP_INFO_STREAM(this->get_logger(),
      "\n[DEBUG] Loaded Parameters:" << "\n"
      << " width: " << width_ << "\n"
      << " height: " << height_ << "\n"
      << " visualize: " << (visualize_ ? "true" : "false") << "\n"
      << " device: " << device_ << "\n"
      << " exposure: " << exposure_ << "\n"
      << " camera_matrix: " << vectorToString(camera_matrix_) << "\n"
      << " distortion_coefficients: " << vectorToString(distortion_coefficients_) << "\n"
      << " rectification_matrix: " << vectorToString(rectification_matrix_) << "\n"
      << " projection_matrix: " << vectorToString(projection_matrix_) << "\n"
    );
  } catch (const std::exception &e) {
    RCLCPP_ERROR(this->get_logger(), "Error loading config file: %s", e.what());
  }
}
// 디버깅 출력 용도(1)
std::vector<double> RoarmCameraNode::parseDoubleVector(const YAML::Node &node) {
  std::vector<double> vec;
  if (node && node.IsSequence()) {
    for (size_t i = 0; i < node.size(); ++i) {
      vec.push_back(node[i].as<double>());
    }
  }
  return vec;
}
// 디버깅 출력 용도(2)
std::string RoarmCameraNode::vectorToString(const std::vector<double> &vec) {
  std::ostringstream oss;
  oss << "[";
  for (size_t i = 0; i < vec.size(); ++i) {
    oss << vec[i];
    if (i != vec.size() - 1)
      oss << ", ";
  }
  oss << "]";
  return oss.str();
}

void RoarmCameraNode::timerCallback()
{
  cv::Mat frame;
  cap_ >> frame;
  
  if (frame.empty()) {
    RCLCPP_ERROR(this->get_logger(), "Failed to capture image");
    return;
  }

  if (width_ == 0 || height_ == 0) {
    RCLCPP_ERROR(this->get_logger(), "Width or height is not set");
    return;
  }
  
  cv::resize(frame, frame, cv::Size(width_, height_));

  // ROS 이미지 메시지 생성
  auto img_msg = cv_bridge::CvImage(std_msgs::msg::Header(), "bgr8", frame).toImageMsg();
  // auto img_msg = cv_bridge::CvImage(std_msgs::msg::Header(), "bgr8", frame).toCompressedImageMsg();

  img_msg->header.frame_id = "camera_frame";
  img_msg->header.stamp = this->now();                          

  pub_camera_raw_->publish(*img_msg);

  // CameraInfo 메시지에 매트릭스 데이터 설정
  sensor_msgs::msg::CameraInfo camera_info_msg;
  camera_info_msg.header.stamp = img_msg->header.stamp;         
  camera_info_msg.width = width_;
  camera_info_msg.height = height_;

  // config.yaml 파일로부터 성공적으로 매트릭스 데이터를 불러온 경우에만 메시지에 설정
  // std::vector<double>에서 std::array<double, N>로 변환
  if (!camera_matrix_.empty() && camera_matrix_.size() >= 9) {
    std::copy_n(camera_matrix_.begin(), 9, camera_info_msg.k.begin());
  }
  if (!rectification_matrix_.empty() && rectification_matrix_.size() >= 9) {
    std::copy_n(rectification_matrix_.begin(), 9, camera_info_msg.r.begin());
  }
  if (!projection_matrix_.empty() && projection_matrix_.size() >= 12) {
    std::copy_n(projection_matrix_.begin(), 12, camera_info_msg.p.begin());
  }
  if (!distortion_coefficients_.empty()) {
    camera_info_msg.d = {distortion_coefficients_.begin(), distortion_coefficients_.end()};
  }
  
  pub_camera_info_->publish(camera_info_msg);

  if (visualize_ == true)
  {
    cv::imshow("Camera Frame", frame);
    cv::waitKey(1); // millis second
  }
}
