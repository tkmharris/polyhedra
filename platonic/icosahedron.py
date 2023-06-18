import numpy as np
import trimesh

class Icosahedron:

  def __init__(self, radius=1):
    self.radius = radius

  def vertices(self):
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
        [   φ,  0.0, -1.0],
        [  -φ,  0.0,  1.0],
        [  -φ,  0.0, -1.0]
    ])
    return self.radius * (1.0 / np.sqrt(1.0 + φ**2)) * unscaled

  def faces(self):
    indices = [
      []
    ]

  def mesh(self):
    return trimesh.convex.convex_hull(self.vertices())

  def to_stl(self):
    self.mesh().export("stl/icosahedron.stl")
    