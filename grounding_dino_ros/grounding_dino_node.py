#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray
from groundingdino.util.inference import load_model, predict
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

        self.get_logger().info('Loading model...')
        model_config_path = self.get_parameter('model_config_path').get_parameter_value().string_value
        model_checkpoint_path = self.get_parameter('model_checkpoint_path').get_parameter_value().string_value
        device = self.get_parameter('device').get_parameter_value().string_value

        self.model = load_model(model_config_path, model_checkpoint_path)
        self.model.to(device)
        self.device = device

        self.get_logger().info('Model loaded successfully.')

    def image_callback(self, msg: Image) -> None:
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        text_prompt = self.get_parameter('text_prompt').value

        rgb_image = cv_image[:, :, ::-1]

        box_threshold = self.get_parameter('box_threshold').value
        text_threshold = self.get_parameter('text_threshold').value

        boxes, logits, phrases = predict(
            model=self.model,
            image=rgb_image,
            caption=text_prompt,
            box_threshold=box_threshold,
            text_threshold=text_threshold,
            device=self.device,
        )

        self._last_boxes = boxes
        self._last_logits = logits
        self._last_phrases = phrases


def main(args=None):
    rclpy.init(args=args)
    node = GroundingDinoNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
