######## basic procedure for reading in parameters,
## optimising a lus on a specified sequence of seasons, printing and exporting results 
seasonSeq=[5,9,15,2,16,5,7,19,6,5] ## these start from 1 not 0 as in csv file

##    This file is part of LUSO.
##
##    LUSO is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    LUSO is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with LUSO.  If not, see <http://www.gnu.org/licenses/>.



import sys
sys.path.append('files')
from random import *
from readers import *
from csv import *
from lusofuncs import *


#stochMults=readinstochMults('_stochasticParameters_used.csv')
stochMults=readinstochMults('_stochasticParameters_used.csv')
stochMults
lulist=readinLUlist('_LUSdetails_used.csv')
parameters=readinparams('_parameters_used.csv')
stochMultsUsed=[stochMults[s-1] for s in seasonSeq]
optionalparams=readoptionalparams(lulist)
optionalparams['pricevarlist']=[]   ## set this back to empty, because makes no sense to have price variability for this function...

updateParameter(len(seasonSeq),parameters,lulist,'nyears')

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

b=GA(int(parameters['nyears']),parameters,lulist,optionalparams=optionalparams,stochMultsUsed=stochMultsUsed)
print '#############################################################################'
details=profit(b,parameters,lulist,getDetails=True,optionalparams=optionalparams,stochMultsUsed=stochMultsUsed)
print(details)
plotDetails(details,stufftoplot=['cost','profit','disease','newseedbank','weedpenalty','newN'],lus=b,lulist=lulist)
savefig('outputs/luso_output_details.png')
detailsToCSV(details,'luso_output_details.csv')
plotYields(details,b,lulist,stochMultsUsed)
savefig('outputs/example_yields.png')

print '#############################################################################'
print "finished - the best land use sequence found was"
print [lulist[bx]['name'] for bx in b]

print '#############################################################################'
print('overall profit:'),profit(b,parameters,lulist,getDetails=False,optionalparams=optionalparams,stochMultsUsed=stochMultsUsed)
print('this includes the penalty for final weed seedbank')

print '#############################################################################'
print('more information in output files')
show()
