ARG ROS_DISTRO=humble
FROM ros:${ROS_DISTRO}

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip python3-colcon-common-extensions python3-serial \
    tmux ros-${ROS_DISTRO}-rqt-image-view \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir "setuptools>=64.0,<71" && \
    pip3 install --no-cache-dir \
    git+https://github.com/TouchTronix-Robotics/sensx_python.git \
    numpy

WORKDIR /ros2_ws/src
COPY . tactile_module/

WORKDIR /ros2_ws
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    rosdep update && \
    rosdep install -i --from-path src --rosdistro ${ROS_DISTRO} -y || true

RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    colcon build --symlink-install

RUN echo ". /opt/ros/${ROS_DISTRO}/setup.sh" >> /root/.bashrc && \
    echo ". /ros2_ws/install/setup.bash" >> /root/.bashrc

CMD ["bash"]
