#include "fisherVector.h"
#include <unistd.h>
#include <sys/time.h>
#include <sys/resource.h>

int main(int argc, char** argv) {
    
    char *data_words_file_treino = NULL, *word2vec_file = NULL, *output_fn_treino = NULL;
    int opt, dimension;
    map<string, vector<float> > word2vec;
    vector<float> meanVec;
    vector<float> varVec;
    while ((opt = getopt (argc, argv, "t:w:d:o:")) != -1) {
        switch (opt) {
            case 't': data_words_file_treino = optarg; break;
            case 'w': word2vec_file = optarg; break;
            case 'd': dimension = atoi(optarg); break;
            case 'o': output_fn_treino = optarg; break;
            case '?':
                if (optopt == 't' || optopt == 'w' || optopt == 'd' || optopt == 'o')
                    fprintf (stderr, "Option -%c requires an argument.\n", optopt);
                else if (isprint (optopt))
                    fprintf (stderr, "Unknown option `-%c'.\n", optopt);
                else
                    fprintf (stderr, "Unknown option character `\\x%x'.\n", optopt);
                return 1;
            default:
                std::cerr << "USAGE: " << argv[0] << " -d <val> -t <val>" << std::endl;
                exit(1);
        }
    }
    readWord2Vec(word2vec, word2vec_file, dimension, meanVec, varVec);
    readDataWords(word2vec, data_words_file_treino, dimension, output_fn_treino, meanVec, varVec);
    return 0;
}
