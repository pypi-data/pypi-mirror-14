#!/usr/bin/env python
#
# -----------------------------------------------------------------------------
# Copyright (c) 2015-2016   Daniel Standage <daniel.standage@gmail.com>
# Copyright (c) 2015-2016   Indiana University
#
# This file is part of genhub (http://github.com/standage/genhub) and is
# licensed under the BSD 3-clause license: see LICENSE.txt.
# -----------------------------------------------------------------------------


class HiLocus(object):

    def __init__(self, record):
        self._rawdata = record
        values = record.split('\t')
        self.iloci = values[2].split(',')
        self.species = values[3].split(',')
        self.iloci_by_species = dict()
        for locus in self.iloci:
            species = locus[6:10]
            if species not in self.iloci_by_species:
                self.iloci_by_species[species] = list()
            self.iloci_by_species[species].append(locus)
        self.simple_iloci = None

    def in_clade(self, clade):
        assert self.simple_iloci
        reps = list()
        for species in clade:
            copynumber = len(self.iloci_by_species[species])
            assert copynumber > 0
            if copynumber > 1:
                continue
            ilocus = self.iloci_by_species[species]
            if ilocus not in self.simple_iloci:
                continue
            reps.append(ilocus)
        return reps
