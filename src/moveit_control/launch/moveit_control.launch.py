from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    declared_arguments=[]
    declared_arguments.append(
        DeclareLaunchArgument(

        )
    )

    base_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource("/opt/ros/rolling/share/ur_moveit_config/launch/ur_moveit.launch.py")
        launch_arguments={
            "ur_type": "ur3e"
            "launch_rviz": true
        }.items(),
    )

    moveit_config = (
        MoveItConfigsBuilder("")
        .robot_description(file_path="/opt/ros/humble/share/ur_description/urdf")   #urdf or ros2_control?
    ).to_moveit_configs() #.to_dict()?

    return LaunchDescription(declared_arguments + [base_launch])