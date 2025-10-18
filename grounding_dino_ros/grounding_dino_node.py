#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class GroundingDinoNode(Node):
    def __init__(self):
        super().__init__('grounding_dino_node')
        # ここからAIに実装をお願いしていく

def main(args=None):
    rclpy.init(args=args)
    node = GroundingDinoNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()