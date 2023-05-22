import numpy as np
import numpy as np
import trimesh
import drawsvg as draw
import itertools
from rotations import rotations

class Dodecahedron:

    def __init__(self, radius=1):
        self.radius = radius

    def vertices(self):
        φ = (1.0 + np.sqrt(5.0)) / 2.0
        unscaled = np.array([
            [     1.0,      1.0,      1.0],
            [     1.0,      1.0,     -1.0],
            [     1.0,     -1.0,      1.0],
            [     1.0,     -1.0,     -1.0],
            [    -1.0,      1.0,      1.0],
            [    -1.0,      1.0,     -1.0],
            [    -1.0,     -1.0,      1.0],
            [    -1.0,     -1.0,     -1.0],
            [       φ,  1.0 / φ,      0.0],
            [       φ, -1.0 / φ,      0.0],
            [      -φ,  1.0 / φ,      0.0],
            [      -φ, -1.0 / φ,      0.0],
            [     0.0,        φ,  1.0 / φ],
            [     0.0,        φ, -1.0 / φ],
            [     0.0,       -φ,  1.0 / φ],
            [     0.0,       -φ, -1.0 / φ],
            [ 1.0 / φ,      0.0,        φ],
            [ 1.0 / φ,      0.0,       -φ],
            [-1.0 / φ,      0.0,        φ],
            [-1.0 / φ,      0.0,       -φ],
        ])
        return self.radius * (1.0 / np.sqrt(3.0)) * unscaled
    
    def face_midpoints(self):
        faces = [
        [0, 2, 8, 9, 16], 
        [2, 6, 14, 16, 18], 
        [2, 3, 9, 14, 15], 
        [1, 3, 8, 9, 17], 
        [0, 1, 8, 12, 13], 
        [0, 4, 12, 16, 18], 
        [4, 6, 10, 11, 18], 
        [6, 7, 11, 14, 15], 
        [3, 7, 15, 17, 19], 
        [1, 5, 13, 17, 19], 
        [4, 5, 10, 12, 13], 
        [5, 7, 10, 11, 19]
        ]
        midpoints = np.array([
            self.vertices()[face, :].mean(axis=0)
            for face in faces
        ])
        return midpoints

    def mesh(self):
        return trimesh.convex.convex_hull(self.vertices())

    def to_stl(self):
        self.mesh().export("../stl/dodecahedron.stl")

def to_xy_plane(pt):
    """
    Map from R^3 -> R^2 calibrated so that the
    midpoint of the face of the dodecahedron
    given by:
        [    1.0,      1.0,  1.0]
        [    1.0,     -1.0,  1.0]
        [      φ,  1.0 / φ,  0.0]
        [      φ, -1.0 / φ,  0.0]
        [1.0 / φ,      0.0,    φ]
    is sent to the origin and such that the map
    acts isometrically when restricted to the 
    plane containing this face.
    """
    φ = (1.0 + np.sqrt(5.0)) / 2.0
    
    midpoint = (1.0 / 5.0) * (1.0 / np.sqrt(3.0)) * np.array([3.0 * φ + 1.0, 0.0, φ + 2.0])
    k = np.sqrt(20.0 * φ + 15.0)

    # rotation matrix
    R = np.array([
        [      (1.0 / k) * (φ + 2.0), 0.0, -(1.0 / k) * (3.0 * φ + 1.0)],
        [                         0.0, 1.0,                         0.0],
        [(1.0 / k) * (3.0 * φ + 1.0), 0.0,        (1.0 / k) * (φ + 2.0)],
    ])

    # translation vector
    t = np.array([0.0, 0.0, -np.linalg.norm(midpoint)])

    # rotate, translate, and drop final coordinate  
    return (R @ pt + t)[:2]

