#ifndef ALLEIN_ZU_HAUS_HPP
#define ALLEIN_ZU_HAUS_HPP


#include <vector>
#include <climits>


class aligner
{
public:
    using penalty_t = double;
    using alignment_t = std::vector<char>;
    using mat_t = std::vector<std::vector<double>>;


public:
    explicit aligner(
        std::size_t max_read_size, 
        std::size_t max_ref_size,
        penalty_t mismatch_penalty, 
        penalty_t open_gap_penalty, 
        penalty_t extend_gap_penalty);

    void init(
        std::size_t read_size,
        const char *const read,
        const double *const read_bp_prob,
        const double *const base_priors,
        std::size_t ref_size,
        const char *const ref);

    std::pair<std::size_t, std::size_t> step();

    double match_bps(std::size_t i, std::size_t j);

    mat_t get_in_read_gap_mat() const;
    mat_t get_outside_gap_mat() const;  
    mat_t get_in_ref_gap_mat() const;

    penalty_t get_inf_penalty() const;

    penalty_t get_min() const;
    alignment_t get_alignment() const;

    inline std::size_t get_max_read_size() const;
    inline std::size_t get_max_ref_size() const;


private:
    struct opt_path
    {
        penalty_t m_in_read_gap;
        penalty_t m_outside_gap;
        penalty_t m_in_ref_gap;
    };

    using opt_path_vec_t = std::vector<opt_path>;
    using opt_path_mat_t = std::vector<opt_path_vec_t>;

    static constexpr penalty_t s_inf_penalty = LLONG_MAX / 2;

private:
    const penalty_t m_mismatch_penalty; 
    const penalty_t m_open_gap_penalty;
    const penalty_t m_extend_gap_penalty;
    const std::size_t m_max_read_s;
    const std::size_t m_max_ref_s;

    opt_path_mat_t m_m;
    std::size_t m_i, m_j;

    std::size_t m_read_size;
    const char *m_read;
    const double *m_read_bp_prob;
    std::size_t m_ref_size;
    const char *m_ref;
    const double *m_base_priors;
};


inline std::size_t aligner::get_max_read_size() const
{
    return m_max_read_s;
}


inline std::size_t aligner::get_max_ref_size() const
{
    return m_max_ref_s;
}


#endif // #ifndef ALLEIN_ZU_HAUS_HPP

