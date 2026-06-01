#!/usr/bin/env /media/gugu/DATA/diff_car/venv/bin/python3
import rclpy
from rclpy.node import Node
from interface.srv import Speech
import espeakng

class SpeakerNode(Node):
    def __init__(self):
        super().__init__('speaker_node')
        self.srv = self.create_service(Speech, 'speak', self.speak_callback)
        self.esng = espeakng.Speaker()
        self.esng.voice = 'zh'

    def speak_callback(self, request, response):
        text = request.text
        self.get_logger().info(f'Received text to speak: "{text}"')
        self.esng.say(text)
        self.esng.wait()  # 等待语音播放完成
        response.success = True
        return response
    
def main(args=None):
    rclpy.init(args=args)
    speaker_node = SpeakerNode()
    rclpy.spin(speaker_node)
    speaker_node.destroy_node()
    rclpy.shutdown()