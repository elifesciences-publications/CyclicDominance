##########################################################
Explanation for files:
all analysis codes read raw data files in ../data/ and generate output file in ../res/

(1) analysis_K.py
	desciption:		measure all sample and surviving sample averages of population size and # of types over time
	output_file:	../Res/mu1e-05_d*_tmax*.txt
						output: time, avg_pop_size, std_pop_size, sur_sampled_avg_pop_size, sur_sampled_std_pop_size, avg_#_types, std_#_types, sur_sampled_avg_#_types, sur_sampled_std_#_types 
					../Res/nN_mu1e-05_tmax*.txt
						output: baseline_death_rate, avg_pop_size_at_steady_state, avg_#_types_at_steady_state, sur_sampled_pop_size_at_steady_state, sur_sampled_#_types_at_steady_state

(2) analysis_avgpayoff.py
	description:	average of all payoffs in a matrix over time
	output_file: 	../Res/avgp_mu1e-05_d*.txt
						output:	time, avg_all_payoffs, avg_self_payoffs(diagonal), avg_offdiagonal_payoffs, sur_sampled_avg_all_payoffs, sur_sampled_avg_self_payoffs(diagonal), sur_sampled_avg_offdiagonal_payoffs

(3) analysis_links.py
	description:	average link fraction over time and average of them in steady state
	output_file: 	../Res/links_mu1e-05_d*.txt
						output: time, frac_dominance, frac_bistability, frac_coexistence, sur_sampled_frac_dominance, sur_sampled_frac_bistability, sur_sampled_frac_coexistence
					../Res/links_mu1e-05.txt (all fractions are averaged in steady state)
						output: baseline_death_rate, frac_dominance_at_steady_state, frac_bistability, frac_coexistence, sur_sampled_frac_dominance, sur_sampled_frac_bistability, sur_sampled_frac_coexistence

(4) analysis_triad.py
	description:	average link fraction over time and average of them in steady state
	dependency:		triad.txt
	output_file: 	../Res/triad_mu*_d*.txt
						output: triad_idx, its_fraction_at_steady_state

(5) analysis_temporal_changes.py
	description:	sur_sampled_#_types and prob_to_observe_cyc_dom and noncyc_dom in time with its fraction
	dependency:		triad.txt
	output_file: 	../Res/ts_d*_mu*_t*.txt (all values are averaged over sur_samples)
						output: time, sur_sampled_#_type, prob_to_observe_cyc_dom, std_prob_cyc_dom, prob_to_observe_noncyc_dom, std_prob_noncyc_dom, frac_cyc_dom

(6) analysis_triplets_steady.py
	description:	payoffs of cyc_dom and noncyc_don during steady state (t\in[9500:10000])
	dependency:		triad.txt
	output_file: 	../Res/matrix_d*_t*_t*.txt
						output: nine_payoff_elemnets, time_to_birth_, time_to_death, triplet_ID (14: cyc_dom, 15:noncyc_com)

(7) analysis_extract_mean_vector.py
	description:	extracting mean vector of trait to idenfity the characteristics of cyc_dom and noncyc_dom
	output_file: 	../Res/t*_scatter.txt
						output: mean, sdt of three cosine similarities 

(8) analysis_lifespan.py
	description:	making cdf from matrix_d*_t*_t*.txt file (generated from analysis_triplets_steady.py)
	output_file: 	../Res/cdf_t*_t*_t*.txt
						output: lifespan, pdf, ccdf(from 500), lifespan, cdf(from0)

(9) analysis_chi_from_reading.py
	description:	reading data file n Res to read fraction of cyclic dominance in the steady state
	dependency:		need ../Res/ts_d*_mu*_t*.txt files to read data
	output_file: 	../Res/chi_mu1e-05.txt
						output: baseline_death_rate, sur_sampled_#_types, std_#_types, prob_to_cyc_dom, std_prob_cyc_dom, prob_to_noncyc_dom, std_prob_noncyc_dom, frac_cyc_dom, min_frac, max_frac

	



