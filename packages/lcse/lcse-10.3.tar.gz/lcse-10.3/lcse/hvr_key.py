
class hvr_key(object):

  _keys = ['seamangle', 'section', 'subsection', 'lut',
          'hvfile', 'imagefile', 'eye', 'center', 'up', 'imagesize',
          'opacity', 'fov', 'clipping', 'ifauxclip', 'auxclip',
          'nplanes', 'singlebuffered', 'caching', 'paletted', 'tex3d',
          'tolerance', 'frameperkey', 'rotperkey', 'timeperframe',
          'render']

  def __init__(self, filename=None, data=None):
    """Initialize a .key from `filename` or dictionary `data`"""

    from lut import lut
    self.lut = lut()

    self._data = dict(seamangle=0,
                      section=[1,1,1,1],
                      subsection=[1,1,1,1],
                      hvfile='',
                      imagefile='',
                      eye=[0.0, 0.0, 1.6],
                      center=[0.0, 0.0, 0.0],
                      up=[0.0, 1.0, 0.0],
                      imagesize=[1024, 1024],
                      opacity=1.0,
                      fov=35.30840,
                      clipping=[1.100000024, 101.599998474],
                      ifauxclip=[2, 2, 2, 2, 2, 2],
                      auxclip=[[0.0, 0.0, 0.0, -0.5], [0.0, 0.0, 0.0, 0.5],
                               [0.0, 0.0, 0.0, -0.5], [0.0, 0.0, 0.0, 0.5],
                               [0.0, 0.0, 0.0, -0.5], [0.0, 0.0, 0.0, 0.0],
                               ],
                      nplanes=[4.0, 4.0],
                      singlebuffered=True,
                      caching=2,
                      paletted=1,
                      tex3d=1,
                      tolerance=[[0.0001, 1.0]],
                      frameperkey=1,
                      rotperkey=0.0,
                      timeperframe=0,
                      render=True,
                      )

    if filename:
      self.open(filename)

    if data:
      self._data.update(data)

  def __str__(self):
    """Return the string representation of the .key file with `\\r\\n` line endings """

    out = []

    for k in self._keys:
      out.extend(self._key_as_str(k))

    return '\r\n'.join(out)

  def _key_as_str(self, k):

    if k in ['seamangle', 'opacity', 'fov', 'rotperkey']:
      return ['%s\t%0.9f' % (k, self._data[k])]

    elif k in ['caching', 'paletted', 'tex3d', 'frameperkey', 'timeperframe']:
      return ['%s\t%i' % (k, self._data[k])]

    elif k in ['section', 'subsection', 'imagesize']:
      return ['%s\t%s' % (k, ' '.join('%i' % i for i in self._data[k]))]

    elif k in ['eye', 'center', 'up', 'clipping', 'nplanes']:
      return ['%s\t%s' % (k, ' '.join('%0.9f' % i for i in self._data[k]))]

    elif k in ['hvfile', 'imagefile']:
      return ['%s\t%s' % (k, self._data[k])]

    elif k == 'ifauxclip':
      return ['%s\t%i %i' % (k, i, j)for i, j in enumerate(self._data[k])]

    elif k in ['auxclip','tolerance']:
      return ['%s\t%i %s' % (k, i, ' '.join('%0.9f' % k for k in j))for i, j in enumerate(self._data[k])]

    elif k in ['singlebuffered', 'render']:
      return [k]

    elif k == 'lut':
      return [str(self.lut)]

    else:
      print("Uknown key %s" % k)
      return []

  def open(self, filename):
    """Load .key data from the file `filename`. Internally this calls `from_string`"""

    f = open(filename, 'r')
    keyfile_str = f.read()
    f.close()

    self.from_string(keyfile_str)

  def from_string(self, keyfile_str):
    """Load .key data from the string `keyfile_str`"""

    lines = [l.strip() for l in keyfile_str.splitlines() if l.strip()]

    self._data['ifauxclip'] = []
    self._data['auxclip'] = []

    lut_lines = []

    for l in lines:
      s = l.split()

      key = s[0] if len(s) > 0 else s
      key = key.strip(':')

      if not key:
        continue

      if key in ['seamangle', 'opacity', 'fov', 'rotperkey']:
        self._data[key] = float(s[1])
      elif key in ['caching', 'paletted', 'tex3d', 'frameperkey', 'timeperframe']:
        self._data[key] = int(s[1])
      elif key in ['section', 'subsection', 'imagesize']:
        self._data[key] = [int(i) for i in s[1:]]
      elif key in ['eye', 'center', 'up', 'clipping', 'nplanes']:
        self._data[key] = [float(i) for i in s[1:]]
      elif key in ['hvfile', 'imagefile']:
        self._data[key] = ' '.join(s[1:]) if len(s) > 0 else ''
      elif key == 'tolerance':
        self._data[key] = [[float(i) for i in s[2:]], ]
      elif key == 'ifauxclip':
        self._data[key].append(int(s[2]))
      elif key == 'auxclip':
        self._data[key].append([float(i) for i in s[2:]])
      elif key in ['Cnot', 'Anot']:
        lut_lines.append(l)
      elif key in ['singlebuffered', 'render']:
        self._data[key] = True

    self.lut.load(lut_lines)

  def save(self, filename):
    """Write .key data to the file `filename`. Internally this calls `f.write(self.__str__())`"""

    with open(filename, 'w') as f:
      f.write(self.__str__())

  def get(self, key):
    """ Get the value of `key` """

    return self._data.get(key)

  def set(self, key, value):
    """Set the value of `key` to `value`"""

    self._data[key] = value

  def update(self, d):
    """Merge the values in `d` with internal data"""
    self._data.update(d)

  def to_dict(self):
    """Convert to dictionary"""

    return dict(self._data)

if __name__ == '__main__':
  import sys
  k = hvr_key(sys.argv[1])
  print(k)

