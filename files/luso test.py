######## basic procedure for reading in parameters,
## optimising a lus, printing and exporting results 

from random import *
from readers import *
from csv import *
from lusofuncs import *


lulist=readinLUlist('GS_LUSdetails_used.csv')
parameters=readinparams('GS_parameters_used.csv')

nlus=len(lulist)
print [lu['name'] for lu in lulist]

print '#############################################################################'
print('these land uses available:')
nlus=len(lulist)
i=1
for lu in lulist:
    print i-1,lu['name']
    i=i+1

#sb0=500
#parameters.update([('seedbank0',sb0)]

#b=testall(int(parameters['nyears']),int(len(lulist)),parameters,lulist)
#b=randsearch(int(parameters['nyears']),1,parameters,lulist)
b=GA(int(parameters['nyears']),parameters,lulist)
print '#############################################################################'
details=profit(b,parameters,lulist,getDetails=True)
print(details)
plotDetails(details,stufftoplot=['cost','profit','disease','newseedbank','weedpenalty','newN'])
savefig('example_details.png')
detailsToCSV(details,'example_solutions.csv')

print '#############################################################################'
print "finished - the best land use sequence found was"
print [lulist[bx]['name'] for bx in b]

print '#############################################################################'
print('overall profit:'),profit(b,parameters,lulist,getDetails=False)

print '#############################################################################'
print('more information in output files')
