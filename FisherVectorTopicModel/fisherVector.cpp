#include "fisherVector.h"

void stringTokenize(const std::string& str, std::vector<std::string>& tokens,
		const std::string& delimiters = " ") {

	std::string::size_type lastPos = str.find_first_not_of(delimiters, 0);
	std::string::size_type pos = str.find_first_of(delimiters, lastPos);
	while (std::string::npos != pos || std::string::npos != lastPos) {
		tokens.push_back(str.substr(lastPos, pos - lastPos));
		lastPos = str.find_first_not_of(delimiters, pos);
		pos = str.find_first_of(delimiters, lastPos);
	}

}

void stringTokenizeDoc(const std::string& str, map<string, vector<float> > &word2vecDoc, map<string, vector<float> > word2vec,
		const std::string& delimiters = " ") {

	std::string::size_type lastPos = str.find_first_not_of(delimiters, 0);
	std::string::size_type pos = str.find_first_of(delimiters, lastPos);
	string token;
	while (std::string::npos != pos || std::string::npos != lastPos) {
		token = (str.substr(lastPos, pos - lastPos));
		if(word2vec.find(token) != word2vec.end())
			word2vecDoc[token] = word2vec[token];
		lastPos = str.find_first_not_of(delimiters, pos);
		pos = str.find_first_of(delimiters, lastPos);
	}

}

void readWord2Vec(map<string, vector<float> > &word2vec, const char *word2vec_file, int dimension, vector<float> &meanVec, vector<float> &varVec){
	ifstream file(word2vec_file);
	string line;

	if(file){
		while(getline(file, line)){
			std::vector<string> tokens;
			stringTokenize(line, tokens);
			string word = tokens[0];
			vector<float> vecAux = vector<float>(dimension, 0);
			for(int i = 1; i < tokens.size(); i++){
				vecAux[i-1] = atof(tokens[i].c_str());
			}
			word2vec[word] = vector<float>(vecAux.begin(), vecAux.end());
		}
		estimatingGaussianParameters(word2vec, dimension, meanVec, varVec);
	}
	else{
		cerr << "Error while open word2vec file." << endl;
	}
}

void gaussianFV(map<string, vector<float> > wordvec, unsigned int dimension, vector<float> &fisherVector,
		vector<float> meanVec, vector<float> varVec){
	vector<float> meanGradient;
	vector<float> sdGradient;
	int countWord;

	
	// Estimating the first gradient
	countWord =0;
	meanGradient = vector<float>(dimension, 0);
	sdGradient = vector<float>(dimension, 0);
	for(map<string, vector<float> >::iterator it = wordvec.begin(); it != wordvec.end(); ++it){
		vector<float> vecAux = vector<float>(it->second.begin(), it->second.end());
		for(int d = 0; d < vecAux.size(); d++){
			if(varVec[d] != 0.0){
				meanGradient[d] += (vecAux[d] - meanVec[d]) / varVec[d];
				float part1 = ((vecAux[d] - meanVec[d])*(vecAux[d] - meanVec[d]) / (varVec[d]*sqrt(varVec[d])));
				float part2 = (1/sqrt(varVec[d]));
				sdGradient[d] += (part1 - part2);
			}
			else{
				meanGradient[d] += 0.0;
				sdGradient[d] += 0.0;
			}
		}
		countWord +=1;
	}

	vector<float> F_mean = vector<float>(dimension, 0);
	vector<float> F_sd = vector<float>(dimension, 0);
	for(int d = 0; d < F_mean.size(); d++){
		if(varVec[d] != 0.0){
			F_mean[d] = countWord/varVec[d];
			F_sd[d] = (2*countWord)/varVec[d];
			// Não tenho certeza se o calculo abaixo está correto
			meanGradient[d] *= pow(F_mean[d], -0.5);
			sdGradient[d] *= pow(F_sd[d], -0.5);
		}
		else{
			F_mean[d] = 0.0;
			F_sd[d] = 0.0;	
		}	
	} 
		

	fisherVector = vector<float>(meanGradient.begin(), meanGradient.end());
	fisherVector.insert(fisherVector.end(), sdGradient.begin(), sdGradient.end());

}

//REMOVER O ARQUIVO ANTES DE EXECUTAR!!!!!!
void printFisherVector(vector<float> fisherVector, const char* output_fn){
	ofstream outputFile;
    outputFile.open(output_fn, std::ofstream::app);
	// outputFile << "1:" << fisherVector[0];
	outputFile << fisherVector[0];
	for(int d = 1; d < fisherVector.size(); d++){
		outputFile << " " << fisherVector[d];
	}
	outputFile << endl;
	outputFile.close();
}

void readDataWords(map<string, vector<float> > word2vec, const char *data_words_file, int dimension, const char *output_fn, 
		vector<float> meanVec, vector<float> varVec){
	ifstream file(data_words_file);
	string line;
	map<string, vector<float> > word2vecDoc;
	vector<float>fisherVector;
	if(file){
		while(getline(file, line)){
			fisherVector = vector<float>();
			word2vecDoc = map<string, vector<float> >();
			stringTokenizeDoc(line, word2vecDoc, word2vec);
			if(word2vecDoc.size() > 0){
				gaussianFV(word2vecDoc, dimension, fisherVector, meanVec, varVec);	
			}
			else{
				fisherVector = vector<float>(dimension*2, 0.0);
			}
			printFisherVector(fisherVector, output_fn);
		}
	}
	else {
		std::cerr << "Error while open data words file." << std::endl;
		exit(1);
	}
	file.close();
}

void estimatingGaussianParameters(map<string, vector<float> > word2vec, int dimension, vector<float> &meanVec, vector<float> &varVec){
	int countWord =0;
	// Estimating mean
	meanVec = vector<float>(dimension, 0);
	for(map<string, vector<float> >::iterator it = word2vec.begin(); it != word2vec.end(); ++it){
		vector<float> vecAux = vector<float>(it->second.begin(), it->second.end()); 
		for(int d = 0; d < vecAux.size(); d++){
			meanVec[d] += vecAux[d];				
		}
		countWord +=1;
	}
	for(int d = 0; d < meanVec.size(); d++){
		meanVec[d] /= countWord;	
	}
	// Estimating variance
	varVec = vector<float>(dimension, 0);
	for(map<string, vector<float> >::iterator it = word2vec.begin(); it != word2vec.end(); ++it){
		vector<float> vecAux = vector<float>(it->second.begin(), it->second.end());
		for(int d = 0; d < vecAux.size(); d++){
			varVec[d] += (vecAux[d] - meanVec[d])*(vecAux[d] - meanVec[d]);				
		}
	}
	for(int d = 0; d < varVec.size(); d++){
		varVec[d] /= countWord;
	}
}