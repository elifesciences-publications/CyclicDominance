#ifndef mutant_h
#define mutant_h
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include"twist.h"
#include <iostream>
#include <sstream>
#include <fstream>
#include <fenv.h>
#include <limits>
#include <vector>
#include <random>
using namespace std;

normal_distribution<double> Gdist(0, 1);
random_device ran;
default_random_engine generator(ran());

//######################### structures ##############################
struct Pop {
	//for the system
	int n; //# of types
	int* x; //abundance vector
	double** P; //P[i][j] means the payoff of i type with an j type opponent
	double** rates; //exp(-w*P[i][j])
	double mu; //mutation rate per capita
	int M; //typical population size
	int ns;//maximum # of types at the same time
	int id;//total number of types including extincted types; id of the first residence is id=0

	//for birth and death rates
	double rd; //death rate
	double rb; //birth rate
	double r; //r=rb-rd

	//for dynamics and parameters
	double tot; //Total number of accessible states
	int choice; //reaction idx which will occur
	long double t; //real time
	int maxt; //unit of mutant (generations); is the same with maximum number of id
	double base_d;
	int intmax;

	//for tree
	int* seq;//species index starts from zero 
	int* mother;

	//for writting
	int fidx;
	vector<long double> tempt;
	vector<int> tempn;
	vector<int> tempN;
	vector< vector<int> > tempx;
	vector<int> vecx;//including type id: x_1 x_2 ... id_1 id_2 ...
	vector< vector<double> > Payoffs;
	vector<double> vecP;
};

//######################### non-core functions ##############################
int Count_row(char* fname)
{
	int N = 0;
	ifstream in(fname);
	string unused;
	string s;
	while ( getline(in, unused) )	{
		if(N==1) { s=unused;	}
		++N;
	}
	return N;
}

//0: Dominance of mutant, 1: Coexistence, 2: Coordination, 3: Dominance of residence
int gametype(Pop &sys)
{
	int game;
	if(sys.P[0][0] < sys.P[1][0])
	{
		if(sys.P[1][1] < sys.P[0][1])
		{
			game = 1;
		}
		else
		{
			game = 0;
		}
	}
	else
	{
		if(sys.P[1][1] < sys.P[0][1])
		{
			game = 3;
		}
		else
		{
			game = 2;
		}
	}
	return game;
}

void showx(Pop &sys) {
  cout << "t=" << sys.t << ": ";
  for (int i=0; i<sys.n; i++) {
    cout << sys.x[i] << " ";
  }
  cout << endl;
}


void showP(Pop &sys) {
  cout << "n=" << sys.n << endl;
  for (int i=0; i<sys.n; i++) {
  	for (int j=0; j<sys.n; j++) {
    cout << sys.P[i][j] << " ";
	}	
	cout << endl;
  }
}


//#######################################################################
//######################### core functions ##############################
//#######################################################################


//######################### initialization ##############################
void init(Pop &sys, int M, double mu, int maxt, int fidx, double base_d) {
	//for Pop
	sys.M = M;
	sys.mu = mu;
	sys.ns = 200;
	sys.x = (int*)calloc(sys.ns, sizeof(int));
	sys.P = (double**)calloc(sys.ns, sizeof(double*));
	sys.rates = (double**)calloc(sys.ns, sizeof(double**));
	for(int i=0; i<sys.ns; i++)
	{
		sys.P[i] = (double*)calloc(sys.ns, sizeof(double));
		sys.rates[i] = (double*)calloc(sys.ns, sizeof(double));
	}
	sys.maxt = maxt;
	sys.t =0;
	sys.rd=0.4;
	sys.rb=0.9;
	sys.r = sys.rb-sys.rd;
	sys.base_d = base_d;

	sys.intmax = numeric_limits<int>::max();

	//for writing 
	sys.fidx = fidx;
	sys.mother = (int*)calloc(maxt+1, sizeof(int));
	sys.seq = (int*)calloc(sys.ns, sizeof(int));
}

