import numpy as np
import trimesh

class Cube:

  def __init__(self, radius=1):
    self.radius = radius

  def vertices(self):
    unscaled = np.array([
      [ 1.0,  1.0,  1.0],
      [ 1.0,  1.0, -1.0],
      [ 1.0, -1.0,  1.0],
      [ 1.0, -1.0, -1.0],
      [-1.0,  1.0,  1.0],
      [-1.0,  1.0, -1.0],
      [-1.0, -1.0,  1.0],
      [-1.0, -1.0, -1.0]
    ])
    return self.radius * (1.0 / np.sqrt(3.0)) * unscaled

  def mesh(self):
    return trimesh.convex.convex_hull(self.vertices())

  def to_stl(self):
    self.mesh().export("../stl/cube.stl")
