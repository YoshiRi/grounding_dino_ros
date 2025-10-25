#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray
from cv_bridge import CvBridge


class GroundingDinoNode(Node):
    def __init__(self):
        super().__init__('grounding_dino_node')
        self.bridge = CvBridge()
        self.image_subscription = self.create_subscription(
            Image,
            '~/input/image_raw',
            self.image_callback,
            10,
        )
        self.detections_publisher = self.create_publisher(
            Detection2DArray,
            '~/output/detections',
            10,
        )
        self.image_publisher = self.create_publisher(
            Image,
            '~/output/image_processed',
            10,
        )

    def image_callback(self, msg: Image) -> None:
        pass


def main(args=None):
    rclpy.init(args=args)
    node = GroundingDinoNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
