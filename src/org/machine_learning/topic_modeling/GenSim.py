'''
Created on Feb 5, 2014

@author: mimis
'''
import logging
from gensim import corpora, models, similarities

# Gensim uses Python's standard logging module to log various stuff at various priority levels; to activate logging (this is optional) 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)