#include <memory>
#include <fstream>
#include <string>
#include <vector>
#include <rclcpp/rclcpp.hpp>

#include <geometry_msgs/msg/pose.hpp>

#include <tf2/LinearMath/Quaternion.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

std::vector<std::vector<std::string>> csv_to_waypoints(const std::string& path) {
    std::vector<std::vector<std::string>> waypoints;
    std::ifstream file(path);

    if (!file.is_open()) {
        return waypoints;
    }

    std::string line;

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string field;
        std::vector<std::string> row;

        // Extract each field separated by a comma
        while (std::getline(ss, field, ',')) {
            row.push_back(field);
        }
        waypoints.push_back(row);
    }

    file.close();
    return waypoints;
}

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("ur_moveit_pub");

    RCLCPP_INFO(node->get_logger(), "Starting waypoint follower");
    
    std::string path = "/home/aaron/ur_ws/src/moveit_control/points_export(jet_waypoints_wings2).csv";
    std::vector<std::vector<std::string>> waypoints = csv_to_waypoints(path);

    auto move_group_interface = moveit::planning_interface::MoveGroupInterface(node, "manipulator");

    //moveit::planning_interface::MoveGroupInterface arm(node, "arm");

    for (const auto &waypoint : waypoints) {
        //std::vector<std::string> pose_euler = waypoints[i];
        tf2::Quaternion quat;
        //quat.setRPY(std::stod(pose_euler[3]),std::stod(pose_euler[4]),std::stod(pose_euler[5]));
        quat.setRPY(std::stod(waypoint[3]),std::stod(waypoint[4]),std::stod(waypoint[5]));
        
        auto target_pose = [&quat, &waypoint](){geometry_msgs::msg::Pose msg;
            msg.orientation.w = quat.getW();
            //msg.position.x = std::stod(pose_euler[0]);
            //msg.position.y = std::stod(pose_euler[1]);
            //msg.position.z = std::stod(pose_euler[2]);
            msg.position.x = std::stod(waypoint[0]);
            msg.position.y = std::stod(waypoint[1]);
            msg.position.z = std::stod(waypoint[2]);
        return msg;}();
        move_group_interface.setPoseTarget(target_pose);

        // Create a plan to that target pose
        auto const [success, plan] = [&move_group_interface](){
            moveit::planning_interface::MoveGroupInterface::Plan msg;
            auto const ok = static_cast<bool>(move_group_interface.plan(msg));
            return std::make_pair(ok, msg);
        }();

        // Execute the plan
        if(success) {
            move_group_interface.execute(plan);
        } else {
            RCLCPP_ERROR(node->get_logger(), "Planning failed!");
        }
    }

    RCLCPP_INFO(node->get_logger(), "CSV Sequence Complete");

    rclcpp::shutdown();
    return 0;
}
