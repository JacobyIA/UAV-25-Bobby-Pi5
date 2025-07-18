from ament_index_python.resources import has_resource

from launch.actions import DeclareLaunchArgument
from launch.launch_description import LaunchDescription
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description() -> LaunchDescription:
    """
    Generate a launch description with for the camera node and a visualiser.

    Returns
    -------
        LaunchDescription: the launch description

    """
    # parameters
    cam_dn_param_name = "cam_dn"
    cam_dn_param_default = str(0)
    cam_dn_param = LaunchConfiguration(
        cam_dn_param_name,
        default=cam_dn_param_default,
    )
    cam_dn_launch_arg = DeclareLaunchArgument(
        cam_dn_param_name,
        default_value=cam_dn_param_default,
        description="down camera ID or name"
    )
    
    cam_fr_param_name = "cam_fr"
    cam_fr_param_default = str(0)
    cam_fr_param = LaunchConfiguration(
        cam_fr_param_name,
        default=cam_fr_param_default,
    )
    cam_fr_launch_arg = DeclareLaunchArgument(
        cam_fr_param_name,
        default_value=cam_fr_param_default,
        description="front camera ID or name"
    )


    format_param_name = "format"
    format_param_default = str()
    format_param = LaunchConfiguration(
        format_param_name,
        default=format_param_default,
    )
    format_launch_arg = DeclareLaunchArgument(
        format_param_name,
        default_value=format_param_default,
        description="pixel format"
    )

    # camera node
    composable_nodes = [
        ComposableNode(
            package='camera_ros',
            plugin='camera::CameraNode',
            parameters=[{
                "camera": 0,
                "width": 640,
                "height": 480,
                "format": format_param,
            }],
            remappings=[
                ("camera", "cam_dn")
            ],
            extra_arguments=[{'use_intra_process_comms': True}],
        ),
        
        ComposableNode(
            package='camera_ros',
            plugin='camera::CameraNode',
            parameters=[{
                "camera": 1,
                "width": 640,
                "height": 480,
                "format": format_param,
            }],
            remappings=[
                ("camera", "cam_fr")
            ],
            extra_arguments=[{'use_intra_process_comms': True}],
        ),

    ]

    # optionally add ImageViewNode to show camera image
    if has_resource("packages", "image_view"):
        composable_nodes += [
            ComposableNode(
                package='image_view',
                plugin='image_view::ImageViewNode',
                remappings=[('/image', '/camera/image_raw')],
                extra_arguments=[{'use_intra_process_comms': True}],
            ),
        ]

    # composable nodes in single container
    container = ComposableNodeContainer(
        name='camera_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=composable_nodes,
    )

    return LaunchDescription([
        container,
        cam_dn_launch_arg,
        cam_fr_launch_arg,
        format_launch_arg,
    ])