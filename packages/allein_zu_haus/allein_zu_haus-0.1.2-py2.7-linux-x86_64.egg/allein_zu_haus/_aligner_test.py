import unittest

import numpy as np
import six


class _TestInputs(unittest.TestCase):
    def setUp(self):
        import allein_zu_haus

        self._read = np.array(['A', 'C', 'G', 'T', 'A'], dtype=bytes)
        self._read_bp_probs = np.array([1.0] * len(self._read))
        self._ref = np.array(['A', 'C', 'G', 'T', 'A'], dtype=bytes)
        self._base_probs = {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25}
        self._mismatch_p = 7
        self._a = allein_zu_haus.Aligner(5, 5, self._mismatch_p, 10, 1)

    def test_ok(self):
        self._a.match(self._read, self._read_bp_probs, self._base_probs, self._ref)

    def test_probs(self):
        self._read_bp_probs = np.array([1.0] * 4)
        with self.assertRaises(ValueError):
            self._a.match(self._read, self._read_bp_probs, self._base_probs, self._ref)

    def test_empty_read(self):
        with self.assertRaises(ValueError):
            self._a.match(np.array([]), np.array([]), self._base_probs, self._ref)

    def test_empty_ref(self):
        with self.assertRaises(ValueError):
            self._a.match(self._read, self._read_bp_probs, self._base_probs, np.array([]))

    def test_large_read(self):
        with self.assertRaises(ValueError):
            self._a.match(np.array(['A', 'G', 'T', 'T', 'T', 'T'], dtype=bytes), np.array([1] * 6), self._base_probs, self._ref)

    def test_large_ref(self):
        with self.assertRaises(ValueError):
            self._a.match(self._read, self._read_bp_probs, self._base_probs, np.array(['A', 'G', 'T', 'T', 'T', 'T']))

    def test_short_read(self):
        self._a.match(np.array(['A', 'C', 'G', 'T'], dtype=bytes), np.array([1.0] * 4), self._base_probs, self._ref)

    def test_short_ref(self):
        self._a.match(self._read, self._read_bp_probs, self._base_probs, np.array(['A', 'G', 'T', 'T'], dtype=bytes))

    def test_short_ref_read(self):
        self._a.match(
            np.array(['A', 'C', 'G', 'T'], dtype=bytes),
            np.array([1.0] * 4),
            self._base_probs,
            np.array(['A', 'G', 'T', 'T'], dtype=bytes))

    def test_priors_over_one(self):
        base_probs = {'A': 0.25, 'C': 0.3, 'G': 0.4, 'T': 0.25}
        with self.assertRaises(ValueError):
            self._a.match(
                self._read, 
                self._read_bp_probs,
                base_probs,
                self._ref)

    def test_zero_priors(self):
        base_probs = {'A': 0.25, 'C': 0.25, 'G': 0.0, 'T': 0.5}
        with self.assertRaises(ValueError):
            self._a.match(
                self._read,
                self._read_bp_probs,
                base_probs,
                self._ref)

    def test_invalid_read_bp_probs(self):
        with self.assertRaises(ValueError):
            self._a.match(
                self._read,
                np.array([0.25, 0.25, 0.2, 1.2]),
                self._base_probs,
                self._ref)


