import os.path
import numpy as np
from utils import to_xy
from dodecahedron import Dodecahedron

PATH = 'data/stellation_diagram_points.npy'

def get_stellation_diagram_points():
    """
    Load the points from file if it exists; else generate them from scratch.
    Check shape is correct and error otherwise. Save points if generated.
    """
    loaded = False

    if os.path.exists(PATH):
        stellation_diagram_points = np.load(PATH)
        loaded = True
    else:
        stellation_diagram_points = generate_stellation_diagram_points()
    
    if stellation_diagram_points.shape != (15, 2):
        raise ValueError("'stellation_diagram_points' is not the correct shape")
    
    if not loaded:
        np.save(PATH, stellation_diagram_points)
    
    return stellation_diagram_points

def generate_stellation_diagram_points():
    """
    Generate the stellation diagram points from scratch. 
    Done by intersecting the plane containing the privileged face (index 0 in
    the dodecahedron's face array) with a specially-chosen pairs of other face
    planes sufficient to represent all points of intersection in the diagram. 
    This requires foreknowledge of the shape of the diagram but is simpler 
    than calculating all (11 C 2) = 55 intersections of the privileged plane 
    with two other planes and removing redundancies.
    """

    # Helper for getting the points.
    def intersect(three_faces):
        """
        Find the point of intersection of the triple of planes defined by:
        m0 . (x - m0) = 0
        m1 . (x - m1) = 0
        m2 . (x - m2) = 0,
        where three_faces = np.array([m0, m1, m2]), mi.shape = (3,).
        These are the planes through mi and orthogonal to mi;
        for us the mi are the midpoints of the faces of a dodecahedron
        centered on the origin.

        (Requires m0, m1, m2 linearly independent, else raises 
        numpy.linalg.LinAlgError)
        """
        M = three_faces
        b = np.array([
            np.dot(M[0], M[0]), np.dot(M[1], M[1]), np.dot(M[2], M[2]),
        ])

        return np.linalg.solve(M, b)

    # Use the unit dodecahedron
    face_midpoints = Dodecahedron().faces.mean(axis=1)

    # Defining the intersection sets below is contingent on the order of faces
    # in dodecahedron.py (bad!)
    face_sets_to_intersect = np.array([
        face_midpoints[face_indices]
        for face_indices in [
            [0, 1, 2],  [0, 2, 3], [0, 3, 4], [0, 4, 5], [0, 5, 1],
            [0, 1, 3],  [0, 2, 4], [0, 3, 5], [0, 4, 1], [0, 5, 2],  
            [0, 6, 9], [0, 7, 10], [0, 8, 6], [0, 9, 7], [0, 10, 8]
        ]
    ])
    
    # Intersect the sets of three face planes and return the images of the 
    # resulting points under the map sending the privileged face plane to the
    # xy-plane.
    stellation_diagram_points = np.array([
        to_xy(intersect(faces))
        for faces in face_sets_to_intersect
    ])

    return stellation_diagram_points


def stellation_regions():
    """
    Generate or load the points of the stellation diagram and return a hash
    of the possible component regions of a stellation.
    """
    points = get_stellation_diagram_points()
    # All individual regions in the stellation diagram. Contingent on the 
    # order of points chosen in generate_stellation_diagram_points().
    all_regions = [
        points[idxs] for idxs in [
            [0, 1, 2, 3, 4],
            [0, 1, 5],  [1, 2, 6], [2, 3, 7], [3, 4, 8], [4, 0, 9], 
            [0, 9, 5],  [1, 5, 6], [2, 6, 7], [3, 7, 8], [4, 8, 9],
            [5, 6, 13], [6, 7, 14], [7, 8, 10], [8, 9, 11], [9, 5, 12]
        ]
    ]
    # Regions grouped into sets of necessary mutual co-occurrence.
    regions = {
        'base': [0],                  
        'first_shell':  [1, 2, 3, 4, 5],
        'second_shell': [6, 7, 8, 9, 10],     
        'third_shell':  [11, 12, 13, 14, 15]  
    }
    stellation_regions = {
        k: [all_regions[idx] for idx in v] 
        for k, v in regions.items()
    }
    
    return stellation_regions

STELLATION_REGIONS = stellation_regions()
