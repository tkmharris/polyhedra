import numpy as np

φ = (1.0 + np.sqrt(5.0)) / 2.0

toX = np.array([
    [1.0 / np.sqrt(φ ** 2 + 1.0),   φ / np.sqrt(φ ** 2 + 1.0),  0.0],
    [ -φ / np.sqrt(φ ** 2 + 1.0), 1.0 / np.sqrt(φ ** 2 + 1.0),  0.0],
    [                        0.0,                         0.0,  1.0]
])
aroundX = np.array([
    [1.0,                       0.0,                        0.0],
    [0.0, np.cos(2.0 * np.pi / 5.0), -np.sin(2.0 * np.pi / 5.0)],
    [0.0, np.sin(2.0 * np.pi / 5.0),  np.cos(2.0 * np.pi / 5.0)]
])

toZ = np.array([
    [1.0 / np.sqrt(φ ** 2 + 1.0), 0.0,  -φ / np.sqrt(φ ** 2 + 1.0)],
    [                        0.0, 1.0,                          0.0],
    [  φ / np.sqrt(φ ** 2 + 1.0),  0.0, 1.0 / np.sqrt(φ ** 2 + 1.0)],
])
aroundZ = np.array([
    [ np.cos(2.0 * np.pi / 5.0), np.sin(2.0 * np.pi / 5.0), 0.0],
    [-np.sin(2.0 * np.pi / 5.0), np.cos(2.0 * np.pi / 5.0), 0.0],
    [                       0.0,                       0.0, 1.0]
])

I = np.identity(3)
R = np.linalg.inv(toX) @ aroundX @ toX
S = np.linalg.inv(toZ) @ aroundZ @ toZ
T = np.array([
    [-1.0,  0.0, 0.0],
    [ 0.0, -1.0, 0.0],
    [ 0.0,  0.0, 1.0]
])

rotations = [
        I,         R,         R @ R,         R @ R @ R,         R @ R @ R @ R,
        S,     R @ S,     R @ R @ S,     R @ R @ R @ S,     R @ R @ R @ R @ S,
        T,     T @ R,     T @ R @ R,     T @ R @ R @ R,     T @ R @ R @ R @ R,
    T @ S, T @ R @ S, T @ R @ R @ S, T @ R @ R @ R @ S, T @ R @ R @ R @ R @ S
]

triangle = np.array([
    [1.0,   φ,  0.0],
    [  φ, 0.0,  1.0],
    [  φ, 0.0, -1.0]
]).T


import trimesh


mesh = trimesh.util.concatenate([
    trimesh.Trimesh(vertices = (M @ triangle).T, faces = [0, 1, 2])
    for M in rotations
])
mesh.export("test.stl")

# hell yess!!!!