class _TestPrior(unittest.TestCase):
    def test_uniform_prior_matchbp(self):
        import allein_zu_haus

        mismatch_p = 7
        a = allein_zu_haus.Aligner(5, 5, mismatch_p, 10, 1)

        read = np.array(['A', 'C', 'G', 'T', 'A'], dtype=bytes)
        read_bp_probs = np.array([1.0] * len(read))
        ref = np.array(['A', 'C', 'G', 'T', 'A'], dtype=bytes)
        base_probs = {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25}
        read_prob_series = np.array([1.0, 0.999, 0.99, 0.8, 0.5, 0.2, 0.0])

        m = []
        mm = []
        for p in range(0, 7):
            read_bp_probs = np.array([read_prob_series[p]] * 5)
            a._init(read, read_bp_probs, base_probs, ref)
            mm.append(a._matchbp(1, 2))
            m.append(a._matchbp(1, 1))
        for i in range(0, 6):
            six.print_('index %d, prob %f mm i %f m i %f mm i+1 %f m i+1 %f' % (i, read_prob_series[i], mm[i], m[i], mm[i+1], m[i+1]))
            self.assertGreaterEqual(mm[i], mm[i+1])
            self.assertGreaterEqual(m[i+1], m[i])
        six.print_('index %d, prob %f mm %f m %f' % (6, read_prob_series[6], mm[6], m[6]))
        self.assertEqual(mm[0], mismatch_p)
        self.assertEqual(m[6], mismatch_p)
        self.assertEqual(m[0], 0)

        six.print_('Finished uniform prior match bp test')

    def test_extreme_prior_matchbp(self):
        import allein_zu_haus

        mismatch_p = 7
        a = allein_zu_haus.Aligner(5, 5, mismatch_p, 10, 1)

        read = np.array(['A', 'C', 'G', 'T', 'A'], dtype=bytes)
        read_bp_probs = np.array([1.0] * len(read))
        ref = np.array(['A', 'C', 'G', 'T', 'A'], dtype=bytes)
        base_probs = {'A': 0.03, 'C': 0.91, 'G': 0.03, 'T': 0.03}
        read_prob_series = np.array([1.0, 0.999, 0.99, 0.8, 0.5, 0.2, 0.0])

        m = []
        mm = []
        for p in range(0, 7):
            read_bp_probs = np.array([read_prob_series[p]] * 5)
            a._init(read, read_bp_probs, base_probs, ref)
            mm.append(a._matchbp(2, 1))
            m.append(a._matchbp(1, 1))
        for i in range(0, 6):
            six.print_('index %d, prob %f mm %f m %f' % (i, read_prob_series[i], mm[i], m[i]))
            self.assertGreaterEqual(mm[i], mm[i+1])
            self.assertGreaterEqual(m[i+1], m[i])
        six.print_('index %d, prob %f mm %f m %f' % (6, read_prob_series[6], mm[6], m[6]))
        self.assertEqual(mm[0], mismatch_p)
        self.assertEqual(m[6], mismatch_p)
        self.assertEqual(m[0], 0)

        six.print_('Finished extreme prior match bp test')


