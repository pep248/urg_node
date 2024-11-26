cmake_minimum_required(VERSION 3.5)
project(urg_node)

if(WIN32)
  message(WARNING "${PROJECT_NAME} is currently not supported on Windows")
  ament_package()
  return()
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake_auto REQUIRED)
find_package(Boost REQUIRED)  # Boost still needed explicitly for CRC component

ament_auto_find_build_dependencies()

# Create the library
ament_auto_add_library(urg_node SHARED
  src/urg_c_wrapper.cpp
  src/urg_node.cpp
)

# Register the component
rclcpp_components_register_node(urg_node
  PLUGIN "urg_node::UrgNode"
  EXECUTABLE urg_node_driver
)

# Create getID executable
ament_auto_add_executable(getID src/get_id.cpp)
target_link_libraries(getID urg_node)

# Install Python scripts
install(PROGRAMS 
  scripts/set_urg_ip.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install additional directories
install(
  DIRECTORY
    rviz
    meshes 
    urdf
    config
  DESTINATION
    share/${PROJECT_NAME}
)

ament_auto_package(INSTALL_TO_SHARE launch)