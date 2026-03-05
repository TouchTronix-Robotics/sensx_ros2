import os
from setuptools import find_packages, setup

package_name = "tactile_module"

setup(
    name=package_name,
    version="1.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), ["launch/sensor_launch.py"]),
    ],
    install_requires=["setuptools", "sensx", "numpy"],
    entry_points={
        "console_scripts": [
            "tactile_pub = tactile_module.sensor_publisher:main",
        ],
    },
)
