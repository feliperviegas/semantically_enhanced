make to compile
./fisherVector -t <dataset> -w <word embedding space> -d <dimensions of word-vectors> -o <output-file>

If you are going to use the Fisher Vector representation in the input of NMF or ASToC, you have to rescale the values because the fihser vector representation generates negative values.