from pythreejs import *
import pythreejs as pjs
import numpy as np


def create_threejs_scene(view_width=400, view_height=1200, add_lights=True):
    camera = pjs.CombinedCamera(
        position=[0, 0, 1], width=view_width, height=view_height)
    camera.up = (0, 0, 1)
    grid_helper = pjs.GridHelper(
        1, 10, colorCenterLine="#000000", colorGrid="#000000")
    grid_helper.rotateX(90 * 3.14159 / 180)
    scene = pjs.Scene(children=[camera, grid_helper])
    renderer = pjs.Renderer(
        scene=scene,
        camera=camera,
        controls=[pjs.OrbitControls(controlling=camera)],
        width=view_width,
        height=view_height,
        antialias=True)
    if add_lights:
        key_light = pjs.PointLight(position=[-100, -100, 100])
        ambient_light = pjs.AmbientLight(intensity=0.4)
        scene.add([key_light, ambient_light])

    return camera, scene, renderer


def create_axis_with_center_sphere(pos,
                                   quat,
                                   text='',
                                   axes_size=0.1,
                                   sphere_size=0.01,
                                   sphere_color='red'):
    helper = pjs.AxesHelper(axes_size, position=tuple(pos))
    helper.quaternion = tuple(quat)
    sm = pjs.SpriteMaterial(
        map=pjs.TextTexture(
            string=text, color='black', size=100, squareTexture=False))
    sc = 0.025
    label = pjs.Sprite(
        material=sm,
        position=list(pos),
        scaleToTexture=True,
        scale=[sc, sc, sc])
    label.position = (label.position[0] - sc, label.position[1],
                      label.position[2])

    return [helper, label]


def create_point_cloud_with_per_point_color(x, y, z, r, g, b, point_size=0.01):
    ptsCoord = np.vstack((x, y, z)).astype(np.float32).T
    colorsRaw = np.vstack((r, g, b)).astype(np.float32).T
    pts = pjs.BufferAttribute(array=ptsCoord, )

    colors = pjs.BufferAttribute(array=colorsRaw)
    geometry = pjs.BufferGeometry(attributes={
        'position': pts,
        'color': colors
    })
    geometry.attributes['color'] = pjs.BufferAttribute(colorsRaw)

    material = pjs.PointsMaterial(size=point_size)

    material.vertexColors = 'VertexColors'

    pointCloud = pjs.Points(geometry=geometry, material=material)
    return pointCloud


def create_point_cloud_with_single_color(x, y, z, point_size=0.1, color="#FFFFFF"):
    if isinstance(z, type(None)):
        z = y.copy()
        z[:] = 0
    ptsCoord = np.vstack((x, y, z)).astype(np.float32).T
    pts = pjs.BufferAttribute(array=ptsCoord)
    geometry = pjs.BufferGeometry(attributes={'position': pts})
    material = pjs.PointsMaterial(point_size=point_size, color=color)
    pointCloud = pjs.Points(geometry=geometry, material=material)
    return pointCloud
