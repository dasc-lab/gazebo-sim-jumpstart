# gazebo-sim-jumpstart
Jumping point for sims in gazebo using ros2 and px4

## Usage

Fork this repo, clone it, and initialize the submodules
```
git submodule init
git submodule update --recursive
```

This repo is very much designed to be used in a docker environment. To build it, run
```
docker compose build
```

and then the docker container can be created using
```
docker compose up
```

Enter the docker container. 

First we need to build the `PX4_Autopilot` library:
```
cd /root/PX4_Autopilot
DONT_RUN=1 make px4_sitl_rtps gazebo
```

Next, we need to build the colcon workspace. 
```
cd /root/colcon_ws
colcon build --symlink-install
```
to build all the packages. After the first build you will need to source the environment: 
```
source /opt/ros/galactic/setup.bash
source /root/colcon_ws/install/setup.bash
```
although these lines have been added to the `~/.bashrc`, so they may not be needed in every new terminal. 

Since the `colcon_ws` is mounted using the `docker_compose.yaml` any code changes made in or outside the docker container will remain saved (and therefore git commitable). If you have made changes to the base setup that you think other users will benefit from, please raise a pull request. 


To run experiments, we use a launch file:
```
ros2 run experiment launch_exp.py
```

For some nodes, you might want/need to specify that they should be using sim time. Launch the node using a ros param:
```
ros2 run <pkg> <node_name> --ros-args -p use_sim_time:=True
``` 
