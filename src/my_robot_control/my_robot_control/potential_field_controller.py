import math
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from scipy.spatial.transform import Rotation as R


class Controller(Node):

    def __init__(self):
        super().__init__('potential_field_controller')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.declare_parameter("goal_x", 1.0)
        self.declare_parameter("goal_y", 3.0)
        self.goal_x = self.get_parameter("goal_x").value
        self.goal_y = self.get_parameter("goal_y").value
        self.kv = 0.4
        self.kw = 0.8
        self.tolerance = 0.05
        self.max_speed_linear = 2.0
        self.max_speed_angular = 2.0
        self.vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.on_timer)
        self.goal_reached = False

    def set_goal(self, x, y):
        self.goal_x = x
        self.goal_y = y
        self.goal_reached = False
        self.get_logger().info(f"New goal set to: x={x}, y={y}")

    def on_timer(self):
        from_frame_rel = 'odom'
        to_frame_rel = 'base_footprint'

        try:
            t = self.tf_buffer.lookup_transform(
                from_frame_rel,
                to_frame_rel,
                rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().info(
                f'Could not transform {from_frame_rel} to {to_frame_rel}: {ex}')
            return

        self.get_logger().info(f"Current position: x={t.transform.translation.x}, y={t.transform.translation.y}")
        
        quaternion = [t.transform.rotation.x, t.transform.rotation.y, t.transform.rotation.z, t.transform.rotation.w]
        r = R.from_quat(quaternion)
        euler = r.as_euler('xyz', degrees=False)

        vel_command = Twist()
        distance = math.sqrt((self.goal_x - t.transform.translation.x) ** 2 + (self.goal_y - t.transform.translation.y) ** 2)
        angle = math.atan2(self.goal_y - t.transform.translation.y, self.goal_x - t.transform.translation.x) - euler[2]
        if angle > math.pi:
            angle -= 2 * math.pi
        elif angle < -math.pi:
            angle += 2 * math.pi

        if distance > self.tolerance:
            if math.cos(angle) >= 0:
                vel_command.linear.x = min(distance * self.kv * math.cos(angle), self.max_speed_linear)
            else:
                vel_command.linear.x = max(distance * self.kv * math.cos(angle), -self.max_speed_linear)
            if angle >= 0:
                vel_command.angular.z = min(self.kw * angle, self.max_speed_angular)
            else:
                vel_command.angular.z = max(self.kw * angle, -self.max_speed_angular)
        else:
            vel_command.linear.x = 0.0
            vel_command.angular.z = 0.0
            if not self.goal_reached:
                self.get_logger().info("Goal reached!")
                self.goal_reached = True

        self.vel_publisher.publish(vel_command)


def main():
    rclpy.init()
    node = Controller()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()


if __name__ == '__main__':
    main()
