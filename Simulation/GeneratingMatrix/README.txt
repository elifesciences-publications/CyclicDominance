Explanation for files:

(1) random_n_chi.py
	desciption:		generating matrices where all elements are randomly drawn from standard normal distribution.
	dependence:		analysis_triad.py, triads.txt
	output: 		matrix_dimension, fraction_of_cyclic_dominance
	output_file:	Random/TriadDist_*.txt (triad_index, frequency_of_triad)
	
(2) sigma_chi.py
	description:	generating matrices that payoffs of the first are sampled from standard normal distribution while variance sigma is used for second mutant that emerges from the first mutant.
	dependence:		analysis_triad.py, triads.txt
	output: 		array(sigma, fraction_of_cyclic_dominance, frequency_of_cyclic_dominance, frequency_of_noncyclic_dominance, probability_to_have_the_same_dominance_direction, probability_to_have_the_opposite_dominance_direction) 

(3) analysis_triad.py
	description:	counting traid types at a given matrix
	dependence:		triads.txt
	main function:	CountTriads(frac, matrix, n)
					input:
						frac: (array) array to add the results
						matrix: (array) payoff matrix
						n: (int) dimension of matrix

(4) triads.txt
	description:	array(triad_type, link_profile)
					there are 64 triads and 16 types of triads
					triad types are from 0 to 15
					index 14 = cyclic dominance 
					index 15 = noncyclic dominance 
					link notation:
					a = counter_clcokwise direction of dominance
					b = clcokwise direction of dominance 
					c = bistability
					d = coexistence
