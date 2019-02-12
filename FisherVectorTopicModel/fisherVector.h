#include <cstring>
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <utility>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <math.h>
#include <string>
#include <algorithm>

using namespace std;

void stringTokenize(const std::string& str, std::vector<std::string>& tokens, const std::string& delimiters);

void stringTokenizeDoc(const std::string& str, map<string, vector<float> > &word2vecDoc, map<string, vector<float> > word2vec, const std::string& delimiters);

void readWord2Vec(map<string, vector<float> > &word2vec, const char *word2vec_file, int dimension, vector<float> &meanVec, vector<float> &varVec);

void gaussianFV(map<string, vector<float> > wordvec, unsigned int dimension, vector<float> &fisherVector, vector<float> meanVec, vector<float> varVec);

void printFisherVector(vector<float> fisherVector, const char* output_fn);

void readDataWords(map<string, vector<float> > word2vec, const char *data_words_file, int dimension, const char *output_fn, vector<float> meanVec, vector<float> varVec);

void estimatingGaussianParameters(map<string, vector<float> > word2vec, int dimension, vector<float> &meanVec, vector<float> &varVec);