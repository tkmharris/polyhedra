import numpy as np
import trimesh

toX = np.array([
    [ 1.0 / np.sqrt(3.0), 1.0 / np.sqrt(3.0),  1.0 / np.sqrt(3.0)],
    [-1.0 / np.sqrt(6.0), 2.0 / np.sqrt(6.0), -1.0 / np.sqrt(6.0)],
    [-1.0 / np.sqrt(2.0),                0.0,  1.0 / np.sqrt(2.0)]
])
aroundX = np.array([
    [1.0,                0.0,                 0.0],
    [0.0,         -1.0 / 2.0, -np.sqrt(3.0) / 2.0],
    [0.0, np.sqrt(3.0) / 2.0,          -1.0 / 2.0]
])

I = np.identity(3)
R = np.linalg.inv(toX) @ aroundX @ toX
S = np.array([
    [-1.0,  0.0, 0.0],
    [ 0.0, -1.0, 0.0],
    [ 0.0,  0.0, 1.0]
])
T = np.array([
    [-1.0, 0.0,  0.0],
    [ 0.0, 1.0,  0.0],
    [ 0.0, 0.0, -1.0]
])

rotations = [
        I,         R,         R @ R,
        S,     R @ S,     R @ R @ S,
        T,     R @ T,     R @ R @ T,
    T @ S, R @ T @ S, R @ R @ T @ S,
]

φ = (1.0 + np.sqrt(5.0)) / 2.0
pentagon_vertices = np.array([
    [    1.0,      1.0, 1.0],
    [    1.0,     -1.0, 1.0],
    [      φ,  1.0 / φ, 0.0],
    [      φ, -1.0 / φ, 0.0],
    [1.0 / φ,      0.0,   φ]
]).T
pentagon_faces = [
    [0, 4, 1], [0, 1, 3], [0, 3, 2]
]

def test_stl():
    mesh = trimesh.util.concatenate([
        trimesh.Trimesh(
            vertices = (M @ pentagon_vertices).T, 
            faces = pentagon_faces
        )
        for M in rotations
    ])
    mesh.export("test.stl")

k = 1.0 / np.sqrt(20.0 * φ + 15.0)
toZ = np.array([
    [       k * (φ + 2.0), 0.0,  k * (3.0 * φ + 1.0)],
    [                 0.0, 1.0,                  0.0],
    [-k * (3.0 * φ + 1.0), 0.0,        k * (φ + 2.0)],
])

def toXY(vec):
    k = np.sqrt(20.0 * φ + 15.0)
    rotation = np.array([
        [      (1.0 / k) * (φ + 2.0), 0.0, -(1.0 / k) * (3.0 * φ + 1.0)],
        [                         0.0, 1.0,                         0.0],
        [(1.0 / k) * (3.0 * φ + 1.0), 0.0,        (1.0 / k) * (φ + 2.0)],
    ])
    translation = -np.array([
        0.0, 0.0, k / 5.0
    ])
    return (rotation @ vec + translation)[:2]


