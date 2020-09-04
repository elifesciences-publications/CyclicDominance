##########################################################
Explanation for files:

(1) singlerun.cpp
	desciption:		generating a signle run of population dynamics
	dependence:		mutant.h, twist.h
	output_file:	data/M*_mu*_d*_maxt*_*.d
						output: time, real_time, population size, # of types, abundances, idx of types, payoffs
					data/tree_M*_mu*_d*_maxt*_*.d
						output: index of mutants, its parantal index
	
(2) mutant.h
	description:	core functions to implment singlerun.cpp
	dependence:		twist.h

(3) twist.h
	description:	random # generating functions
##########################################################
Data Processing:
singlerun -> codes in DataAnalysisCodes -> output files in Res
(1) signlerub: 					obtating raw data by simulating singlerun
(2) codes in DataAnalysisCodes:	analyzing the raw data using python files
(3) output files in Res:		from the python codes output files are generated in Res folder	
