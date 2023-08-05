#include <iostream>
#include <string>
#include <algorithm>

#include "align.hpp"


static inline int get_nuc_index(char c)
{
    switch(c)
    {
    case 'A':
        return 0;
    case 'C':
        return 1;
    case 'G':
        return 2;
    case 'T':
        return 3;
    default:
        // Tmp Ami
        return -1;
    }
}


aligner::aligner(
        std::size_t max_read_size, 
        std::size_t max_ref_size,
        penalty_t mismatch_penalty, 
        penalty_t open_gap_penalty, 
        penalty_t extend_gap_penalty) :
    m_mismatch_penalty{mismatch_penalty},
    m_open_gap_penalty{open_gap_penalty},
    m_extend_gap_penalty{extend_gap_penalty},
    m_max_read_s{max_read_size},
    m_max_ref_s{max_ref_size},
    m_m{max_read_size + 1, opt_path_vec_t{max_ref_size + 1}}
{
    // Do nothing.
}


void aligner::init(
    std::size_t read_size,
    const char *const read,
    const double *const read_bp_prob,
    const double *const base_priors,
    std::size_t ref_size,
    const char *const ref)
{
    m_read_size = read_size;
    m_read = read;
    m_read_bp_prob = read_bp_prob;
    m_ref_size = ref_size;
    m_ref = ref;
    m_base_priors = base_priors;

    for(std::size_t i = 0; i < m_m.size(); ++i)
        for(auto &p: m_m[i])
            p.m_in_read_gap = p.m_in_ref_gap = p.m_outside_gap = s_inf_penalty;

    m_m[0][0].m_outside_gap = 0;

    for(std::size_t i = 1; i <= m_read_size; ++i)
    {
       m_m[i][0].m_in_read_gap = m_open_gap_penalty + i * m_extend_gap_penalty;
       m_m[i][0].m_outside_gap = m_m[i][0].m_in_read_gap;
    }
    for(std::size_t j = 1; j <= m_ref_size; ++j) 
    {
       m_m[0][j].m_in_ref_gap = m_open_gap_penalty + j * m_extend_gap_penalty;
       m_m[0][j].m_outside_gap = m_m[0][j].m_in_ref_gap;
    }
    m_i = m_j = 1;

}


double aligner::match_bps(std::size_t i, std::size_t j)
{
    const double p1 = m_read_bp_prob[i];
    const double p2 = (1 - p1) / 3;
    
    const int read_i = get_nuc_index(m_read[i]);
    const int ref_i = get_nuc_index(m_ref[j]);

    double denum = p1 * m_base_priors[read_i];
    for(int k = 0; k < 4; k++) 
        if(k != read_i)
            denum += p2 * m_base_priors[k];

    const double posterior = (m_read[i] != m_ref[j]?
        denum - p2 * m_base_priors[ref_i]:
        denum - p1 * m_base_priors[ref_i]) / denum;
    double penalty = log(posterior*exp(m_mismatch_penalty) + (1 - posterior));

    return std::max(0.0, penalty);
}


aligner::mat_t aligner::get_in_read_gap_mat() const
{
    mat_t read_gap_mat(
        m_read_size + 1,
        std::vector<double>(m_ref_size + 1, s_inf_penalty));
    for(std::size_t i = 0; i <= m_read_size; i++)
        for(std::size_t j = 0; j <= m_ref_size; j++)
            read_gap_mat[i][j] = m_m[i][j].m_in_read_gap;
    return read_gap_mat;
}


aligner::mat_t aligner::get_outside_gap_mat() const
{
    mat_t outside_gap_mat(
        m_read_size + 1,
        std::vector<double>(m_ref_size + 1, s_inf_penalty));
    for(std::size_t i = 0; i <= m_read_size; i++)
        for(std::size_t j = 0; j <= m_ref_size; j++)
            outside_gap_mat[i][j] = m_m[i][j].m_outside_gap;
    return outside_gap_mat;
}


