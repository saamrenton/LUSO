cropRotation=[1,2,3,1,2,3,1,2,3,1]

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
print('overall profit:'),profit(cropRotation,parameters,lulist,getDetails=False)

print '#############################################################################'
print('more information in output files')
details=profit(cropRotation,parameters,lulist,getDetails=True)
#print(details)
plotDetails(details,stufftoplot=['cost','profit','disease','newseedbank','weedpenalty','newN'],lus=cropRotation,lulist=lulist)
savefig('outputs/singlerun_details.png')
detailsToCSV(details,'singlerun_details.csv')
show()
