######## basic procedure for reading in parameters,
## optimising a lus, printing and exporting results 

from random import *
from readers import *
from csv import *
from lusofuncs import *


lulist=readinLUlist('_LUSdetails_used.csv')
parameters=readinparams('_parameters_used.csv')

nlu=len(lulist)
print [lu['name'] for lu in lulist]

nsols=10
ny=parameters['nyears']
bestlist=testallMultiSols(ny,nlu,nsols,parameters,lulist)
print bestlist
