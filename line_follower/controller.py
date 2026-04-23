import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math

class Controller(Node):

    def __init__(self):
        super().__init__('controller')

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.create_subscription(LaserScan, '/gazebo_ros_ray_sensor/out', self.scan_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.front_dist = 5.0

        # STATES
        self.state = "FOLLOW"
        self.avoid_step = 0
        self.avoid_counter = 0

        # WAYPOINTS (square track)
        self.waypoints = [
	    (0, 6),     # start point
	    (6, 6),     # top-right
	    (6, -6),    # bottom-right
	    (-6, -6),   # bottom-left
	    (-6, 6),    # top-left
	    (0, 6),     # back to start
	]
        self.current_wp = 0

    # ---------------- LIDAR ----------------
    def scan_cb(self, msg):
        mid = len(msg.ranges)//2
        front = msg.ranges[mid-6:mid+6]
        valid = [r for r in front if r > 0.0 and not math.isinf(r)]
        self.front_dist = min(valid) if valid else 5.0

    # ---------------- YAW ----------------
    def get_yaw(self, msg):
        q = msg.pose.pose.orientation
        siny = 2 * (q.w*q.z + q.x*q.y)
        cosy = 1 - 2 * (q.y*q.y + q.z*q.z)
        return math.atan2(siny, cosy)

    def angle_diff(self, target, current):
        diff = target - current
        return math.atan2(math.sin(diff), math.cos(diff))

    # ---------------- CONTROL ----------------
    def odom_cb(self, msg):

        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.yaw = self.get_yaw(msg)

        cmd = Twist()

        # ================= OBSTACLE TRIGGER =================
        if self.state == "FOLLOW" and self.front_dist < 1.0:
            self.state = "AVOID"
            self.avoid_step = 0
            self.avoid_counter = 0

        # ================= AVOID MODE =================
        if self.state == "AVOID":

            # STEP 1: TURN LEFT
            if self.avoid_step == 0:
                cmd.angular.z = 0.8
                self.avoid_counter += 1

                if self.avoid_counter > 25:
                    self.avoid_step = 1
                    self.avoid_counter = 0

            # STEP 2: MOVE FORWARD (SIDE)
            elif self.avoid_step == 1:
                cmd.linear.x = 0.3
                self.avoid_counter += 1

                if self.avoid_counter > 35:
                    self.avoid_step = 2
                    self.avoid_counter = 0

            # STEP 3: TURN RIGHT (come parallel)
            elif self.avoid_step == 2:
                cmd.angular.z = -0.8
                self.avoid_counter += 1

                if self.avoid_counter > 25:
                    self.avoid_step = 3
                    self.avoid_counter = 0

            # STEP 4: MOVE FORWARD (PASS OBSTACLE)
            elif self.avoid_step == 3:
                cmd.linear.x = 0.3
                self.avoid_counter += 1

                if self.avoid_counter > 40:
                    self.state = "FOLLOW"   # return to path

            self.pub.publish(cmd)
            return

        # ================= FOLLOW PATH =================
        target = self.waypoints[self.current_wp]

        dx = target[0] - self.x
        dy = target[1] - self.y

        dist = math.hypot(dx, dy)

        target_angle = math.atan2(dy, dx)
        error = self.angle_diff(target_angle, self.yaw)

        # CONTROL (NO SPIN)
        if abs(error) > 0.5:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.7 * error
        else:
            cmd.linear.x = 0.3
            cmd.angular.z = 0.4 * error

        # ONLY TURN AT CORNER
        if dist < 0.3 and abs(error) < 0.2:
            self.current_wp = (self.current_wp + 1) % len(self.waypoints)

        self.pub.publish(cmd)


def main():
    rclpy.init()
    node = Controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