class _TestAligner(unittest.TestCase):
    def setUp(self):
        import allein_zu_haus

        self._read = np.array(['A', 'C', 'G', 'T', 'A'], dtype=bytes)
        self._read_bp_probs = np.array([1.0] * len(self._read))
        self._ref = np.array(['A', 'C', 'G', 'T', 'A'], dtype=bytes)
        self._base_probs = {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25}
        self._mismatch_p = 7
        self._a = allein_zu_haus.Aligner(5, 5, self._mismatch_p, 10, 1)

    def test_create(self):
        self._a._init(self._read, self._read_bp_probs, self._base_probs, self._ref)

    def test_perfect_alignment_traceback(self):
        score, cigar = self._a.match(self._read, self._read_bp_probs, self._base_probs, self._ref)
        six.print_('perfect alignemnt score: %f, cigar: %s' % (score, cigar))
        self.assertEqual(score, 0)
        self.assertEqual(cigar, '5M')

    def test_perfect_short_alignments(self):
        score, cigar = self._a.match(
            np.array(['A', 'C', 'G', 'T'], dtype=bytes),
            np.array([1.0] * 4),
            self._base_probs,
            np.array(['A', 'C', 'G', 'T'], dtype=bytes))
        self.assertEqual(score, 0)
        self.assertEqual(cigar, '4M')
        six.print_('short perfect alignment score: %f, cigar %s' % (score, cigar))

    def test_indel_alignments(self):
        score, cigar = self._a.match(
            np.array(['A', 'C', 'G', 'T'], dtype=bytes),
            np.array([1.0] * 4),
            self._base_probs,
            np.array(['A', 'C', 'G', 'T', 'A'], dtype=bytes))
        self.assertEqual(score, 11)
        self.assertEqual(cigar, '4M1D')
        six.print_('short uneven alignment (long ref) score: %f, cigar %s' % (score, cigar))

        score, cigar = self._a.match(
            np.array(['A', 'C', 'G', 'T', 'A'], dtype=bytes),
            np.array([1.0] * 5),
            self._base_probs,
            np.array(['A', 'C', 'G', 'T'], dtype=bytes))
        self.assertEqual(score, 11)
        self.assertEqual(cigar, '4M1I')
        six.print_('short uneven alignment (long read) score: %f, cigar %s' % (score, cigar))

        score, cigar = self._a.match(
            np.array(['A', 'C', 'A', 'G', 'T'], dtype=bytes),
            np.array([1.0] * 5),
            self._base_probs,
            np.array(['A', 'C', 'G', 'T'], dtype=bytes))
        self.assertEqual(score, 11)
        self.assertEqual(cigar, '2M1I2M')
        six.print_('short uneven alignment (long read, middle insertion) score: %f, cigar %s' % (score, cigar))

        score, cigar = self._a.match(
            np.array(['A', 'C', 'G', 'T'], dtype=bytes),
            np.array([1.0] * 4),
            self._base_probs,
            np.array(['A', 'C', 'A', 'G', 'T'], dtype=bytes))
        self.assertEqual(score, 11)
        self.assertEqual(cigar, '2M1D2M')
        six.print_('short perfect uneven alignment (long ref, middle deletion) score: %f, cigar %s' % (score, cigar))

    def test_subs_alignment(self):
        score, cigar = self._a.match(np.array(['A', 'C', 'C', 'T'], dtype=bytes), np.array([1.0] * 4), self._base_probs, np.array(['A', 'C', 'G', 'T'], dtype=bytes))
        self.assertEqual(score, 7)
        self.assertEqual(cigar, '4M')
        six.print_('short substitution alignment score: %f, cigar %s' % (score, cigar))

    def test_combined_sub_indel_alignment(self):
        score, cigar = self._a.match(np.array(['T', 'A', 'C', 'C', 'T'], dtype=bytes), np.array([1.0] * 5), self._base_probs, np.array(['A', 'C', 'G', 'T'], dtype=bytes))
        self.assertEqual(score, 18)
        self.assertEqual(cigar, '1I4M')
        six.print_('combined alignment read %r ref %r score: %f, cigar %s' % (str(np.array(['T', 'A', 'C', 'C', 'T'])),
            str(np.array(['A', 'C', 'G', 'T'])),
            score,
            cigar))

        score, cigar = self._a.match(np.array(['A', 'C', 'G', 'T'], dtype=bytes), np.array([1.0] * 4), self._base_probs, np.array(['T', 'A', 'C', 'C', 'T'], dtype=bytes))
        self.assertEqual(score, 18)
        self.assertEqual(cigar, '1D4M')
        six.print_('combined alignment ref %s read %s score: %f, cigar %s' % (str(np.array(['T', 'A', 'C', 'C', 'T'])),
            str(np.array(['A', 'C', 'G', 'T'])),
            score,
            cigar))

        score, cigar = self._a.match(np.array(['A', 'C', 'G', 'T'], dtype=bytes), np.array([1.0] * 4), self._base_probs, np.array(['A', 'C', 'C', 'T', 'G'], dtype=bytes))
        self.assertEqual(score, 18)
        self.assertEqual(cigar, '4M1D')
        six.print_('combined alignment end gap ref %s read %s score: %f, cigar %s' % (str(np.array(['A', 'C', 'C', 'T', 'G'], dtype=bytes)),
            str(np.array(['A', 'C', 'G', 'T'], dtype=bytes)),
            score,
            cigar))

    def test_no_match(self):
        import allein_zu_haus

        self._mismatch_p = 6
        self._a = allein_zu_haus.Aligner(5, 5, self._mismatch_p, 10, 1)
        score, cigar = self._a.match(np.array(['A', 'A', 'A', 'A'], dtype=bytes), np.array([1.0] * 4), self._base_probs, np.array(['C', 'C', 'C', 'C'], dtype=bytes))
        self.assertEqual(score, 24)
        self.assertEqual(cigar, '4M')
        six.print_('no match alignment ref %s read %s score: %f, cigar %s' % (str(np.array(['A', 'A', 'A', 'A'])),
            str(np.array(['C', 'C', 'C', 'C'], dtype=bytes)),
            score,
            cigar))


if __name__ == '__main__':
    unittest.main()
