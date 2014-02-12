'''
Created on Feb 5, 2014

First step for topic modeling is to create a dictionary with the ids of every feature that exist in our corpus:

#Python
    #Read document vectors from MySql
    #Add document's vectors to GenSim Dictionary
    #Save Dictionary into disk

#Usage
    python src/org/machine_learning/topic_modeling/CreateDictionary.py Production usr psw  /Users/mimis/Development/Amedoo/machine-learning_python/data/dictionary/jobs_en.dict

@author: mimis
'''
import logging
import MySQLdb as mdb
from gensim import corpora, models, similarities
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
### INPUT 

'''
database_name = str(sys.argv[1])
database_usr = str(sys.argv[2])
database_psw = str(sys.argv[3])
dictionary_output_file = str(sys.argv[4])


'''
### MAIN 

'''


# peewee mysql wrapper
db = MySQLDatabase(database_name, user=database_usr,passwd=database_psw)
class Job_post(peewee.Model):
#    id = peewee.IntegerField()
    document_vector = peewee.TextField()
    topics = peewee.TextField()

    class Meta:
        database = db
        
        
        
start = time.time()
# collect statistics about all tokens
dictionary = corpora.Dictionary(job.document_vector.encode("utf-8").split(',') for job in Job_post.select().where( ~(Job_post.document_vector >> None) & (Job_post.topics >> None)  ))


# store the dictionary, for future reference
dictionary.save(dictionary_output_file)

# Info messages
print dictionary
print "\tTotal Time:", time.time() - start


# Close database connection
db.close()        







