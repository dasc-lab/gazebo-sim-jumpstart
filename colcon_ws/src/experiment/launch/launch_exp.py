#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    print("hi")

    """Launch Gazebo with a drone running PX4 communicating over ROS 2."""
    HOME = os.environ.get('HOME')
    PX4_RUN_DIR = HOME + '/tmp/px4_run_dir'
    
    gazebo_launch_dir = os.path.join(get_package_share_directory('gazebo_ros'), 'launch')

    # the world and models are copied directly from the PX4-Autopilot directory
    experiment_gazebo_dir = get_package_share_directory('experiment')
    world = os.path.join(experiment_gazebo_dir, 'worlds', 'empty.world') # 'warehouse.world')
    model = os.path.join(experiment_gazebo_dir, 'models', 'iris_depth_camera', 'iris_depth_camera.sdf')

    os.makedirs(PX4_RUN_DIR, exist_ok=True)

    return LaunchDescription([
        SetEnvironmentVariable('GAZEBO_PLUGIN_PATH',
                               '/root/PX4-Autopilot/build/px4_sitl_rtps/build_gazebo'),
        
        SetEnvironmentVariable('GAZEBO_MODEL_PATH', '/root/PX4-Autopilot/Tools/sitl_gazebo/models'),

        SetEnvironmentVariable('PX4_SIM_MODEL', 'iris'),

        DeclareLaunchArgument('world', default_value=world),
        DeclareLaunchArgument('model', default_value=model),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='0.0'),
        DeclareLaunchArgument('R', default_value='0.0'),
        DeclareLaunchArgument('P', default_value='0.0'),
        DeclareLaunchArgument('Y', default_value='0.0'),

        # launch the gzserver
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([gazebo_launch_dir, '/gzserver.launch.py']),
            launch_arguments={'world': LaunchConfiguration('world'),
                              'verbose': 'true',
                              'lockstep': 'true'}.items(),
        ),

        # launch the gzclient
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([gazebo_launch_dir, '/gzclient.launch.py'])
        ),
        
        # define a static transform for the camera
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            arguments=['0','0','0','-1.57','0','-1.57', 'drone1', 'camera_link'],
            parameters = [
                {'use_sim_time': True}
                ],
            ),

        # launch gazebo
        ExecuteProcess(
            cmd=[
                'gz', 'model',
                '--spawn-file', LaunchConfiguration('model'),
                '--model-name', 'drone',
                '-x', LaunchConfiguration('x'),
                '-y', LaunchConfiguration('y'),
                '-z', LaunchConfiguration('z'),
                '-R', LaunchConfiguration('R'),
                '-P', LaunchConfiguration('P'),
                '-Y', LaunchConfiguration('Y')
            ],
            prefix="bash -c 'sleep 5s; $0 $@'",
            output='screen'),
            
        # launch px4's autopilot
        ExecuteProcess(
            cmd=[
                '/root/PX4-Autopilot/build/px4_sitl_rtps/bin/px4',
                '/root/PX4-Autopilot/ROMFS/px4fmu_common/',
                '-s',
                '/root/PX4-Autopilot/ROMFS/px4fmu_common/init.d-posix/rcS'
            ],
            cwd=PX4_RUN_DIR,
            output='screen'),
  
        # launch micrortps_agent
        ExecuteProcess(
            cmd=['micrortps_agent', '-t', 'UDP', '-n', 'drone1'],
            output='screen'),

])