void init_conf(Pop &sys) {
	sys.n = 1;
	sys.id = 0;
	sys.t = 0;
	int M = sys.M;
	
	//single individual with a=0
	for(int i=0; i<sys.ns; i++)
	{
		sys.x[i] = 0;
		for(int j=0; j<sys.ns; j++)
		{
			sys.P[i][j] = 0;
			sys.rates[i][j] = 0;
		}
	}
	sys.P[0][0] = Gdist(generator);
	sys.rates[0][0] = (exp(-sys.P[0][0])+sys.base_d)/(double)M;
	sys.x[0] = (int)(sys.r/sys.rates[0][0]);
}

//######################### payoff sampling: mutation process ##############################
int sampling_payoffs(Pop &sys, int mom) {

	//payoff sampling 
	for(int i=0; i<sys.n; i++) {
		sys.P[sys.n][i] = Gdist(generator);
		sys.P[sys.n][i] += sys.P[mom][i];
		sys.P[i][sys.n] = Gdist(generator);
		sys.P[i][sys.n] += sys.P[i][mom];
	}
	sys.P[sys.n][sys.n] = Gdist(generator) + sys.P[mom][mom];
	//sys.P[sys.n][sys.n] = sys.P[mom][mom];

	//cout << sys.id << endl;
	//calculate rates
	for(int i=0; i<sys.n+1; i++) 	{
		for(int j=0; j<sys.n+1; j++) 	{
			sys.rates[i][j] = (exp(-sys.P[i][j])+sys.base_d)/sys.M;
			//cout << i << " " << j << " " << sys.P[i][j] << " " << sys.rates[i][j] << " " << endl;
		}
	}

	return gametype(sys);
}


void record_mut(Pop &sys){
	int N=0;
	//double Pop;
	
	//push {x_i} and {id}
	sys.tempt.push_back(sys.t);
	for(int i=0; i<sys.n; i++) {
		sys.vecx.push_back(sys.x[i]);
		N += sys.x[i];
	}
	for(int i=0; i<sys.n; i++) {
		sys.vecx.push_back(sys.seq[i]);
	}
	sys.tempN.push_back(N);
	sys.tempx.push_back(sys.vecx);
	sys.vecx.erase(sys.vecx.begin(), sys.vecx.end());
	sys.tempn.push_back(sys.n);
	
	//payoffs {p_ij}
	for(int i=0; i<sys.n; i++){
		for(int j=0; j<sys.n; j++) { 
			sys.vecP.push_back(sys.P[i][j]);
		}
	}
	sys.Payoffs.push_back(sys.vecP);
	sys.vecP.erase(sys.vecP.begin(), sys.vecP.end());
}


void mutate(Pop &sys, int mom) {
	//pick the new payoffs
	int game = sampling_payoffs(sys, mom);
	record_mut(sys);
	sys.id++;
	sys.seq[sys.n] = sys.id;
	sys.mother[sys.id] = sys.seq[mom];
	sys.x[sys.n] = 1;
	sys.n++;
}

//######################### extinction ##############################
void extinction(Pop &sys, int die) {
	sys.n -= 1;
	sys.x[die] = sys.x[sys.n];
	sys.seq[die] = sys.seq[sys.n];
	for(int i=0; i<sys.n; i++) {
		if(i==die) {
			sys.P[die][i] = sys.P[sys.n][sys.n];
			sys.rates[die][i] = sys.rates[sys.n][sys.n];
		}
		else {
			sys.P[die][i] = sys.P[sys.n][i];
			sys.P[i][die] = sys.P[i][sys.n];
			sys.rates[die][i] = sys.rates[sys.n][i];
			sys.rates[i][die] = sys.rates[i][sys.n];
		}
	}
	
	//record extinction of whole population event
	if(sys.n==0) {
		sys.tempN.push_back(0);
		sys.tempn.push_back(0);
		sys.vecx.push_back(0);
		sys.vecx.push_back(0);
		sys.tempx.push_back(sys.vecx);
		sys.vecP.push_back(0);
		sys.Payoffs.push_back(sys.vecP);
		sys.vecx.erase(sys.vecx.begin(), sys.vecx.end());
		sys.vecP.erase(sys.vecP.begin(), sys.vecP.end());
		sys.id++;
	}
}

