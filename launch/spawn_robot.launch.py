from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([

        ExecuteProcess(
            cmd=[
                'ros2', 'run', 'gazebo_ros', 'spawn_entity.py',
                '-entity', 'tb3',
                '-file',
                '/opt/ros/humble/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf',
                '-x', '0',
                '-y', '6',
                '-z', '0.1'
            ],
            output='screen'
        )

    ])
