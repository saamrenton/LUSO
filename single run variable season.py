######## basic procedure for reading in parameters,
## evaluating a specified land use sequence on a specified sequence of seasons, printing and exporting results 

cropRotation=[1,1,3,1,1,3,1,1,3,1]
seasonSeq=[5,9,15,2,16,5,7,19,6,5]  ## these start from 1 not 0 as in csv file
pureRandomEffects = True  ## include pure random effects on disease (beyond season) ?? if True then you will get a slightly different result each time


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


stochMults=readinstochMults('_stochasticParameters_used.csv')
stochMults
lulist=readinLUlist('_LUSdetails_used.csv')
parameters=readinparams('_parameters_used.csv')
optionalparams=readoptionalparams(lulist)
optionalparams['pricevarlist']=[]   ## set this back to empty, because makes no sense to have price variability for this function...


print '#############################################################################'
print('these land uses available:')
nlus=len(lulist)
i=1
for lu in lulist:
    print i-1,lu['name']
    i=i+1
    
print '#############################################################################'
print('evaluating:')
print [lulist[b]['name'] for b in cropRotation]

print '#############################################################################'
print('on season sequence:')
print [stochMults[e-1]['label'] for e in seasonSeq]

stochMultsUsed=[stochMults[s-1] for s in seasonSeq]
print '#############################################################################'
print('overall profit:'),profit(cropRotation,parameters,lulist,getDetails=False,optionalparams=optionalparams,stochMultsUsed=stochMultsUsed,pureRandomEffects=pureRandomEffects)
print('this includes the penalty for final weed seedbank')

print '#############################################################################'
print('more information in output files')
details=profit(cropRotation,parameters,lulist,getDetails=True,optionalparams=optionalparams,stochMultsUsed=stochMultsUsed,pureRandomEffects=pureRandomEffects)
#print(details)
plotDetails(details,stufftoplot=['cost','profit','disease','newseedbank','weedpenalty','newN'],lus=cropRotation,lulist=lulist)
savefig('outputs/singlerun_varseason_details.png')
detailsToCSV(details,'singlerun_varseason_details.csv')
plotYields(details,cropRotation,lulist,stochMultsUsed)
savefig('outputs/singlerun_varseason_yields.png')
show()