def from_xy_plane(pt):
    """Inverse of the above"""
    pt = np.pad(pt, (0,1))

    φ = (1.0 + np.sqrt(5.0)) / 2.0
    
    midpoint = (1.0 / 5.0) * (1.0 / np.sqrt(3.0)) * np.array([3.0 * φ + 1.0, 0.0, φ + 2.0])
    k = np.sqrt(20.0 * φ + 15.0)

    # rotation matrix
    R = np.array([
        [      (1.0 / k) * (φ + 2.0), 0.0, -(1.0 / k) * (3.0 * φ + 1.0)],
        [                         0.0, 1.0,                         0.0],
        [(1.0 / k) * (3.0 * φ + 1.0), 0.0,        (1.0 / k) * (φ + 2.0)],
    ])

    # translation vector
    t = np.array([0.0, 0.0, -np.linalg.norm(midpoint)])

    return np.linalg.inv(R) @ (pt - t)
  

def intersection_point(m0, m1, m2):
    """
    Find the line of intersection of the triple of planes defined by:
    m0 . (x - m0) = 0
    m1 . (x - m1) = 0
    m2 . (x - m2) = 0
    (These are the face planes of the solid when mi is the 
    midpoint of each face.)

    (Requires m0, m1, m2 linearly independent)
    """
    M = np.array([m0, m1, m2])

    b = np.array([
        np.dot(m0, m0), np.dot(m1, m1), np.dot(m2, m2),
    ])

    return np.linalg.solve(M, b)

"""
d = draw.Drawing(2000, 2000, origin='center')

midpoints = Dodecahedron().face_midpoints()
m0 = midpoints[0]

for m1 in midpoints[1:]:
    for m2, m3 in itertools.combinations(midpoints[1:], 2):
        try:
            pt2 = 100*to_xy_plane(intersection_point(m0, m1, m2))
            pt3 = 100*to_xy_plane(intersection_point(m0, m1, m3))
            d.append(
                draw.Line(
                    pt2[0], pt2[1], pt3[0], pt3[1], stroke='black'
                )
            )
        except:
            pass
    
d.save_png('example.png')
"""

def stellation_diagram_point(m0, m1, m2):
    return to_xy_plane(intersection_point(m0, m1, m2))

midpoints = Dodecahedron().face_midpoints()
face_intersections = [
    midpoints[face_indices]
    for face_indices in [
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 4],
        [0, 4, 5],
        [0, 5, 1],
        [0, 1, 3],
        [0, 2, 4],
        [0, 3, 5],
        [0, 4, 1],
        [0, 5, 2],  
        [0, 6, 9],
        [0, 7, 10],
        [0, 8, 6],
        [0, 9, 7],
        [0, 10, 8]
    ]
]
stellation_diagram_points = np.array([
    stellation_diagram_point(*faces)
    for faces in face_intersections
])  

stellation_diagram_regions = [
    stellation_diagram_points[point_indices]
    for point_indices in [
        [0, 1, 2, 3, 4],
        [0, 1, 5],
        [1, 2, 6],
        [2, 3, 7],
        [3, 4, 8],
        [4, 0, 9],
        [0, 9, 5],
        [1, 5, 6],
        [2, 6, 7],
        [3, 7, 8],
        [4, 8, 9],
        [5, 6, 13],
        [6, 7, 14],
        [7, 8, 10],
        [8, 9, 11],
        [9, 5, 12]
    ]
]

stellation_shells = {
    'central': [0],
    'first': [1, 2, 3, 4, 5],
    'second': [6, 7, 8, 9, 10],
    'third': [11, 12, 13, 14, 15]
}

meshes = []
for face in stellation_shells['third']:
    region = stellation_diagram_regions[face]
    points = np.array([
        from_xy_plane(pt) for pt in region
    ]).T
    if points.shape[1] > 3:
        mesh = trimesh.util.concatenate([
            trimesh.convex.convex_hull((M @ points).T)
            for M in rotations
        ])
    elif points.shape[1] == 3:
        mesh = trimesh.util.concatenate([
            trimesh.Trimesh(vertices = (M @ points).T, faces = [[0,1,2], [0,2,1]])
            for M in rotations
        ])
    meshes.append(mesh)

mesh = trimesh.util.concatenate(meshes)
mesh.export("test.stl")