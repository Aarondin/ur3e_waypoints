from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    declared_arguments=[]
    declared_arguments.append(
        DeclareLaunchArgument(
            Node(
                package=...
                namespace=...
                executable=...
                name=...
                arguments=...
            )
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
        .robot_description(ParameterValue(Command([
            'xacro', str()]), name='ur3e'))
        .trajectory_execution(file_path='/opt/ros/rolling/share/ur_moveit_config/config/controllers.yaml')
        .robot_description_kinematics(file_path='/opt/ros/rolling/share/ur_moveit_config/config/kinematics.yaml')
        .planning_scene_monitor(publish_robot_description=True, publish_robot_description_semantic=True)
        .planning_pipelines(pipelines=["ompl"])
    ).to_moveit_configs() #.to_dict()?

    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["--frame-id", "world", "--child-frame-id", "base_link"],
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[moveit_config.robot_description],
    )

    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[ros2_controllers_path],
        remappings=[
            ("/controller_manager/robot_description", "/robot_description"),
        ],
        output="both",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", "-c", "/controller_manager"],
    )

    return LaunchDescription([
        base_launch,
        moveit_config,
        static_tf,
        robot_state_publisher,
        ros2_control_node,
        joint_state_broadcaster_spawner,
        arm_controller_spawner
    ])