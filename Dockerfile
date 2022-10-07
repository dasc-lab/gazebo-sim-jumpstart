FROM px4io/px4-dev-ros2-galactic

RUN apt-get update && \
 apt-get install -y --no-install-recommends vim tmux

# install gazebo and any other packages necessary
RUN apt-get update && apt-get install -y \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev  \ 
    ros-galactic-gazebo-ros-pkgs

# source folders
WORKDIR /root/colcon_ws
RUN echo 'source /opt/ros/galactic/setup.bash' >> ~/.bashrc
RUN echo 'source /root/colcon_ws/install/setup.bash' >> ~/.bashrc

WORKDIR /root/colcon_ws
