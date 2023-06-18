import numpy as np

def to_xy_plane(pt):
  """
  Map from R^3 -> R^2 calibrated so that the
  midpoint of the face of the unit icosahedron
  given by:
    [ 1.0,    φ,  0.0]
    [-1.0,    φ,  0.0]
    [ 0.0,  1.0,    φ]
  is sent to the origin and such that the map
  acts isometrically when restricted to the 
  plane containing this face.
  """
  φ = (1.0 + np.sqrt(5.0)) / 2.0
  scale_factor = (1.0 / np.sqrt(1.0 + φ**2))
  midpoint = (1 / 3.0) * np.array([0.0, 1.0 + 2 * φ, φ])

  # rotation matrix
  R = np.array([
    [1.0,                      0.0,                      0.0],
    [0.0,         φ / np.sqrt(3.0), (φ - 1.0) / np.sqrt(3.0)],
    [0.0, (1.0 - φ) / np.sqrt(3.0),         φ / np.sqrt(3.0)],
    ])

  # translation vector
  t = np.array([0.0, -np.linalg.norm(midpoint), 0.0])

  # rotate, translate, and drop second coordinate
  return np.delete(R @ pt + t, 1)

def intersection_line(m0, m1):
  """
  Find the line of intersection of the pair of planes defined by:
  m0 . (x - m0) = 0
  m1 . (x - m1) = 0
  (These are the face planes of the icosahedron when mi is the 
  midpoint of each face.)

  See https://math.stackexchange.com/a/1937116
  """
  M = np.array([
    [  2.0,   0.0,   0.0, m0[0], m1[0]],
    [  0.0,   2.0,   0.0, m0[1], m1[1]],
    [  0.0,   0.0,   2.0, m0[2], m1[2]],
    [m0[0], m0[1], m0[2],   0.0,   0.0],
    [m1[0], m1[1], m1[2],   0.0,   0.0],
  ])

  b = np.array([
      0.0, 0.0, 0.0, np.dot(m0, m1), np.dot(m0, m1)
    ])

  specific_point = np.linalg.solve(M, b)[0:3]
  direction = np.cross(m0, m1)

  return specific_point, direction

import drawsvg as draw

d = draw.Drawing(200, 200, origin='center')

# Draw an irregular polygon
d.append(draw.Lines(-80, 45,
                     70, 49,
                     95, -49,
                    -90, -40,
                    close=False,
            fill='#eeee00',
            stroke='black'))
d.save_png('example.png')