import itertools.chain

class DodecahedronStellationBuilder:
    φ = (1.0 + np.sqrt(5.0)) / 2.0

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
        form a dodecahedron inscribed in the unit spehre.
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

        return [
                I,         R,         R @ R,
                S,     R @ S,     R @ R @ S,
                T,     R @ T,     R @ R @ T,
            T @ S, R @ T @ S, R @ R @ T @ S,
        ]
    ROTATIONS = generate_rotations()

    def _to_xy(xyz_pt):
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
        xy0_pt = np.linalg.inv(R) @ (xyz_pt - t)

        # drop final coordinate
        return (R @ xy0_pt + t)[:2]

    def _from_xy(xy_pt):
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
        xy0_pt = np.pad(pt, (0,1))

        # translate and rotate point
        return np.linalg.inv(R) @ (xy0_pt + t)

    # vectorize these functions
    to_xy = np.vectorize(_to_xy)
    from_xy = np.vectorize(_from_xy)
    
    def build(stellation_regions):
        meshes = []

        # we'll build the mesh by building a mesh of all the 
        # rotations of each region and merging these meshes
        # at the end.
        for region in itertools.chain(*stellation_regions):
            # map the points to the special plane in R^3
            # described in _from_xy
            region_3d = from_xy(region)
            
            # map these points to each of the 12 dodecahedron planes
            rotated_regions = [
                (M @ region_3d).T for M in ROTATIONS
            ]

            # build a mesh by building all the regions and concatenating
            # them; append to ongoing array of meshes
            mesh = trimesh.util.concatenate(
                [
                    build_mesh(rotated_region) # build mesh not yet implemented
                    for rotated_region in rotated_regions
                ]
            )
            meshes.append(mesh)
        
        return trimesh.util.concatenate(meshes)

            



