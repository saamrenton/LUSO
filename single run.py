cropRotation=[1,5,1,5,1,5]

######## basic procedure for reading in parameters,
## evaluating a land use sequence, printing and exporting results

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


lulist=readinLUlist('_LUSdetails_used.csv')
parameters=readinparams('_parameters_used.csv')
optionalparams=readoptionalparams(lulist,'_disallowed_combinations.csv')

print '#############################################################################'
print('these land uses available:')
nlus=len(lulist)
i=1
for lu in lulist:
    print i-1,lu['name']
    i=i+1
    
print '#############################################################################'
print 'evaluating:'
print [lulist[b]['name'] for b in cropRotation]

print '#############################################################################'
##[details1,p1] = profit(cropRotation,parameters,lulist,getDetails='both',optionalparams=optionalparams,annualise=False)
##[details2,p2] = profit(cropRotation,parameters,lulist,getDetails='both',optionalparams=optionalparams,annualise=False)
##detailsToCSV(details1,'singlerun_details1.csv')
##detailsToCSV(details2,'singlerun_details2.csv')

print 'overall profit:',profit(cropRotation,parameters,lulist,getDetails=False,optionalparams=optionalparams,annualise=False)
print 'annualised profit:',profit(cropRotation,parameters,lulist,getDetails=False,optionalparams=optionalparams,annualise=True)


print '#############################################################################'
print 'more information in output files' 
details=profit(cropRotation,parameters,lulist,getDetails=True,optionalparams=optionalparams)
#print(details)
plotDetails(details,stufftoplot=['cost','profit','disease','newseedbank','weedpenalty','newN'],lus=cropRotation,lulist=lulist)
savefig('outputs/singlerun_details.png')
detailsToCSV(details,'singlerun_details.csv')
show()
