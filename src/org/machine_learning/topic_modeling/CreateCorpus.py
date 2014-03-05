'''
Created on Feb 5, 2014

Second step for topic modeling is to the Corpora - a list of document vectors

#Corpora
    A collection of digital documents. This collection is used to automatically infer structure of the documents, their topics etc. 
    For this reason, the collection is also called a training corpus. The inferred latent structure can be later used to assign topics 
    to new documents, which did not appear in the training corpus. No human intervention (such as tagging the documents by hand, or creating other metadata) is required.


#Python
    #Read document vectors from MySql
    #Add document's vectors to GenSim Corpora
    #Save Corpus into disk with Market Matrix Format

#Usage
    python src/org/machine_learning/topic_modeling/CreateCorpus.py Production root  salle20mimis  ./data/dictionary/jobs_en.dict   ./data/corpus/jobs_en.mm &

@author: mimis
'''
import logging
import MySQLdb as mdb
from gensim import corpora,matutils
import peewee
from peewee import *
import sys
import codecs
import time


# utf-8 codec
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# Gensim uses Python's standard logging module to log various stuff at various priority levels; to activate logging (this is optional) 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


'''
####################### INPUT #######################

'''
database_name = str(sys.argv[1])
database_usr = str(sys.argv[2])
database_psw = str(sys.argv[3])
dictionary_file = str(sys.argv[4])
corpus_output_file = str(sys.argv[5])







'''
####################### MAIN #######################
'''
start = time.time()
# peewee mysql wrapper
db = MySQLDatabase(database_name, user=database_usr,passwd=database_psw)
class Job_post(peewee.Model):
#    id = peewee.IntegerField()
    document_vector = peewee.TextField()
    topics = peewee.TextField()

    class Meta:
        database = db


        
# load dictionary 
dictionary = corpora.Dictionary.load(dictionary_file)



# create coprus
class MyCorpus(object):
    def __iter__(self):
        for job in Job_post.select().where( ~(Job_post.document_vector >> None) & (Job_post.topics >> None)  ):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(job.document_vector.encode("utf-8").split(','))
            
            
            
            
            
# doesn't load the corpus into memory!            
corpus = MyCorpus() 
#for vector in corpus: # load one vector into memory at a time
#    print vector
            
            
#print 'old_coprus:',old_corpus
#print 'corpus:',corpus            
            
# save the corpus in the Matrix Market format
corpora.MmCorpus.serialize(corpus_output_file, corpus)




# Close database connection
db.close()        




# Info messages
print dictionary
print "Total Time:", time.time() - start
