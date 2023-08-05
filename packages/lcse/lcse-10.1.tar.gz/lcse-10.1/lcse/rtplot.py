"""
Reader for PPMs RTPlot.ppm files
"""

import os

class rtplot_reader(object):
  """Reader for PPMs RTPlot.ppm files"""

  header = ['dump', 'cycle', 'time', 'T', 'dt', 'courant', 'bubble_ht', 'spike_ht', 'bubble_uy', 'spike_uy']

  def __init__(self, path):
    """ Load the RTplot.ppm given by `path` or found at `path` + /RTPlot.ppm

    `rtplot_reader.dump_map` maps dump numbers to dicts of each RTPlot.ppm line.
    `rtplot_reader.header` contains the list of variable keys
    """

    self.dump_map = {}

    if not path.endswith('RTplot.ppm'):
      path = os.path.join(path, 'RTplot.ppm')


    with open(path, 'r') as f:
      rt_plot_lines = f.readlines()

      for l in rt_plot_lines:
        if l.startswith('#'):
          continue

        terms = [t.strip() for t in l.split(' ') if t.strip()]

        if len(terms) != 10:
          continue

        dump = int(terms[0])
        data = {}

        for label, t in zip(self.header[1:], terms[1:]):

          try:
            v = float(t)
          except ValueError:
            v = 0.0

          data[label] = v

          self.dump_map[dump] = data