//######################### update: Gillespie algorithm ##############################
void choose_n(Pop &sys) {
	int N = (sys.n+2)*sys.n;
	double* TNAS = (double*)calloc(N, sizeof(double));
	int idx=0;
	double tot=0;

	//make prob array
	//for birth
	for(int i=0; i<sys.n; i++) {
		tot += sys.rb*sys.x[i];
		TNAS[idx++] = tot;
	}

	//for death
	for(int i=0; i<sys.n; i++) {
		tot += sys.rd*sys.x[i];
		TNAS[idx++] = tot;
	}

	//interaction between different type
	for(int i=0; i<sys.n; i++) {
		for(int j=0; j<sys.n; j++) {
			if(i==j) {
				//interaction with the same type
				tot += sys.rates[i][i]*sys.x[i]*(sys.x[i]-1);
				TNAS[idx++] = tot;
			}
			else {
				tot += sys.rates[i][j]*sys.x[i]*sys.x[j];
				TNAS[idx++] = tot;
			}
		}
	}

	//find reaction rule
	int choice=-1;
	double target = drnd()*tot;
	if(target < TNAS[0]) 	{
		choice = 0;
	}
	else {
		for(int i=1; i<idx; i++) {
			if(target < TNAS[i]) {
				choice = i;
				break;
			}
		}
	}
	sys.tot = tot;
	sys.choice = choice;

	if(choice==-1){cout<< "something wring in choice: tot=" << tot << endl; showx(sys); exit(1);}
	free(TNAS);
}

void update(Pop &sys) {
	int i, j;

	//birth: choice \in [0:n-1]
	if(sys.choice < sys.n) {
		if(drnd() < sys.mu)	{
			mutate(sys, sys.choice);
		}
		else {
			sys.x[sys.choice]++;
		}
	}
	//death: choice \in [n:2n-1]
	else if(sys.choice < 2*sys.n) {
		sys.choice -= sys.n; //choice \in [0:n-1]
		sys.x[sys.choice] -= 1;
		if(sys.x[sys.choice] == 0) {
			extinction(sys, sys.choice);
		}
	}
	//death from competition: choice \in [2n:n*n+2n-1]
	else {
		sys.choice -= 2*sys.n; //choice \in [0:n*n-1]
		i = sys.choice%sys.n;
		j = (sys.choice - i)/sys.n;
		//cout << sys.rates[i][j] << endl;

		sys.x[i] -= 1;
		if(sys.x[i] == 0) {
			extinction(sys, i);
		}
	}

	//update t
	sys.t += -log(drnd())/sys.tot;
}

void run(Pop &sys) {
	choose_n(sys);
	update(sys);
}

//######################### writing ##############################
void write_conf(Pop &sys) {
	int n;
	char fname[200];
	FILE *fp;
	sprintf(fname, "data/M%d_mu%g_d%g_maxt%d_%d.d", sys.M, sys.mu, sys.base_d, sys.maxt-1, sys.fidx);

	//write
	ofstream ofp(fname);
	for(int i=0; i<sys.id; i++)
	{
		ofp << i << "\t" << sys.tempt[i]<< "\t" << sys.tempN[i] << "\t" << sys.tempn[i] << "\t";
		
		//print x[i] and P[i][j]
		n = sys.tempn[i];
		if(n==0) {n = 1;}

		for(int l=0; l<2*n; l++) {
			ofp << sys.tempx[i][l] << "\t";
		}
		for(int l=0; l<n*n; l++) {
			ofp << sys.Payoffs[i][l] << "\t";
		}
		ofp << endl;
	}

	//write tree
	sprintf(fname, "data/tree_M%d_mu%g_d%g_maxt%d_%d.d", sys.M, sys.mu, sys.base_d, sys.maxt-1, sys.fidx);
	ofstream tree(fname);
	for(int i=1; i<sys.id; i++)
	{
		tree << i << "\t" << sys.mother[i] << endl;
	}
}

#endif
