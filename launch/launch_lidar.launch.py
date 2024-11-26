from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    # Paths
    urg_node_launch_file = PathJoinSubstitution([
        FindPackageShare("urg_node"),
        "launch",
        "urg_node_launch.py"
    ])
    
    urdf_file = PathJoinSubstitution([
        FindPackageShare("urg_node"),
        "urdf",
        "hokuyo_laser.urdf"
    ])
    
    rviz_config = PathJoinSubstitution([
        FindPackageShare("urg_node"),
        "rviz",
        "rviz.rviz"
    ])

    # Launch Description
    return LaunchDescription([
        # Static Transform Publisher
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['--x', '0', '--y', '0', '--z', '0',
                      '--roll', '0', '--pitch', '0', '--yaw', '0',
                      '--frame-id', 'world',
                      '--child-frame-id', 'laser'],
            output='screen'
        ),
        
        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            arguments=[urdf_file]
        ),
        
        # Include URG Node Launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution([
                FindPackageShare("urg_node"),
                "launch",
                "urg_node.launch.py"]))
        ),
        
        
        # RViz with Config
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            output='screen'
        )
    ])
