from setuptools import setup

package_name = 'line_follower'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', [
            'launch/world.launch.py',
            'launch/spawn_robot.launch.py'
        ]),
        ('share/' + package_name + '/worlds', [
            'worlds/track.world'
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jyothi',
    maintainer_email='jyothi@todo.todo',
    description='Line follower with obstacle avoidance',
    license='TODO',
    entry_points={
        'console_scripts': [
            'controller = line_follower.controller:main',
        ],
    },
)
