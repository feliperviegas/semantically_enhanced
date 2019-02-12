# -*- coding: iso-8859-15 -*-
from sklearn.decomposition import NMF, LatentDirichletAllocation
from scipy import sparse
import time
from SToC import *  # Why?????
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sys import argv
from information_gain import InformationGainZheng

#sys.path.append("../Metricas/")
#from metrics import *

#sys.path.append("../Preprocessamento/")
#from preprocessamento import * 
#from IO import *

#import matplotlib.pyplot as plt
#import pickle


class Astoc():
    def __init__(self, n_words=n_words, n_topics, n_final, base_pre, fisher):
        print('Starting ASToC...')
        self.n_words = n_words
        self.n_topics = n_topics
        self.n_final = n_final
        self.base_pre = base_pre
        self.fisher = fisher

    #model => H = terms x topics
    #         W = documents x topics
    def _print_join(self, iterates, model, W, n_topics, features, n_words):
        more = []
        tops = []

        more2 = []

        for i in range(len(iterates)):
            a = iterates[i][1]
            b = iterates[i][2]

            #change? for what?

            if ((a<n_topics)&(b>=n_topics)):
                aux = (model[a] + more[b-n_topics])/2
                #aux = more[b-n_topics]
                aux2 = (W[a] + more2[b-n_topics])/2
    #
            if ((a>=n_topics)&(b<n_topics)):
                aux = (more[a-n_topics] + model[b])/2
                #aux = model[b]
                aux2 = (more2[a-n_topics] + W[b])/2

            if ((a>=n_topics)&(b>=n_topics)):
                #print a
                #print b
                #print len(more)
                aux = (more[a-n_topics] + more[b-n_topics])/2
                #aux = more[b-n_topics]# + more[b-n_topics])/2
                aux2 = (more2[a-n_topics] + more2[b-n_topics])/2
            
            if ((a < n_topics) & (b < n_topics)):
                aux = (model[a] + model[b])/2
                #aux = model[b]
                aux2 = (W[a] + W[b])/2
    
            #print aux
            more.append(aux)
            more2.append(aux2)

        #    words = []
        
        #    sort = sorted(range(len(aux)), key=lambda k: aux[k], reverse=True)
        #    print "(", iterates[i][0],"\t", a,"\t", b, "\t",
        #    for j in range(n_words):
        #        words.append(features[sort[j]])
        #        print features[sort[j]],
        #    print "\t\t", iterates[i][3],")"
        #    tops.append((iterates[i][0], a, b, words, iterates[i][3]))

        #return tops

    def _print_stats(self, t2):
        valores = []
        for (i,j,k,l) in t2:
            valores.append(l)

        ex =  pd.Series(valores)
        print "(Max+min)/2: ", (ex.max() + ex.min())/2 
        print "Media: ", ex.mean()
        print "Max: ", ex.max()
        print "Min: ", ex.min()
        print "Variancia: ", ex.var()
        print "Desvio Padrao: ", ex.std()
        print "Desvio Absoluto: ", ex.mad()
        return ex.mean()


    def _see_join(self, iterates, W, H, threshold, n_final):
        W = W.transpose()
        H = H.transpose()
        W_dict = {}
        H_dict = {}
        for i in range(len(W)):
            W_dict[i] = W[i]
        for i in range(len(H)):
            H_dict[i] = H[i]

        #iterates[i][0] numero do novo topicos
        #iterates[i][1] uniao tópico 1
        #iterates[i][2] uniao topico 2
        #iterates[i][3] valor (threshold)

        #iterates = sorted(iterates, key=lambda x: x[3], reverse=True)

        #print iterates
        #exit()
        n_topics = len(W)
        print iterates
        aux_final = len(W)
        for i in range(len(iterates)):
            new = iterates[i][0]
            a = iterates[i][1]
            b = iterates[i][2]
            valor = iterates[i][3]

            #if valor < threshold:
            #    break

            if aux_final == n_final:
                break

            W_dict[new] = (W_dict[a] + W_dict[b])/2
            del(W_dict[a])
            del(W_dict[b])

            H_dict[new] = (H_dict[a] + H_dict[b])/2
            del(H_dict[a])
            del(H_dict[b])



            aux_final -=1

        W_new = []

        H_new = []

        print W_dict.keys()
        #exit()

        #print sorted(W_dict.keys())

        for i in sorted(W_dict.keys()):
            W_new.append(W_dict[i])

        for i in sorted(H_dict.keys()):
            H_new.append(H_dict[i])

        W_ret = np.zeros((len(W_new),len(W_new[0])))
        H_ret = np.zeros((len(H_new),len(H_new[0])))

        for i in range(len(W_new)):
            for j in range(len(W_new[0])):
                W_ret[i][j] = W_new[i][j]        

        for i in range(len(H_new)):
            for j in range(len(H_new[0])):
                H_ret[i][j] = H_new[i][j]        


        return W_ret, H_ret

    def run(self):
        print "ok3" #????
        
        #usage : python astoc.py fisher basepre ntopics nfinal

        arq = open(self.fisher, "r")
        doc = arq.readlines()
        arq.close()

        for i in range(len(doc)):
            doc[i] = doc[i].strip()

        #print doc[0]

        A = []

        for i in doc:
            aux = []
            text = i.split()
            for j in text:
                aux.append(float(j))
            A.append(aux)

        #for i in A:
        #    if (len(i) != 600):
        #        print i

        csr_A = sparse.csr_matrix(A)

        #csr_A = A

        
        #print csr_A[0]
        #exit()
        print('Applying NMF...')
        nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(csr_A)

        W = nmf.fit_transform(csr_A)
        #np.save("../../W", W)
        #W = np.load("W.npy")
        #print len(W[0])

        print('Creating H...')
        H = nmf.components_.transpose()

        #np.save("../../H", H)
        #H = np.load("H.npy")
        #print len(H[0])
        #exit()

        print('Building irreducible matrix...')
        topXtop_norm = getIrredutibleMatrix(W,H,n_topics)
        #np.save("../../topx", topXtop_norm)
        #topXtop_norm = np.load("topx.npy")

        print('Joing topics')
        assign, t2 = joinTopics(n_topics, topXtop_norm)

        tops = self._print_join(t2, H.transpose(), W, n_topics, None, self.n_words)

        threshold = self._print_stats(t2)
        print('threshold: {}'.format(threshold))
        #print len(H.transpose())
        #print(len(doc))
        #print(len(W.transpose()))
        #exit()
        W_new, H_new = see_join(t2, W, H, threshold, n_final)
        print('Dimension new matrix W: {}'.format(len(W_new)))
        # print len(W_new[0])
        print('Dimension new matrix H: {}'.format(len(H_new)))
        # print len(H_new[0])

        WxHt = np.dot(W , H.transpose()) # Why not use W_new and H_new?
        print(len(WxHt))
        print(len(WxHt[0]))

        with open(base_pre+".WxHt", "w") as arq:
            for i in WxHt:
                for j in i:
                    arq.write(str(j)+" ")
                arq.write("\n")


        with open(base_pre, 'r') as arq:
            docp = map(str.rstrip, arq.readlines())

        count_vec = CountVectorizer(binary=True)
        count = count_vec.fit_transform(docp)
        words = list(map(str, count_vec.get_feature_names()))
        with open(base_pre+".words", "w") as arq:
            for i in words:
                arq.write(i+"\n")        

        new_n_topics = len(W_new)
        
        docXtop = W_new.transpose()

        with open(base_pre+".docxtop", "w") as arq:
            for i in docXtop:
                for j in i:
                    arq.write(str(j)+" ")
                arq.write("\n")

        n_docs = len(docXtop)

        doc_class = []
        new_doc_class = []

        for i in docXtop:
            aux = np.where(i > 0)[0].tolist()
            #doc_class.append(np.where(i == max(i))[0][0])
            new_doc_class.append(aux)
        #print new_doc_class

        #np.save("../../bases_2/new_doc_class", new_doc_class)
        
        #new_doc_class = np.load("../../bases_2/new_doc_class.npy")

        aux = []
        for i in new_doc_class:
            aux+=i

        labels = np.asarray(aux)
        #print labels

        print "Número final de tópicos: ", new_n_topics
        print "Número total de docs: ", n_docs  
        print "Tópico - Quantidade de documentos"
        mean = []
        docs_overlapping = []
        for i in docXtop.transpose():
            docs_overlapping.append(set(np.where(i > 0)[0]))
        for i in range(len(docs_overlapping)):
            print i, "-" , len(docs_overlapping[i])
            mean.append(len(docs_overlapping[i]))

        # print() 
        
        #print n_docs
        #print len(docXtop)
        #print len(docXtop.transpose())

        with open(base_pre+".topicassign", "w") as arq:
            for i in docs_overlapping:
                for j in i:
                    arq.write(str(j)+" ")
                arq.write("\n")

        with open(base_pre+".topicweigths", "w") as arq:
            for i in docXtop:
                for j in i:
                    arq.write(str(j)+" ")
                arq.write("\n")

        print('Average: {}'.format(sum(mean)/new_n_topics))

        over = np.zeros((new_n_topics, new_n_topics))    

        print('Topx Topy Overlapping')
        for i in range(len(docs_overlapping)):
            for j in range(len(docs_overlapping)):
                if i < j:
                    len_docs_i_j = len(docs_overlapping[i].intersection(docs_overlapping[j]))
                    over[i][j] = (float(len_docs_i_j)/float(n_docs))*100
                else:
                    over[i][j] = -1

        for i in range(new_n_topics):
            for j in range(new_n_topics):
                if j < new_n_topics - 1:
                    if over[i][j] == -1:
                        print "-- ;",
                    else:
                        print int(over[i][j]), ";",
                else:
                    if over[i][j] == -1:
                        print "-- "
                    else:
                        print int(over[i][j])


        arq1 = open(base_pre, "r")
        doc1 = arq1.readlines()
        arq1.close()

        pre_processed_document =  map(str.rstrip, doc1)
        
        doc = []
        for d in range(len(new_doc_class)):
            for i in range(len(new_doc_class[d])):
                doc.append(pre_processed_document[d])
        print(len(doc))

        print('Running information gain...')
        ig_zheng = InformationGainZheng()
        info = ig_zheng._infogain(doc, labels, new_n_topics,n_words)

        #f = open('igEver.pckl', 'wb')
        #pickle.dump(ig_zheng, f)
        #f.close()

        #print info

        topics = []
        for i in info:
            topics.append(" ".join(i))

        for i in range(len(topics)):
            print i, topics[i]

        with open(base_pre+".topics","w") as arq:
            for i in topics:
                arq.write(i+"\n")


def execute_astoc():
    n_words=100
    
    if len(argv) == 5:
        fisher = argv[1]
        base_pre = argv[2]
        n_topics = int(argv[3])
        n_final = int(argv[4])
        astoc = Astoc()
        astoc.run(n_words=n_words, fisher=fisher, base_pre=base_pre, n_topics=n_topics, n_final=n_final)
    else:
        print('Error input...')

if __name__ == '__main__':
        execute_astoc()
