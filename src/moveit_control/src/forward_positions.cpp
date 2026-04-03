#include <chrono>
#include <iostream>
#include <fstream>
#include <sstream>
#include <rclcpp/rclcpp.hpp>

#include <std_msgs/msg/float64_multi_array.hpp>
#include <tf2/LinearMath/Quaternion.h>

std::vector<std::vector<double>> csv_to_waypoints(const std::string& path) {
    std::vector<std::vector<double>> waypoints;
    //std::vector<std::vector<double>> waypoints;
    std::ifstream file(path);

    if (!file.is_open()) {
        return waypoints;
    }

    std::string line;

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string field;
        std::vector<double> row;

        while (std::getline(ss, field, ',')) {
            row.push_back(std::stod(field));
        }
        waypoints.push_back(row);
    }

    file.close();
    return waypoints;
}

class ForwardPublisher : public rclcpp::Node
{
    public:
        ForwardPublisher(std::vector<std::vector<double>>& path_dat) : Node("waypoint_publisher"), waypoints_(path_dat), index_(0)
        {
            publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>("forward_position_controller/commands", 10);
            timer_ = this->create_wall_timer(std::chrono::milliseconds(500), std::bind(&ForwardPublisher::timer_callback, this));
        }

    private:
        void timer_callback()
        {
            if (index_ >= waypoints_.size()) {
                RCLCPP_INFO(this->get_logger(), "Finished publishing all waypoints.");
                timer_->cancel();
                return;
            }

            auto msg = std_msgs::msg::Float64MultiArray();
            msg.data = waypoints_[index_];
            
            std::stringstream ss;
            for (int i = 0; i < msg.data.size(); i++) {
                ss << msg.data[i] << " ";
            };
            RCLCPP_INFO(this->get_logger(), "%s", ss.str().c_str());

            publisher_->publish(msg);            
            index_++;
        }
        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr publisher_;
        size_t index_;
        std::vector<std::vector<double>> waypoints_;
};


int main(int argc, char * argv[])
{
    std::string path = "/home/aaron/ur_ws/src/moveit_control/ajam_waypoints.csv";
    auto waypoints = csv_to_waypoints(path);

    std::cout << "Loaded " << waypoints.size() << " waypoints from CSV." << std::endl;
    if (waypoints.empty()) {
        std::cerr << "Error loading waypoints." << std::endl;
    }

    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ForwardPublisher>(waypoints));
    rclcpp::shutdown();
    return 0;
};