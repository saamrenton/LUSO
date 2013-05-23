######## this procedure reads in parameters and then evaluates a given land use sequence on a
## large number of randomly chosen season sequences of seasons,
## exporting results to a file called 'multiple runs variable season results.csv'

cropRotation=[1,1,3,1,1,3,1,1,3,1]  ## this is the crop sequence that will be evaluated
nreps = 500  ## the number of season sequences to simulate
seasonsWithReplacement=False


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
import random as rn
from readers import *
from csv import *
from lusofuncs import *


stochMults=readinstochMults('_stochasticParameters_used.csv')
stochMults
nseasontypes = len(stochMults)
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
print('over multiple season sequences')

alldetails=[]
f=open('outputs/multiple runs variable season profits.csv','w')
wr = writer(f,lineterminator='\n')
wr.writerow(['profit'])
prrec=[]
print '#############################################################################'
for rep in range(nreps):
    print '#############################################################################'
    print "rep",rep
    seasonSeq=[]
    if seasonsWithReplacement:
        for i in range(len(cropRotation)):
            seasonSeq.append(rn.choice(range(nseasontypes))+1) ## these start from 1 not 0 as in csv file
    else:
        if len(cropRotation) > nseasontypes:
            print('ERROR, sampling without replacement but not enough season types')
        seasonSeq=rn.sample(range(1,1+nseasontypes),len(cropRotation))
    print('on season sequence:')
    print [stochMults[e-1]['label'] for e in seasonSeq]
    stochMultsUsed=[stochMults[s-1] for s in seasonSeq]
    print '#############################################################################'
    [details,p]=profit(cropRotation,parameters,lulist,getDetails="both",stochMultsUsed=stochMultsUsed,pureRandomEffects=True)
    alldetails.extend(details)
    wr.writerow([p])
    prrec.append(p)


f.close()
detailsToCSV(alldetails,'multiple runs variable season results.csv')
hist(prrec)
xlabel('profit ($)')
title('histogram of profits')
ylabel('frequency')
savefig("outputs/"+'multiple runs variable season profit histogram.png')
print '#############################################################################'
print('DONE: profits penalised for final seedbank are in file called multiple runs variable season profits.csv')
print('more information in output file called multiple runs variable season results.csv')
print('NOTE: the final cumulative profit in this second file does NOT include penalty for final seed bank')




