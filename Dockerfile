FROM px4io/px4-dev-ros2-foxy:2021-12-11

RUN apt-get update && \
 apt-get install -y --no-install-recommends vim tmux && \
 rm -fr /var/lib/apt/lists/{apt,dpkg,cache,log}

# install gazebo and any other packages necessary
RUN apt-get update && apt-get install -y \
  ros-foxy-gazebo-ros-pkgs \
  && rm -fr /var/lib/apt/lists/{apt,dpkg,cache,log}

# source folders
WORKDIR /root/colcon_ws
RUN echo 'source /opt/ros/foxy/setup.bash' >> ~/.bashrc
RUN echo 'source /root/colcon_ws/install/setup.bash' >> ~/.bashrc

WORKDIR /root/colcon_ws
