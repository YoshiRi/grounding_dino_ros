#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
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

        text_prompt_descriptor = ParameterDescriptor(
            description='Text prompt describing objects to detect.',
            read_only=False,
        )
        self.declare_parameter(
            'text_prompt',
            'a person . a chair',
            text_prompt_descriptor,
        )
        self.declare_parameter('model_config_path', '')
        self.declare_parameter('model_checkpoint_path', '')
        self.declare_parameter('box_threshold', 0.35)
        self.declare_parameter('text_threshold', 0.25)
        self.declare_parameter('device', 'cuda')

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
