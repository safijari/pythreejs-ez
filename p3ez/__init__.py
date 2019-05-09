import pythreejs as THREE
import pythreejs as pjs
from pythreejs import *
import numpy as np


def create_threejs_scene(view_width=400,
                         view_height=400,
                         add_lights=True,
                         cam_position=(0, 1, 1)):
    camera = pjs.CombinedCamera(
        position=cam_position, width=view_width, height=view_height)
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


def create_point_cloud_with_single_color(x,
                                         y,
                                         z,
                                         point_size=0.1,
                                         color="#FFFFFF"):
    if isinstance(z, type(None)):
        z = y.copy()
        z[:] = 0
    ptsCoord = np.vstack((x, y, z)).astype(np.float32).T
    pts = pjs.BufferAttribute(array=ptsCoord)
    geometry = pjs.BufferGeometry(attributes={'position': pts})
    material = pjs.PointsMaterial(size=point_size, color=color)
    pointCloud = pjs.Points(geometry=geometry, material=material)
    return pointCloud


morph = BufferGeometry.from_geometry(PlaneGeometry(1, 1))


def create_textured_plane(corners, image, morph):
    # corners is [(x, y, z), ...]
    # which is upper left, upper right, lower left, lower right
    top_left, top_right, bot_left, bot_right = corners

    rgb_image = image[:, :, ::-1]

    data_tex = DataTexture(data=rgb_image, format="RGBFormat")
    material = THREE.MeshBasicMaterial(map=data_tex)

    vertices_arr = morph.attributes['position'].array.copy()

    vertices_arr[0] = top_left
    vertices_arr[1] = bot_left
    vertices_arr[2] = top_right
    vertices_arr[3] = bot_left
    vertices_arr[4] = bot_right
    vertices_arr[5] = top_right

    vertices = BufferAttribute(vertices_arr)
    morph.attributes.update({'position': vertices})
    geometry = BufferGeometry(attributes=morph.attributes, )

    plane = Mesh(geometry, material)
    plane.material.side = 'DoubleSide'
    plane.material.transparent = True
    plane.material.opacity = 0.5

    return plane


def create_line_between_two_points(p1, p2, color='red', width=5):
    linesgeom = Geometry(
        vertices=[[p1[0], p1[1], p1[2]], [p2[0], p2[1], p2[2]]],
        colors=[color, color])

    lines = Line(
        geometry=linesgeom,
        material=LineBasicMaterial(
            linewidth=width, vertexColors='VertexColors'),
        type='LinePieces')

    return lines


def create_tf_tree_viz(tree, parent_name_, skip_substrs=['optical', 'target'], text=''):
    parent_name = tree.get_parent().name if not parent_name_ else parent_name_
    out = []
    for node in tree.nodes.values():
        skip = False
        for ss in skip_substrs:
            if ss in node.name:
                skip = True
        if skip:
            continue
        x = tree.lookup_transform(node.name, parent_name)
        out.extend(create_axis_with_center_sphere(x.position, x.quaternion, text=text))
    return out
