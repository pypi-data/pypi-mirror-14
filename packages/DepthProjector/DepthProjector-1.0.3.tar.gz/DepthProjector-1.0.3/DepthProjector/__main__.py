#!/usr/bin/env python

# coding=utf-8

import click
from DepthProjector._pp import PerspectiveProjection

__author__ = 'kanairen'

HELP_THETA = 'Range of theta angle([FROM] [TO] [STEP]). Default is (0 360 30).'
HELP_PHI = 'Range of phi angle([FROM] [TO] [STEP]). Default is (-60 61 30).'
HELP_INIT_ROTATION = 'Initial rotation of 3d shape([X] [Y] [Z]). Default is (0 0 0).'
HELP_RADIUS = "Radius of camera coordinate."
HELP_IS_VIEW_ONLY = 'option whether is DepthProjector executed as 3D Viewer(procjection is not executed) or not.'


@click.command()
@click.argument('file_path')
@click.option('--theta_angle_range', '-t', nargs=3, type=(int, int, int),
              default=(0, 360, 30), help=HELP_THETA)
@click.option('--phi_angle_range', '-p', nargs=3, type=(int, int, int),
              default=(-60, 61, 30), help=HELP_PHI)
@click.option('--init_rotation', '-i', nargs=3, type=(int, int, int),
              default=(0, 0, 0), help=HELP_INIT_ROTATION)
@click.option('--radius', '-r', type=float, default=1., help=HELP_RADIUS)
@click.option('--is_view_only', '-v', type=bool, default=False,
              help=HELP_IS_VIEW_ONLY)
def depth_image(file_path, theta_angle_range, phi_angle_range, init_rotation,
                radius, is_view_only):
    pp = PerspectiveProjection(theta_angle_range, phi_angle_range, radius)
    pp.depth_image(file_path, init_rotation, is_view_only=is_view_only)


if __name__ == '__main__':
    depth_image()
