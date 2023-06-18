import numpy as np

class Dodecahedron:
  """
  Class containing a model for the standard dodecahedron inscribed in the unit
  sphere.
  """

  def __init__(self, radius=1):
    self.radius = radius
    self.vertices = self._vertices()
    self.faces = self._faces()

  def _vertices(self):
    φ = (1.0 + np.sqrt(5.0)) / 2.0
    unscaled = (1.0 / np.sqrt(3.0)) * np.array([
        [     1.0,      1.0,      1.0],
        [     1.0,      1.0,     -1.0],
        [     1.0,     -1.0,      1.0],
        [     1.0,     -1.0,     -1.0],
        [    -1.0,      1.0,      1.0],
        [    -1.0,      1.0,     -1.0],
        [    -1.0,     -1.0,      1.0],
        [    -1.0,     -1.0,     -1.0],
        [       φ,  1.0 / φ,      0.0],
        [       φ, -1.0 / φ,      0.0],
        [      -φ,  1.0 / φ,      0.0],
        [      -φ, -1.0 / φ,      0.0],
        [     0.0,        φ,  1.0 / φ],
        [     0.0,        φ, -1.0 / φ],
        [     0.0,       -φ,  1.0 / φ],
        [     0.0,       -φ, -1.0 / φ],
        [ 1.0 / φ,      0.0,        φ],
        [ 1.0 / φ,      0.0,       -φ],
        [-1.0 / φ,      0.0,        φ],
        [-1.0 / φ,      0.0,       -φ],
      ])
    return self.radius * unscaled
  
  def _faces(self):
    face_vertices = [
        [0, 2, 8, 9, 16], 
        [2, 6, 14, 16, 18], 
        [2, 3, 9, 14, 15], 
        [1, 3, 8, 9, 17], 
        [0, 1, 8, 12, 13], 
        [0, 4, 12, 16, 18], 
        [4, 6, 10, 11, 18], 
        [6, 7, 11, 14, 15], 
        [3, 7, 15, 17, 19], 
        [1, 5, 13, 17, 19], 
        [4, 5, 10, 12, 13], 
        [5, 7, 10, 11, 19]
      ]
    faces = np.array([
      self.vertices[face,:] for face in face_vertices
    ])
    return faces

    
    