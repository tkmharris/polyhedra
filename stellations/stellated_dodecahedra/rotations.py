import os.path
import numpy as np

PATH = 'data/rotations.npy'

def get_rotations():
    """
    Load the rotations from file if it exists; else generate them from scratch.
    Check shape is correct and error otherwise. Save rotations if generated.
    """
    loaded = False

    if os.path.exists(PATH):
        rotations = np.load(PATH)
        loaded = True
    else:
        rotations = generate_rotations()
    
    if rotations.shape != (12, 3, 3):
        raise ValueError("'rotations' is not the correct shape")
    
    if not loaded:
        np.save(PATH, rotations)
    
    return rotations

def generate_rotations():
    """
    A set of rotations R^3 -> R^3 that suffice to send
    the pentagon defined by:
        (1.0 / np.sqrt(3.0)) * np.array([
            [    1.0,      1.0,  1.0]
            [    1.0,     -1.0,  1.0]
            [      φ,  1.0 / φ,  0.0]
            [      φ, -1.0 / φ,  0.0]
            [1.0 / φ,      0.0,    φ]
        ])
    to 11 other pentagons such that the images
    form a dodecahedron inscribed in the unit sphere.
    """

    # We define rotation by 2π/3 about the unit dodecahedron vertex
    # [ 1.0, 1.0, 1.0 ] by rotating this vector to the x-axis,
    # performing a 2π/3 rotation in the yz-plane, and then reversing
    # the first rotation.
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
    R = np.linalg.inv(toX) @ aroundX @ toX

    # The identity and rotations by π in the xy- and xz-planes
    # suffice together with R to generate the rotations we need.
    I = np.identity(3)
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

    rotations = np.array([
            I,         R,         R @ R,
            S,     R @ S,     R @ R @ S,
            T,     R @ T,     R @ R @ T,
        T @ S, R @ T @ S, R @ R @ T @ S,
    ])

    return rotations

ROTATIONS = get_rotations()