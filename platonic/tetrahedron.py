import numpy as np
import trimesh

class Tetrahedron:

  def __init__(self, radius=1):
    self.radius = radius

  def vertices(self):
    unscaled = np.array([
      [                0.0,                       0.0,        1.0],
      [                0.0,  2.0 * np.sqrt(2.0) / 3.0, -1.0 / 3.0],
      [-np.sqrt(2.0 / 3.0),       -np.sqrt(2.0) / 3.0, -1.0 / 3.0],
      [ np.sqrt(2.0 / 3.0),       -np.sqrt(2.0) / 3.0, -1.0 / 3.0]
    ])
    return self.radius * unscaled

  def mesh(self):
    return trimesh.convex.convex_hull(self.vertices())

  def to_stl(self):
    self.mesh().export("../stl/tetrahedron.stl")
    