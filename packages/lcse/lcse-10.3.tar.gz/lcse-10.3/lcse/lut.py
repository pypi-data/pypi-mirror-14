'''
Created on May 3, 2015

@author: stou
'''

import numpy as np
import os

class lut(object):
  """Represents a colormap (.lut) file"""

  def __init__(self, filename=None, name=None, alphas=None, colors=None):
    """
    `filename` to load OR arrays of arryays
    `colors` (val, R, G, B) and
    `alphas` (val, opacity) where R, G, B and opacity are in [0, 1.0] and val is [0, 255]
    """

    self.name = name

    if filename:
      self.open(filename)
      import os
    else:
      self.c_knots = colors or [[0, 0.0, 0.0, 0.0], [255, 1.0, 1.0, 1.0]]
      self.a_knots = alphas or [[0, 0.0], [255, 1.0]]

  def open(self, filename):
    """ Load .lut from `filename` """

    f = open(filename, 'r')
    self.load(f.readlines())
    f.close()

    self.name = os.path.splitext(os.path.basename(filename))[0]

  def load(self, lut_lines):
    """ Parse lut lines """

    self.a_knots = [self.parseKnot(l) for l in lut_lines if l.startswith('Anot')]
    self.c_knots = [self.parseKnot(l) for l in lut_lines if l.startswith('Cnot')]

  def save(self, filename):
    """ Save a lut to the given `filename`"""

    f = open(filename, 'w')
    f.write(self.__str__())
    f.close()

  def parseKnot(self, line):

    s = [k for k in line[5:].strip().split(' ')]

    d = [int(s[0])]
    d.extend([float(i) for i in s[1:]])

    return d

  def getFunctions(self):
    import numpy as np
    from scipy.interpolate import interp1d

    anot_array = np.array(self.a_knots, dtype=np.float32)
    cnot_array = np.array(self.c_knots, dtype=np.float32).reshape(-1, 4)

    f_color = interp1d(cnot_array[:, 0], cnot_array[:, 1:].T)
    f_alpha = interp1d(anot_array[:, 0], anot_array[:, 1])

    return f_color, f_alpha

  def rgba1D(self, size=None):
    f_color, f_alpha = self.getFunctions()
    x = np.arange(size or 256, dtype=np.float32)

    return np.vstack((f_color(x), f_alpha(x))).T

  def toDict(self):
    """ Return the colormap as a dictionary suitable for JSON conversion"""
    return dict(name=self.name, colors=self.c_knots, alphas=self.a_knots)

  def __str__(self):

    lines = []

    for n in self.c_knots:
      line = 'Cnot:\t%i %s' % (n[0], ' '.join('%0.7f' % k for k in n[1:]))
      lines.append(line)

    for n in self.a_knots:
      line = 'Anot:\t%i %s' % (n[0], ' '.join('%0.7f' % k for k in n[1:]))
      lines.append(line)

    return '\n'.join(lines)

if __name__ == '__main__':
  import sys
  print lut(filename=sys.argv[1])

