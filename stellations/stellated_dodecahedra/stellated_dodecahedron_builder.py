import trimesh
import numpy as np
from utils import from_xy, build_polygon
from rotations import ROTATIONS
from stellation_regions import STELLATION_REGIONS

class StellatedDodecahedronBuilder:
    
    @classmethod
    def build_from_keys(cls, keys):
        stellation_regions = []
        for k in keys:
            try:
                stellation_regions += STELLATION_REGIONS[k]
            except KeyError:
                raise ValueError("Invalid stellation region key")

        mesh = cls.build_from_regions(stellation_regions)

        return mesh

    @classmethod
    def build_from_regions(cls, stellation_regions):
        """
        Takes an array of 2d numpy arrays (shape (n, 2)) representing the 
        selected polygons in the stellation diagram and builds a Trimesh
        model by lifting and rotating those polygons to the 12 face planes of
        the dodecahedron.
        """
        region_meshes = []

        # we'll build the mesh by building a mesh of all the 
        # rotations of each region and merging these meshes
        # at the end.
        for region in stellation_regions:
            # map the points to the special plane in R^3
            # described in from_xy
            region_3d = np.array([
                from_xy(vertex) for vertex in region
            ])
            # map these points to each of the 12 dodecahedron planes
            rotated_regions = [
                (M @ region_3d.T).T for M in ROTATIONS
            ]

            # build a mesh by building all the regions and concatenating
            # them; append to ongoing array of meshes
            region_mesh = trimesh.util.concatenate(
                [
                    build_polygon(rotated_region) 
                    for rotated_region in rotated_regions
                ]
            )
            region_meshes.append(region_mesh)

        mesh = trimesh.util.concatenate(region_meshes)
        # Fix any normals. This is hacky and shouldn't be necessary if I build
        # the polygons consistently in the first place.
        trimesh.repair.fix_normals(mesh)
        
        return mesh
    