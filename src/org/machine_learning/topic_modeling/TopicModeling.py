'''
Created on Feb 5, 2014

Last step for topic modeling is to create the model based on trained corpus and dictionary



#Python
    #Load Dictionary and Corpus
    #Transform Corpus to TF-IDF space
    #LSI transformation of the TF-IDF model
    #Save LSI model into disk for later usage

#Usage
    python src/org/machine_learning/topic_modeling/TopicModeling.py 

@author: mimis
'''
from gensim import corpora, models
import logging
import time

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


'''
####################### INPUT #######################

'''
dictionary_file = '/Users/mimis/Development/Amedoo/machine-learning_python/data/dictionary/jobs_en.dict'
corpus_file = '/Users/mimis/Development/Amedoo/machine-learning_python/data/corpus/jobs_en.mm'
model_output_file = '/Users/mimis/Development/Amedoo/machine-learning_python/data/model/model.lsi'
numper_of_topics = 2







'''
####################### MAIN ####################### 

'''
start = time.time()


# load dictionary and corpus
dictionary = corpora.Dictionary.load(dictionary_file)
corpus = corpora.MmCorpus(corpus_file)
print corpus


# step 1 -- initialize a model
print 'tf-idf transformation'
tfidf = models.TfidfModel(corpus) 


# apply a transformation to a whole corpus
corpus_tfidf = tfidf[corpus]


# initialize an LSI transformation - Here we transformed our Tf-Idf corpus via Latent Semantic Indexing into a latent 2-D space (2-D because we set num_topics=2).
print 'Latent Semantic Indexing'
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=numper_of_topics)

# Classify each document to which topic belongs - create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
corpus_lsi = lsi[corpus_tfidf]  


# what do these two latent dimensions stand for?
lsi.print_topics(numper_of_topics)



#for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
#    print doc



#Model persistency is achieved with the save() and load() functions:
lsi.save(model_output_file) # same for tfidf, lda, ...





print "Total Time:", time.time() - start
