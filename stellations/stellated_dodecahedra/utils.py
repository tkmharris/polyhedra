import numpy as np
import trimesh

# golden ratio
φ = (1.0 + np.sqrt(5.0)) / 2.0

# I think I could remove from_xy and to_xy using 
# https://trimsh.org/trimesh.geometry.html#trimesh.geometry.plane_transform
def to_xy(xyz_pt):
    """
    Mapping R^2 -> R^3 calibrated such that the midpoint
    of the pentagon defined by:
        (1.0 / np.sqrt(3.0)) * np.array([
            [    1.0,      1.0,  1.0]
            [    1.0,     -1.0,  1.0]
            [      φ,  1.0 / φ,  0.0]
            [      φ, -1.0 / φ,  0.0]
            [1.0 / φ,      0.0,    φ]
        ])
    goes to the origin and such that the map acts as an
    isometry on the plane containing this pentagon.
    """
    
    # rotation matrix
    k = np.sqrt(20.0 * φ + 15.0) # scale factor for nicer matrix
    R = np.array([
        [       (1.0 / k) * (φ + 2.0), 0.0,  (1.0 / k) * (3.0 * φ + 1.0)],
        [                         0.0, 1.0,                          0.0],
        [-(1.0 / k) * (3.0 * φ + 1.0), 0.0,        (1.0 / k) * (φ + 2.0)]
    ])

    # translation vector
    origin_preimage = (1.0 / (5.0 * np.sqrt(3.0))) * np.array(
        [3.0 * φ + 1.0, 0.0, φ + 2.0]
    ) # midpoint of the target face of the dodecahedron
    t = np.array([0.0, 0.0, np.linalg.norm(origin_preimage)])

    # translate and rotate point
    xy0_pt = np.linalg.inv(R) @ xyz_pt - t

    # drop final coordinate
    return xy0_pt[:2]

def from_xy(xy_pt):
    """
    Isometric embedding R^2 -> R^3 calibrated such that the
    image contains the pentagon defined by:
        (1.0 / np.sqrt(3.0)) * np.array([
            [    1.0,      1.0,  1.0]
            [    1.0,     -1.0,  1.0]
            [      φ,  1.0 / φ,  0.0]
            [      φ, -1.0 / φ,  0.0]
            [1.0 / φ,      0.0,    φ]
        ])
    and such that the origin is sent to the midpoint of this 
    pentagon.
    """
    
    # rotation matrix
    k = np.sqrt(20.0 * φ + 15.0) # scale factor for nicer matrix
    R = np.array([
        [      (1.0 / k) * (φ + 2.0), 0.0, -(1.0 / k) * (3.0 * φ + 1.0)],
        [                        0.0, 1.0,                          0.0],
        [(1.0 / k) * (3.0 * φ + 1.0), 0.0,        (1.0 / k) * (φ + 2.0)],
    ])

    # translation vector
    origin_image = (1.0 / (5.0 * np.sqrt(3.0))) * np.array(
        [3.0 * φ + 1.0, 0.0, φ + 2.0]
    ) # midpoint of the target face of the dodecahedron
    t = np.array([0.0, 0.0, np.linalg.norm(origin_image)])

    # map point into z=0 plane
    xy0_pt = np.pad(xy_pt, (0,1))

    # translate and rotate point
    return np.linalg.inv(R) @ (xy0_pt + t)

def build_polygon(vertices):
    """
    vertices: shape (n, 3).
    We want the normal to point away from the origin
    """
    # Build the polygons so that the normals are all facing outwards.
    # This is heavily contingent on the ordering of the vertices and should be
    # replaced with something more robust.
    if vertices.shape[0] == 5:
        mesh = trimesh.Trimesh(vertices = vertices, faces = [[0, 1, 2], [0, 2, 3], [0, 3, 4]])
    elif vertices.shape[0] == 3:
        mesh = trimesh.Trimesh(vertices = vertices, faces = [[0,2,1]])
    else: 
        raise ValueError("Faces in stellated dodecahedra must be triangular or pentagonal") 
    return mesh


