import numpy as np

class Cube:

  def __initialize__(self, radius=1):
    self.radius = radius

  def vertices(self, radius):
    self.radius * (1.0 / np.sqrt(2)) * np.array([
      [1.0, 1.0, 1.0],
      [1.0, 1.0, -1.0],
      [1.0, -1.0, 1.0],
      [1.0, -1.0, -1.0],
      [-1.0, 1.0, -1.0],
      [-1.0, -1.0, 1.0],
      [-1.0, 1.0, -1.0],
      [-1.0, -1.0, -1.0]
    ])

  def mesh(self):
    return trimesh.convex.convex_hull(self.vertices())

  def stl(self):
    trimesh.exchange.stl("stl/cube.stl")
