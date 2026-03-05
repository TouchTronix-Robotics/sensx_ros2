from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument("port", default_value="/dev/ttyUSB0"),
            DeclareLaunchArgument("baud", default_value="921600"),
            DeclareLaunchArgument("rows", default_value="20"),
            DeclareLaunchArgument("cols", default_value="8"),
            DeclareLaunchArgument("max_value", default_value="4095"),
            Node(
                package="tactile_module",
                executable="tactile_pub",
                name="sensor_publisher",
                output="screen",
                parameters=[
                    {
                        "port": LaunchConfiguration("port"),
                        "baud": LaunchConfiguration("baud"),
                        "rows": LaunchConfiguration("rows"),
                        "cols": LaunchConfiguration("cols"),
                        "max_value": LaunchConfiguration("max_value"),
                    }
                ],
            ),
        ]
    )
