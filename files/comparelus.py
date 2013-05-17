##### routine for comparing the profitability of a number of lus as a parameter changes

###### import libraries
from random import *
from readers import *
from csv import *
from lusofuncs import *
from numpy import *
from pylab import *

######## most things you need to change should be in this first block
fullParamName='Initial Weed Seed Bank'  ##for output
paramName='seedbank0'                   ##identify parameter to vary
luname='general'                        ##identify land use to vary ('general' if general parameter)
pvalrange=arange(0,6.0,0.2)**2         ##set range of parameter values to consider (as proportions of default value)
outputfilename='compare_initialseedbank'    
useGA=True                             ##if useGA is True then results will be much faster but only approximate
maxnsols=6                             ##the maximum number of lus's to consider (will probably be less)
###########################

########## another example
#fullParamName='Weed Survival in Canola'
#paramName='weedsurvival'
#luname='canola'
#pvalrange=2**arange(-3,1.0,0.2)
#################

## open parameter files as normal
lulist=readinLUlist('_LUSdetails_used.csv')
parameters=readinparams('_parameters_used.csv')
ny=int(parameters.get('nyears'))
nlu=len(lulist)

#### set range of values to consider
normalvalue=getParameter(parameters,lulist,paramName,luname='general')
pvals=pvalrange*normalvalue

###################### now choose the list of lus's to test and compare - three options but first is probably best
################ comment in/out to change option
### option 1: chose the best lus's over a range of parameter values
testluslist=[]
pvals1=pvals[range(0,len(pvals),int(len(pvals)/maxnsols))]
for pval in pvals1:
    #lulist[4].update([(paramName,pval)])
    parameters.update([(paramName,pval)])
    if useGA:
        b=GA(int(parameters['nyears']),parameters,lulist)
    else:
        b=testall(int(parameters['nyears']),int(len(lulist)),parameters,lulist)
    b=[int(e) for e in b]
    if b not in testluslist:
        testluslist.append(b)
        
#### option 2: find the best lus's for current default parameter values - other options below 
##nsols=9
##bestluslist=testallMultiSols(ny,nlu,nsols,parameters,lulist)
##testluslist=[lus for [p,lus] in bestluslist]
        
### option 3: provide them directly
#testluslist=[[3, 1, 3, 1, 3, 1],[3, 1, 5, 1, 3, 1],[3, 1, 3, 1, 1, 3]]

#### option 4: add an extra one to the lists found above??
##testluslist.append([1,3,1,3,1,3])
#################################################################

###start timer
starttime=clock()

#### open results file and writer
f=open(outputfilename+'.csv','w')
thiswriter=writer(f)
#### prepare and write header row
headerRow=['lus']
headerRow.append(paramName)
headerRow.append('profit')
for i in range(parameters['nyears']):
    headerRow.append('yr'+str(i))
thiswriter.writerow(headerRow)

allpresults=[]
for lusi in range(len(testluslist)):  ## loop thru the lus's by index
    lus=testluslist[lusi]
    print lus
    optionpresults=[]
    for pval in pvals:
        print luname,paramName,pval
        updateParameter(pval,parameters,lulist,paramName,luname)
        p=profit(lus,parameters,lulist) ##calculate profit of this lus at this parameter value
        optionpresults.append(p)  ## collect results for plotting
        output=[lusi,pval,p]  ## collect results for csv output
        output.extend([lulist[i]['name'] for i in lus])
        print output
        thiswriter.writerow(output)
    plot(pvals,optionpresults,':.',label=convertLUSToString(lus,lulist))
    allpresults.append(optionpresults)

f.close() #close the file
endtime=clock()
print 'that took',endtime-starttime,'seconds'

title('Profit for LUSs Changing with '+fullParamName)
xlabel(fullParamName)
ylabel('Profit')
legend(loc=0)
ylim(ymin=-200)
savefig(outputfilename+'.png')
savefig(outputfilename+'.eps')
show()


