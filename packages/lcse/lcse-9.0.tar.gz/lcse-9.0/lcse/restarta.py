
import os
import struct

class restarta_reader(object):

  aaa_vars = ['g', 'TransitionThickness', 'DisplaceAmpl', 'GammaAir', 'GammaCld(1)', 'RhoCldToAir0(1)', 'BrickWidth',
              'BrickHeight', 'BrickDepth', 'rho00', 'p00', 'VX0', 'VX0Air', 'VX0Cld', 'VCirculationAir', 'VCirculationCld',
              'Ampl1', 'Ampl11', 'VY1', 'VY11', 'asymm', 'SoundSpeed0Air', 'SoundSpeed0Cld', 'ux0', 'ux1', 'uy0', 'uy1',
              'uz0', 'uz1', 'vx0sq', 'rho0', 'rho1', 'p0', 'p1', 's00', 's01', 's0', 's1', 'fv0', 'fv1', 'vort0', 'vort1',
              'divu0', 'divu1', 'deex', 'dtinit', 'safety', 'difcon', 'shkjmp', 'wavhaf',
              # This is from argsimg (apparently corrupt)
              'vort0', 'vort1', 'divu0', 'divu1', 's0', 's1', 'fv0', 'fv1', 'rho0', 'rho1', 'p0', 'p1', 'ux0', 'ux1',
              'uy0', 'uy1', 'uz0', 'uz1'
              # This is from the second part (it's garbage in the 64bit version)
              'smlrho', 'smallp', 'smalle', 'smallu', 'plotsperperiod', 'periods', 'tstop', 'dtdump', 'airmu', 'cldmu',
              'fkair', 'fkcld', 'Rgasconst', 'atomicnoair', 'atomicnocld', 'qc12pgammaMEV', 'CN'
              ]

  iaaa_vars = ['ifmpi', 'ifnompi', 'nhalfwaves', 'NTXBricks', 'NTYBricks', 'NTZBricks', 'NXTeams', 'NYTeams', 'NZTeams',
               'NTeams', 'NXBricks', 'NYBricks', 'NZBricks', 'NBricks', 'ncpucores', 'n', 'nx', 'ny', 'nz', 'nsugar',
               'nbdy', 'nbdy1', 'nghostcubes', 'nsugarsq', 'nsugarcubed', 'ncubes', 'ncubesx', 'ncubesy', 'ncubesz',
               'ncubessq', 'ncubescubed', 'ncubesmx', 'ncubesmxmn', 'ifthunder', 'nfluids', 'nvars', 'nvars4',
               'ninsugarcubette', 'ninsugarcube', 'nbrick', 'NDumps', 'n11', 'NcyclesPerDump', 'Nloops', 'NDump']

  filename = 'restarta0.dmpaaa'

  def __init__(self, path, lazy=True):

    self.path = path
    self.lazy = lazy

    self.aaa = {}
    self.iaaa = {}

    self.open(path)

  def open(self, path):

    if not path.endswith(self.filename):
      path = os.path.join(path, self.filename)

    len_aaa_vars = len(restarta_reader.aaa_vars)
    len_iaaa_vars = len(restarta_reader.iaaa_vars)

    f = open(path, 'r')
    data = f.read(2*512)
    f.close()

    self.aaa = dict([(str(restarta_reader.aaa_vars[i].lower()),v) for i, v in enumerate(struct.unpack(len_aaa_vars * 'd', data[: len_aaa_vars * 8]))])
    self.iaaa  = dict([(str(restarta_reader.iaaa_vars[i].lower()),v) for i, v in enumerate(struct.unpack(len_iaaa_vars * 'i', data[4 * 128 : 4*128 + len_iaaa_vars * 4]))])

    #nndumpstot = 3000
    #lenglobprof= self.iaaa['ny'] * self.iaaa['NTYBricks'] * self.iaaa['NYTeams'] * (nndumpstot+1)*35
    #lenglobthist = (nndumpstot + 1) * 35

    # globprofile(ny*NTYBricks*NYTeams,0:nndumpstot,35)
    #global_profile = data[8 * 512 : 8 * (512 + lenglobprof)]

    # globthist(0:nndumpstot,35)
    #global_time_history = data[8 * (512+lenglobprof) :  8 * (512 + lenglobprof + lenglobthist)]

    # radprof(lenradprof)
#    radprof_data = data[8 * (512+lenglobprof+lenglobthist) : 8 * (512+lenglobprof+lenglobthist + lenradprof)]

def main():
  import sys
  import os

  if len(sys.argv) > 1:

    r = restarta_reader(sys.argv[1])

    for k,v in r.iaaa.iteritems():
      print("%s\t%s" % (k, v))

  else:

    for p in ['restart0', 'restart1']:

      if not os.path.exists(p):
        continue

      r = restarta_reader(p)

      print '%s is dump %04i' % (p, r.iaaa.get('ndump'))

    if os.path.exists('PPMrestart.ppm'):
      print "PPMrestart.ppm:\n %s" % open('PPMrestart.ppm').read()

if __name__ == '__main__':
  main()

