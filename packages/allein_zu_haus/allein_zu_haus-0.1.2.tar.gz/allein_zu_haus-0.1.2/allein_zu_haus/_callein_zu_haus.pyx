from libcpp.pair cimport pair
from libcpp.vector cimport vector
cimport numpy as np
import numpy as np


ctypedef vector[vector[double]] _mat_t
ctypedef vector[char] alignment_t


cdef extern from "align.hpp":
    cdef cppclass aligner:
        aligner(
            size_t max_read_size,
            size_t max_ref_size,
            size_t mismatch_penalty,
            size_t open_gap_penalty,
            size_t extend_gap_penalty)

        void init(
            size_t read_size,
            const char *const read,
            const double *const read_bp_prob,
            const double *const base_probs,
            size_t ref_size,
            const char *const ref)

        double match_bps(
            size_t i,
            size_t j)

        pair[size_t, size_t] step()

        _mat_t get_in_read_gap_mat()
        _mat_t get_outside_gap_mat()
        _mat_t get_in_ref_gap_mat()

        double get_inf_penalty()
        double get_min()
        size_t get_max_read_size()
        size_t get_max_ref_size()
        alignment_t get_alignment()


cdef class Aligner:
    """
    Performs local alignments using the

    This class is optimized for repeated alignments (e.g.,

    Arguments:
    max_read_size: max length of reads that will be aligned.
    max_ref_size: max length of reference subsequences that will be aligned.
    mismatch_penalty: positive penalty for mismatch.
    open_gap_penalty: positive penalty for gap opening.
    extend_gap_penalty: positive penalty of gep extension.
    """
    cdef aligner *_imp
    cdef double[:] _base_probs

    def __cinit__(self,
            max_read_size,
            max_ref_size,
            mismatch_penalty,
            open_gap_penalty,
            extend_gap_penalty):
        self._imp = new aligner(
            max_read_size,
            max_ref_size,
            mismatch_penalty,
            open_gap_penalty,
            extend_gap_penalty)

    def match(self,
              read,
              read_bp_probs,
              base_probs,
              ref):
        """
        Arguments:
            read: numpy array of characters in read sequence
            read_bp_probs: Probability that reported basepair is the actual basepair (P(\hat{B}=b | B=b)= 1 - Pe, where Pe is the error probability extracted from the basepair quality string)
            base_probs: Prior probabilities for nucleotides
            ref: numpy array of characters in reference subsequence
        """
        return self._match_imp(
              read,
              read_bp_probs,
              base_probs,
              ref)

    def _match_imp(self,
            read,
            read_bp_probs,
            base_probs,
            ref,
            verbose=False):

        self._check_dims(
              read,
              read_bp_probs,
              ref)

        self._check_probs(
            read,
            read_bp_probs,
            base_probs,
            ref)

        self._init(read, read_bp_probs, base_probs, ref)

        while self._step() != (len(read) + 1, 1):
            if verbose:
                self._print()
        if verbose:
            self._print()
        score = self._imp.get_min()

        cigar = ''
        alignment = self._imp.get_alignment()
        run = 0
        prev_char = ''
        for a in alignment:
            if a == prev_char:
                run += 1
            else:
                if prev_char != '':
                    cigar += str(run) + chr(prev_char)
                run = 1
                prev_char = a
        cigar += str(run) + chr(prev_char)

        return score, cigar

    def _check_dims(self,
              read,
              read_bp_probs,
              ref):

        cdef size_t read_l = len(read)
        if len(read) != len(read_bp_probs):
            raise ValueError('len(read) != len(read_bp_probs)')
        if read_l == 0:
            raise ValueError('zero len(read)')
        if read_l > self._imp.get_max_read_size():
            raise ValueError('illegal len(read)')

        cdef size_t ref_l = len(ref)
        if ref_l == 0:
            raise ValueError('zero len(ref)')
        if ref_l > self._imp.get_max_ref_size():
            raise ValueError('illegal len(ref)')

    def _check_probs(self,
            read,
            read_bp_probs,
            base_probs,
            ref):
        if not isinstance(base_probs, dict):
            raise ValueError('read_probs must be a dict')
        if set(base_probs.keys()) != set(['A', 'C', 'G', 'T']):
            raise ValueError('Illegal dict for read_probs')

        if not all(0 <= p <= 1 for p in read_bp_probs):
            raise ValueError('read_bp_probs not probabilities')

        prior_vals = base_probs.values()
        if not all(0 <= p <= 1 for p in prior_vals):
            raise ValueError('base_probs not probabilities')
        if any(p == 0 for p in prior_vals):
            raise ValueError('zero base_probs not allowed')
        if sum(prior_vals) != 1:
            raise ValueError('base_probs do not sum to one')

    def __dealloc__(self):
        del self._imp

    def _matchbp(self, i, j):
        cdef size_t i_ = i
        cdef size_t j_ = j
        res = self._imp.match_bps(i_, j_)
        return res

    def _step(self):
        res = self._imp.step()
        return res

    @property
    def _in_read_gap_mat(self):
        return _cpp_mat_to_np_mat(self._imp.get_in_read_gap_mat(), self._imp.get_inf_penalty())

    @property
    def _outside_gap_mat(self):
        return _cpp_mat_to_np_mat(self._imp.get_outside_gap_mat(), self._imp.get_inf_penalty())

    @property
    def _in_ref_gap_mat(self):
        return _cpp_mat_to_np_mat(self._imp.get_in_ref_gap_mat(), self._imp.get_inf_penalty())

    def _init(self,
            read,
            read_bp_probs,
            base_probs,
            ref):

        read_len = len(read)
        max_read = self._imp.get_max_read_size()

        ref_len = len(ref)

        max_ref = self._imp.get_max_ref_size()

        cdef char[:] read_
        read_ = read
        cdef double[:] read_bp_probs_
        read_bp_probs_ = read_bp_probs
        cdef char[:] ref_
        ref_ = ref

        self._base_probs = np.array([base_probs['A'], base_probs['C'], base_probs['G'], base_probs['T']])

        self._imp.init(
            len(read),
            &read_[0],
            &read_bp_probs_[0],
            &self._base_probs[0],
            len(ref),
            &ref_[0])


cdef _cpp_mat_to_np_mat(_mat_t cpp_m, double max_penalty):
    cpp_m.size()
    cpp_m[0].size()
    np_m = np.zeros((cpp_m.size(), cpp_m[0].size()))
    for i in range(cpp_m.size()):
        for j in range(cpp_m[0].size()):
            if cpp_m[i][j] >= max_penalty:
                np_m[i][j] = np.inf
            else:
                np_m[i][j] = cpp_m[i][j]
    return np_m

