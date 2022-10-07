# gazebo-sim-jumpstart
Jumping point for sims in gazebo using ros2 and px4

## Forking/Cloning

Fork this repo, clone it. `cd` into the repo.

Initialize submodules:
```
git submodule init
git submodule update --recursive
```
Note: `--recursive` is important!

Clone PX4-Autopilot:
```
git clone git@github.com:dasc-lab/PX4-Autopilot.git
```
Note: this isnt installed as a git submodule due to some issues with how submodules are treated during PX4-Autopilot's build. 

The folder should now have a structure similar to:
```
.
├── colcon_ws
│   └── src
│       ├── experiment
│       ├── px4_msgs
│       ├── px4_ros_com
│       └── robot-framework
├── docker-compose.yaml
├── Dockerfile
├── LICENSE
├── PX4-Autopilot
└── README.md
```


## Building

Build docker:
```
docker compose build
```

Launch container:
```
docker compose up
```

Enter the docker container. 

Build `PX4-Autopilot` library:
```
cd /root/PX4-Autopilot
DONT_RUN=1 make px4_sitl_rtps gazebo
```
Note, since this builds PX4, and the build is also mounted into the docker, rebooting the docker container does not require rebuilding the PX4-Autopilot. However, if you make changes in PX4-Autopilot, please rebuild `PX4-Autopilot`.

Build `colcon_ws`:
```
cd /root/colcon_ws
colcon build --symlink-install
```

Source the environment: 
```
source /opt/ros/galactic/setup.bash
source /root/colcon_ws/install/setup.bash
```
These lines have been added to the `~/.bashrc`, so they may not be needed in every new terminal. 

Since the `colcon_ws` is mounted using the `docker_compose.yaml` any code changes made in or outside the docker container will remain saved (and therefore git commitable). If you have made changes to the base setup that you think other users will benefit from, please raise a pull request. 


## Running Experiments

Open GGC (outside the docker environment)

Run the launch file:
```
ros2 run experiment launch_exp.py
```

For some nodes, you might want/need to specify that they should be using sim time. Launch the node using a ros param:
```
ros2 run <pkg> <node_name> --ros-args -p use_sim_time:=True
``` 

To test functionality, you can make the drone takeoff using the buttons in QGC.


