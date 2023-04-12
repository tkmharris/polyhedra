import numpy as np
import trimesh

class Permutahedron:

  def __init__(self, radius=1):
    self.radius = radius

  def vertices(self):
    invsqrt2 = 1.0 / np.sqrt(2.0)
    unscaled = np.array([
      [ (1.0 / 3.0) * invsqrt2,  (1.0 / 3.0) * invsqrt2,  (2.0 / 3.0)],
      [ (1.0 / 3.0) * invsqrt2,  (1.0 / 3.0) * invsqrt2, -(2.0 / 3.0)],
      [ (1.0 / 3.0) * invsqrt2, -(1.0 / 3.0) * invsqrt2,  (2.0 / 3.0)],
      [ (1.0 / 3.0) * invsqrt2, -(1.0 / 3.0) * invsqrt2, -(2.0 / 3.0)],
      [-(1.0 / 3.0) * invsqrt2,  (1.0 / 3.0) * invsqrt2,  (2.0 / 3.0)],
      [-(1.0 / 3.0) * invsqrt2,  (1.0 / 3.0) * invsqrt2, -(2.0 / 3.0)],
      [-(1.0 / 3.0) * invsqrt2, -(1.0 / 3.0) * invsqrt2,  (2.0 / 3.0)],
      [-(1.0 / 3.0) * invsqrt2, -(1.0 / 3.0) * invsqrt2, -(2.0 / 3.0)],
      [ (2.0 / 3.0) * invsqrt2,  (2.0 / 3.0) * invsqrt2,  (1.0 / 3.0)],
      [ (2.0 / 3.0) * invsqrt2,  (2.0 / 3.0) * invsqrt2, -(1.0 / 3.0)],
      [ (2.0 / 3.0) * invsqrt2, -(2.0 / 3.0) * invsqrt2,  (1.0 / 3.0)],
      [ (2.0 / 3.0) * invsqrt2, -(2.0 / 3.0) * invsqrt2, -(1.0 / 3.0)],
      [-(2.0 / 3.0) * invsqrt2,  (2.0 / 3.0) * invsqrt2,  (1.0 / 3.0)],
      [-(2.0 / 3.0) * invsqrt2,  (2.0 / 3.0) * invsqrt2, -(1.0 / 3.0)],
      [-(2.0 / 3.0) * invsqrt2, -(2.0 / 3.0) * invsqrt2,  (1.0 / 3.0)],
      [-(2.0 / 3.0) * invsqrt2, -(2.0 / 3.0) * invsqrt2, -(1.0 / 3.0)],
      [               invsqrt2,  (1.0 / 3.0) * invsqrt2,          0.0],
      [               invsqrt2, -(1.0 / 3.0) * invsqrt2,          0.0],
      [              -invsqrt2,  (1.0 / 3.0) * invsqrt2,          0.0],
      [              -invsqrt2, -(1.0 / 3.0) * invsqrt2,          0.0],
      [ (1.0 / 3.0) * invsqrt2,                invsqrt2,          0.0],
      [ (1.0 / 3.0) * invsqrt2,               -invsqrt2,          0.0],
      [-(1.0 / 3.0) * invsqrt2,                invsqrt2,          0.0],
      [-(1.0 / 3.0) * invsqrt2,               -invsqrt2,          0.0]
    ])
    return self.radius * (9.0 / 5.0) * unscaled

  def mesh(self):
    return trimesh.convex.convex_hull(self.vertices())

  def to_stl(self):
    self.mesh().export("../stl/permutahedron.stl")
    