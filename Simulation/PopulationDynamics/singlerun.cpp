#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include "twist.h"
#include "mutant.h"
using namespace std;


int main(int argc, char** argv)
{
	if(argc!=6)
	{
		printf("Usage: %s M mu maxt(maximum number of mutants) fidx base_d\n", argv[0]);
		exit(1);
	}
	
	int M = atoi(argv[1]);
	double mu = atof(argv[2]);
	int maxt = atoi(argv[3])+1;
	int fidx = atoi(argv[4]);
	double base_d = atof(argv[5]);
	

	//initialize
	Pop sys;
	init(sys, M, mu, maxt, fidx, base_d);
	init_rnd(gus()+M*mu*M+fidx);
	init_conf(sys);

	//run
	while(sys.id<maxt && sys.n!=0)	{
		run(sys);
	}
	write_conf(sys);

	return 0;
}
