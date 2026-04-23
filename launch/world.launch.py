from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose',
                 '/home/jyothi/mar_ws/src/line_follower/worlds/track.world',
                 '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        )
    ])
