from __future__ import (absolute_import, division, print_function)

import numpy as np

from .astronomy import ut_astron
from . import ut_constants
from . import constit_index_dict
from .utilities import Bunch


def ut_cnstitsel(tref, minres, incnstit, infer):
    """
    UT_CNSTITSEL()
    carry out constituent selection
    inputs
      tref = reference time (datenum UTC)
      minres = freq separation (cph) used in decision tree
      incnstit = 'cnstit' input to ut_solv
      infer = 'opt.infer' input to ut_solv
    outputs
      nNR,nR,nI = number non-reference, reference, inferred constituents
      cnstit.NR.name = cellstr of 4-char names of NR constits
      cnstit.NR.frq = frequencies (cph) of NR constits
      cnstit.NR.lind = list indices (in ut_constants.mat) of NR constits
      cnstit.R = empty if no inference; otherwise, for each (i'th) R constit:
          cnstit.R{i}.name, .frq, .lind = as above, but for R constits
          cnstit.R{i}.I{j}.name, .frq, .lind = as above for j'th I constit
      coef.name = cellstr of names of all constituents (NR, R, and I)
      coef.aux.frq = frequencies (cph) of all constituents
      coef.aux.lind = list indices of all constituents
      coef.aux.reftime = tref
    UTide v1p0 9/2011 d.codiga@gso.uri.edu
    """

    shallow = ut_constants.shallow
    const = ut_constants.const

    cnstit = Bunch()
    coef = Bunch()

    astro, ader = ut_astron(tref)

    ii = np.isfinite(const.ishallow)
    const.freq[~ii] = np.dot(const.doodson[~ii, :], ader) / 24

    for k in ii.nonzero()[0]:
        ik = const.ishallow[k]+np.arange(const.nshallow[k])
        ik = ik.astype(int)-1
        const.freq[k] = np.sum(const.freq[shallow.iname[ik] - 1] *
                               shallow.coef[ik])

    # cnstit.NR
    cnstit['NR'] = Bunch()

    # if incnstit.lower() == 'auto':
    if incnstit == 'auto':
        cnstit['NR']['lind'] = np.where(const.df >= minres)[0]
    else:
        ilist = [constit_index_dict[n] for n in incnstit]
        cnstit['NR']['lind'] = np.array(ilist, dtype=int)

#        if ordercnstit == 'frq':
#            seq = const.freq[cnstit['NR']['lind']].argsort()
#            tmp = cnstit['NR']['lind'][seq].astype(int).
#            cnstit['NR']['lind'] = tmp.flatten()

    # Skipped some stuff here cause they involve infer.

    cnstit['NR']['frq'] = const.freq[cnstit['NR']['lind']]
    cnstit['NR']['name'] = const.name[cnstit['NR']['lind']]
    nNR = len(cnstit['NR']['frq'])

    # cnstit.R
    nR = 0
    nI = 0
    cnstit['R'] = []  # Empty because inference is not supported yet.

    coef['name'] = cnstit['NR']['name']
    coef['aux'] = Bunch(frq=cnstit.NR.frq,
                        lind=cnstit.NR.lind,
                        reftime=tref)

    return nNR, nR, nI, cnstit, coef
