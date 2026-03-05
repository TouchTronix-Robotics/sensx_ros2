"""ROS 2 publisher node for TouchTronix SensX tactile sensors."""

import sys

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import MultiArrayDimension, MultiArrayLayout, UInt16MultiArray

from sensx import SensX


class SensorNode(Node):
    def __init__(self):
        super().__init__("sensor_publisher")

        # Declare parameters
        self.declare_parameter("port", "/dev/ttyUSB0")
        self.declare_parameter("baud", 921600)
        self.declare_parameter("rows", 20)
        self.declare_parameter("cols", 8)
        self.declare_parameter("max_value", 4095)

        port = self.get_parameter("port").get_parameter_value().string_value
        baud = self.get_parameter("baud").get_parameter_value().integer_value
        rows = self.get_parameter("rows").get_parameter_value().integer_value
        cols = self.get_parameter("cols").get_parameter_value().integer_value
        self._max_value = (
            self.get_parameter("max_value").get_parameter_value().integer_value
        )

        self._rows = rows
        self._cols = cols

        # Publishers
        self._pub_raw = self.create_publisher(UInt16MultiArray, "tactile/raw", 10)
        self._pub_img = self.create_publisher(Image, "tactile/image", 10)

        # Pre-build the MultiArray layout
        self._layout = MultiArrayLayout(
            dim=[
                MultiArrayDimension(label="rows", size=rows, stride=rows * cols),
                MultiArrayDimension(label="cols", size=cols, stride=cols),
            ],
            data_offset=0,
        )

        # Open sensor
        try:
            self._sensor = SensX(port=port, baud_rate=baud, rows=rows, cols=cols)
        except Exception as e:
            self.get_logger().fatal(f"Failed to open sensor: {e}")
            sys.exit(1)

        self._sensor.start()
        self._last_ts = 0.0

        # 100 Hz timer
        self._timer = self.create_timer(1.0 / 100.0, self._timer_cb)

        self.get_logger().info(f"SensX {rows}x{cols} on {port} @ {baud} baud")

    def _timer_cb(self):
        ts = self._sensor.latest_timestamp
        if ts == 0.0 or ts == self._last_ts:
            return  # no new frame
        self._last_ts = ts

        frame = self._sensor.latest_frame  # np.uint16, shape (rows, cols)

        # Publish raw
        msg_raw = UInt16MultiArray(layout=self._layout)
        msg_raw.data = frame.flatten().tolist()
        self._pub_raw.publish(msg_raw)

        # Publish mono8 image
        scale = 255.0 / max(self._max_value, 1)
        img_data = np.clip(frame.astype(np.float32) * scale, 0, 255).astype(np.uint8)

        msg_img = Image()
        msg_img.header.stamp = self.get_clock().now().to_msg()
        msg_img.header.frame_id = "tactile"
        msg_img.height = self._rows
        msg_img.width = self._cols
        msg_img.encoding = "mono8"
        msg_img.is_bigendian = False
        msg_img.step = self._cols
        msg_img.data = img_data.tobytes()
        self._pub_img.publish(msg_img)

    def destroy_node(self):
        self.get_logger().info("Shutting down sensor")
        self._sensor.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == "__main__":
    main()
