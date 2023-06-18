import numpy as np
import trimesh

class SmallTriambicIcosahedron:

  def __init__(self, radius=1):
    self.radius = radius

  def icosahedron_vertices(self):
    φ = (1.0 + np.sqrt(5.0)) / 2.0
    unscaled = np.array([
        [ 1.0,    φ,  0.0],
        [ 1.0,   -φ,  0.0],
        [-1.0,    φ,  0.0],
        [-1.0,   -φ,  0.0],
        [ 0.0,  1.0,    φ],
        [ 0.0,  1.0,   -φ],
        [ 0.0, -1.0,    φ],
        [ 0.0, -1.0,   -φ],
        [   φ,  0.0,  1.0],
        [  -φ,  0.0,  1.0],
        [   φ,  0.0, -1.0],
        [  -φ,  0.0, -1.0]
    ])
    return self.radius * (1.0 / np.sqrt(1.0 + φ**2)) * unscaled
  
  def icosahedron_faces(self):
    vertices = self.icosahedron_vertices()
    return np.array([
      [vertices[0], vertices[4], vertices[8]],
      [vertices[0], vertices[5], vertices[10]],
      [vertices[1], vertices[6], vertices[8]],
      [vertices[1], vertices[7], vertices[10]],
      [vertices[2], vertices[4], vertices[9]],
      [vertices[2], vertices[5], vertices[11]],
      [vertices[3], vertices[6], vertices[9]],
      [vertices[3], vertices[7], vertices[11]],
      [vertices[0], vertices[2], vertices[4]],
      [vertices[0], vertices[2], vertices[5]],
      [vertices[1], vertices[3], vertices[6]],
      [vertices[1], vertices[3], vertices[7]],
      [vertices[4], vertices[6], vertices[8]],
      [vertices[4], vertices[6], vertices[9]],
      [vertices[5], vertices[7], vertices[10]],
      [vertices[5], vertices[7], vertices[11]],
      [vertices[8], vertices[10], vertices[0]],
      [vertices[8], vertices[10], vertices[1]],
      [vertices[9], vertices[11], vertices[2]],
      [vertices[9], vertices[11], vertices[3]]
    ])

  def mesh(self):
    # regular icosahedron mesh
    icos_mesh = trimesh.convex.convex_hull(self.icosahedron_vertices())
    pyramids = []
    for face in self.icosahedron_faces():
      # for each face, build a pyramid of the right height with the face as its base
      vertex = (3.0 / np.sqrt(5.0)) * face.mean(axis=0)
      pyramid = trimesh.convex.convex_hull(
        np.vstack([face, vertex])
      )
      pyramids.append(pyramid)
    # merge the pyramids onto the icosahedron
    mesh = trimesh.util.concatenate(
      [icos_mesh] + pyramids
    )
    return mesh
      
  def to_stl(self):
    self.mesh().export("stl/small_triambic_icosahedron.stl")
    