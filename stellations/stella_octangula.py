import numpy as np
import trimesh

class StellaOctangula:

  def __init__(self, radius=1):
    self.radius = radius

  def _up_vertices(self):
    unscaled = np.array([
      [                0.0,                       0.0,        1.0],
      [                0.0,  2.0 * np.sqrt(2.0) / 3.0, -1.0 / 3.0],
      [-np.sqrt(2.0 / 3.0),       -np.sqrt(2.0) / 3.0, -1.0 / 3.0],
      [ np.sqrt(2.0 / 3.0),       -np.sqrt(2.0) / 3.0, -1.0 / 3.0]
    ])
    return self.radius * unscaled

  def _down_vertices(self):
    unscaled = np.array([
      [                0.0,                       0.0,      -1.0],
      [                0.0, -2.0 * np.sqrt(2.0) / 3.0, 1.0 / 3.0],
      [-np.sqrt(2.0 / 3.0),        np.sqrt(2.0) / 3.0, 1.0 / 3.0],
      [ np.sqrt(2.0 / 3.0),        np.sqrt(2.0) / 3.0, 1.0 / 3.0]
    ])
    return self.radius * unscaled
    
  def vertices(self):
    return np.concatenate([
        self._up_vertices(), self._down_vertices()
      ])

  def mesh(self):
    return trimesh.util.concatenate([
        trimesh.convex.convex_hull(self._up_vertices()),
        trimesh.convex.convex_hull(self._down_vertices())
      ])

  def to_stl(self):
    self.mesh().export("../stl/stella_octangula.stl")
    