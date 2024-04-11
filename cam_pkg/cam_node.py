import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('cam_node')
        self.publisher_ = self.create_publisher(Image, 'camera_image', 10)
        timer_period = 0.1  # seconds (publish images at 1Hz)
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.br = CvBridge()
        self.cap = cv2.VideoCapture(0)  # Change '0' if you have multiple cameras

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the image from OpenCV format to ROS2 format and publish
            ros_image = self.br.cv2_to_imgmsg(frame, 'bgr8')
            self.publisher_.publish(ros_image)
        else:
            self.get_logger().warn('Camera frame capture failed.')

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher()
    rclpy.spin(camera_publisher)

    # Clean up
    camera_publisher.cap.release()
    camera_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