aligner::mat_t aligner::get_in_ref_gap_mat() const
{
    mat_t ref_gap_mat(
        m_read_size + 1,
        std::vector<double>(m_ref_size + 1, s_inf_penalty));
    for(std::size_t i = 0; i <= m_read_size; i++)
        for(std::size_t j = 0; j <= m_ref_size; j++)
            ref_gap_mat[i][j] = m_m[i][j].m_in_ref_gap;
    return ref_gap_mat;
}


aligner::penalty_t aligner::get_inf_penalty() const
{
    return s_inf_penalty;
}


aligner::penalty_t aligner::get_min() const
{
    return std::min({
        m_m[m_read_size][m_ref_size].m_in_read_gap,
        m_m[m_read_size][m_ref_size].m_outside_gap,
        m_m[m_read_size][m_ref_size].m_in_ref_gap});
}


std::pair<std::size_t, std::size_t> aligner::step()
{
    m_m[m_i][m_j].m_in_read_gap = std::min({
        m_m[m_i - 1][m_j].m_in_read_gap + m_extend_gap_penalty,
        m_m[m_i - 1][m_j].m_outside_gap + m_open_gap_penalty + m_extend_gap_penalty});
    m_m[m_i][m_j].m_in_ref_gap = std::min({
        m_m[m_i][m_j - 1].m_in_ref_gap + m_extend_gap_penalty,
        m_m[m_i][m_j - 1].m_outside_gap + m_open_gap_penalty + m_extend_gap_penalty});
    m_m[m_i][m_j].m_outside_gap = std::min({
        m_m[m_i][m_j].m_in_read_gap,
	m_m[m_i - 1][m_j - 1].m_outside_gap + aligner::match_bps(m_i - 1, m_j - 1), 
        m_m[m_i][m_j].m_in_ref_gap});

    if (++m_j == m_ref_size + 1)
    {
        m_j = 1;
        ++m_i;
    }

    return std::make_pair(m_i, m_j);
}

aligner::alignment_t aligner::get_alignment() const
{
    std::size_t i = m_read_size;
    std::size_t j = m_ref_size;
    std::vector<char> traceback;
    char matrix;
    char prev_matrix = 'S';
    double score = aligner::get_min();
    if (m_m[m_read_size][m_ref_size].m_in_read_gap == score)
        matrix = 'I';
    else if (m_m[m_read_size][m_ref_size].m_in_ref_gap == score)
        matrix = 'D';
    else
        matrix = 'M';

    while ((i > 0) || (j > 0))
    {
        if ((matrix != 'M') && (prev_matrix == 'M')) // remove end gap transitions
            traceback.pop_back();
        traceback.push_back(matrix);
        prev_matrix = matrix;
        switch (prev_matrix)
        {
        case 'M':
        {
            if (score == m_m[i][j].m_in_read_gap)
                matrix = 'I';
            else if (score == m_m[i][j].m_in_ref_gap) 
                matrix = 'D';
            else
            {
                matrix = 'M';
                score = m_m[i - 1][j - 1].m_outside_gap;
                i--;
                j--;
            }
            break;
        }
        case 'I':
        {
            if (score == m_m[i - 1][j].m_in_read_gap + m_extend_gap_penalty)
            {
                matrix = 'I';
                score = m_m[i - 1][j].m_in_read_gap;
            }
            else
            {
                matrix = 'M';
                score = m_m[i - 1][j].m_outside_gap;
            }
            i--;
            break;
        }
        case 'D':
        {
            if (score == m_m[i][j - 1].m_in_ref_gap + m_extend_gap_penalty)
            {
                matrix = 'D';
                score = m_m[i][j - 1].m_in_ref_gap;
            }
            else
            {
                matrix = 'M';
                score = m_m[i][j - 1].m_outside_gap;
            }
            j--;
            break;
        }
        }
    }
    std::reverse(traceback.begin(), traceback.end());
    return traceback;
}


