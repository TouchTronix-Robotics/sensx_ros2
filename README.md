# SensX ROS 2 Driver

ROS 2 driver for TouchTronix SensX tactile sensors. Uses the
[sensx](https://github.com/TouchTronix-Robotics/sensx_python) Python API
for serial communication.

## Topics

| Topic | Type | Description |
|-------|------|-------------|
| `tactile/raw` | `std_msgs/UInt16MultiArray` | Raw 12-bit sensor values (rows x cols) |
| `tactile/image` | `sensor_msgs/Image` | Scaled mono8 grayscale image |

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `port` | `/dev/ttyUSB0` | Serial port |
| `baud` | `921600` | Baud rate |
| `rows` | `20` | Sensor grid rows |
| `cols` | `8` | Sensor grid columns |
| `max_value` | `4095` | Max sensor value for image scaling |

## Supported Sensors

| Model     | Grid  | Part Number        | Launch Command |
|-----------|-------|--------------------|----------------|
| SensX 25  | 5x5   | SNX0505-SNS-01     | `ros2 launch tactile_module sensor_launch.py port:=/dev/ttyUSB0 baud:=921600 rows:=5 cols:=5` |
| SensX 160 | 20x8  | SNX2006-SNS-01     | `ros2 launch tactile_module sensor_launch.py port:=/dev/ttyUSB0 baud:=921600 rows:=20 cols:=8` |
| SensX 192 | 16x12 | SNX1216-SNS-01     | `ros2 launch tactile_module sensor_launch.py port:=/dev/ttyUSB0 baud:=15000000 rows:=16 cols:=12` * |

\* SensX 192 baud rate is unverified — may be 921600 instead of 15000000.

## Serial Permissions (Linux)

```bash
sudo chmod a+rw /dev/ttyUSB0
```

## Native Build

```bash
# Install sensx
pip install --upgrade pip setuptools wheel
pip install git+https://github.com/TouchTronix-Robotics/sensx_python.git

# Build workspace
mkdir -p ~/sensor_ws/src
cd ~/sensor_ws/src
git clone https://github.com/TouchTronix-Robotics/sensx_ros2.git
cd ~/sensor_ws
colcon build --symlink-install
source install/setup.bash

# Run
ros2 launch tactile_module sensor_launch.py
```

## Visualize

```bash
# Echo raw data
ros2 topic echo /tactile/raw

# View as image (requires ros-${ROS_DISTRO}-rqt-image-view)
ros2 run rqt_image_view rqt_image_view /tactile/image
```

## Docker

### Build

```bash
# ROS 2 Humble (default)
docker build -t ros2-humble-tactile .

# ROS 2 Jazzy
docker build --build-arg ROS_DISTRO=jazzy -t ros2-jazzy-tactile .
```

### Run

```bash
# Without GUI
docker run -it --rm --privileged -v /dev:/dev ros2-humble-tactile

# With GUI (for rqt_image_view)
xhost +local:docker
docker run -it --rm --privileged -v /dev:/dev \
    -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
    ros2-humble-tactile
```

Inside the container:

```bash
# Default (20x8)
ros2 launch tactile_module sensor_launch.py

# 5x5 sensor
ros2 launch tactile_module sensor_launch.py rows:=5 cols:=5

# Custom port and max value
ros2 launch tactile_module sensor_launch.py port:=/dev/ttyUSB1 max_value:=2047
```
