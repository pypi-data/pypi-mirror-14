# Copyright (C) 2011 Atsushi Togo
# All rights reserved.
#
# This file is part of phonopy.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# * Neither the name of the phonopy project nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import numpy as np
from phonopy.units import VaspToTHz

def estimate_band_connection(prev_eigvecs, eigvecs, prev_band_order):
    metric = np.abs(np.dot(prev_eigvecs.conjugate().T, eigvecs))
    connection_order = []
    for overlaps in metric:
        maxval = 0
        for i in reversed(range(len(metric))):
            val = overlaps[i]
            if i in connection_order:
                continue
            if val > maxval:
                maxval = val
                maxindex = i
        connection_order.append(maxindex)

    band_order = [connection_order[x] for x in prev_band_order]
        
    return band_order


class BandStructure:
    def __init__(self,
                 paths,
                 dynamical_matrix,
                 is_eigenvectors=False,
                 is_band_connection=False,
                 group_velocity=None,
                 factor=VaspToTHz,
                 verbose=False):
        self._dynamical_matrix = dynamical_matrix
        self._cell = dynamical_matrix.get_primitive()
        self._factor = factor
        self._is_eigenvectors = is_eigenvectors
        self._is_band_connection = is_band_connection
        if is_band_connection:
            self._is_eigenvectors = True
        self._group_velocity = group_velocity
            
        self._paths = [np.array(path) for path in paths]
        self._distances = []
        self._distance = 0.
        self._special_point = [0.]
        self._eigenvalues = None
        self._eigenvectors = None
        self._frequencies = None
        self._set_band(verbose=verbose)

    def get_distances(self):
        return self._distances

    def get_qpoints(self):
        return self._paths

    def get_eigenvalues(self):
        return self._eigenvalues

    def get_eigenvectors(self):
        return self._eigenvectors

    def get_frequencies(self):
        return self._frequencies

    def get_group_velocities(self):
        return self._group_velocities
    
    def get_unit_conversion_factor(self):
        return self._factor
    
    def plot(self, pyplot, symbols=None):
        for distances, frequencies in zip(self._distances,
                                          self._frequencies):
            for freqs in frequencies.T:
                if self._is_band_connection:
                    pyplot.plot(distances, freqs, '-')
                else:
                    pyplot.plot(distances, freqs, 'r-')

        pyplot.ylabel('Frequency')
        pyplot.xlabel('Wave vector')
        if symbols and len(symbols)==len(self._special_point):
            pyplot.xticks(self._special_point, symbols)
        else:
            pyplot.xticks(self._special_point, [''] * len(self._special_point))
        pyplot.xlim(0, self._distance)
        pyplot.axhline(y=0, linestyle=':', linewidth=0.5, color='b')

    def write_yaml(self):
        w = open('band.yaml', 'w')
        natom = self._cell.get_number_of_atoms()
        lattice = np.linalg.inv(self._cell.get_cell()) # column vectors
        nqpoint = 0
        for qpoints in self._paths:
            nqpoint += len(qpoints)
        w.write("nqpoint: %-7d\n" % nqpoint)
        w.write("npath: %-7d\n" % len(self._paths))
        w.write("natom: %-7d\n" % (natom))
        w.write("reciprocal_lattice:\n")
        for vec, axis in zip(lattice.T, ('a*', 'b*', 'c*')):
            w.write("- [ %12.8f, %12.8f, %12.8f ] # %2s\n" %
                    (tuple(vec) + (axis,)))
        w.write("phonon:\n")
        for i, (qpoints, distances, frequencies) in enumerate(zip(
            self._paths,
            self._distances,
            self._frequencies)):
             for j, q in enumerate(qpoints):
                w.write("- q-position: [ %12.7f, %12.7f, %12.7f ]\n" % tuple(q))
                w.write("  distance: %12.7f\n" % distances[j])
                w.write("  band:\n")
                for k, freq in enumerate(frequencies[j]):
                    w.write("  - # %d\n" % (k + 1))
                    w.write("    frequency: %15.10f\n" % freq)
    
                    if self._group_velocity is not None:
                        gv = self._group_velocities[i][j, k]
                        w.write("    group_velocity: ")
                        w.write("[ %13.7f, %13.7f, %13.7f ]\n" % tuple(gv))
                        
                    if self._is_eigenvectors:
                        eigenvectors = self._eigenvectors[i]
                        w.write("    eigenvector:\n")
                        for l in range(natom):
                            w.write("    - # atom %d\n" % (l + 1))
                            for m in (0, 1, 2):
                                w.write("      - [ %17.14f, %17.14f ]\n" %
                                        (eigenvectors[j, l * 3 + m, k].real,
                                         eigenvectors[j, l * 3 + m, k].imag))

                        
                w.write("\n")

    def _set_initial_point(self, qpoint):
        self._lastq = qpoint.copy()

    def _shift_point(self, qpoint):
        self._distance += np.linalg.norm(
            np.dot(qpoint - self._lastq,
                   np.linalg.inv(self._cell.get_cell()).T))
        self._lastq = qpoint.copy()

    def _set_band(self, verbose=False):
        eigvals = []
        eigvecs = []
        group_velocities = []
        distances = []
        is_nac = self._dynamical_matrix.is_nac()

        for path in self._paths:
            self._set_initial_point(path[0])

            (distances_on_path,
             eigvals_on_path,
             eigvecs_on_path,
             gv_on_path) = self._solve_dm_on_path(path,
                                                  verbose)

            eigvals.append(np.array(eigvals_on_path))
            if self._is_eigenvectors:
                eigvecs.append(np.array(eigvecs_on_path))
            if self._group_velocity is not None:
                group_velocities.append(np.array(gv_on_path))
            distances.append(np.array(distances_on_path))
            self._special_point.append(self._distance)

        self._eigenvalues = eigvals
        if self._is_eigenvectors:
            self._eigenvectors = eigvecs
        if self._group_velocity is not None:
            self._group_velocities = group_velocities
        self._distances = distances
        
        self._set_frequencies()

    def _solve_dm_on_path(self, path, verbose):
        is_nac = self._dynamical_matrix.is_nac()
        distances_on_path = []
        eigvals_on_path = []
        eigvecs_on_path = []
        gv_on_path = []

        if self._group_velocity is not None:
            self._group_velocity.set_q_points(path)
            gv = self._group_velocity.get_group_velocity()
        
        for i, q in enumerate(path):
            self._shift_point(q)
            distances_on_path.append(self._distance)
            
            if is_nac:
                q_direction = None
                if (np.abs(q) < 0.0001).all(): # For Gamma point
                    q_direction = path[0] - path[-1]
                self._dynamical_matrix.set_dynamical_matrix(
                    q, q_direction=q_direction, verbose=verbose)
            else:
                self._dynamical_matrix.set_dynamical_matrix(
                    q, verbose=verbose)
            dm = self._dynamical_matrix.get_dynamical_matrix()

            if self._is_eigenvectors:
                eigvals, eigvecs = np.linalg.eigh(dm)
                eigvals = eigvals.real
            else:
                eigvals = np.linalg.eigvalsh(dm).real

            if self._is_band_connection:
                if i == 0:
                    band_order = range(len(eigvals))
                else:
                    band_order = estimate_band_connection(prev_eigvecs,
                                                          eigvecs,
                                                          band_order)
                eigvals_on_path.append(eigvals[band_order])
                eigvecs_on_path.append((eigvecs.T)[band_order].T)

                if self._group_velocity is not None:
                    gv_on_path.append(gv[i][band_order])
                prev_eigvecs = eigvecs
            else:
                eigvals_on_path.append(eigvals)
                if self._is_eigenvectors:
                    eigvecs_on_path.append(eigvecs)
                if self._group_velocity is not None:
                    gv_on_path.append(gv[i])

        return distances_on_path, eigvals_on_path, eigvecs_on_path, gv_on_path

    def _set_frequencies(self):
        frequencies = []
        for eigs_path in self._eigenvalues:
            frequencies.append(np.sqrt(abs(eigs_path)) * np.sign(eigs_path)
                               * self._factor)
        self._frequencies = frequencies
