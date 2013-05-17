######### procedure for conducting sensitivity analysis on factorial combinations
# of parameter values

from random import *
from readers import *
from csv import *
from lusofuncs import *

## open parameter files as normal
lulist=readinLUlist('_LUSdetails_used.csv')
parameters=readinparams('_parameters_used.csv')

## names of parameters to vary - just for output - also need to specify below when updating
outputNames=['Ncost','pasturediseasemult','canolaprice']

#start timer
starttime=clock()

## open results file and writer
f=open('sensitivity_results.csv','w')
thiswriter=writer(f)
## prepare and write header row
headerRow=outputNames[:]
for i in range(parameters['nyears']):
    headerRow.append('yr'+str(i))
headerRow.append('profit')
thiswriter.writerow(headerRow)
for p1 in [1,2,3,4]:  ## first parameter values to loop thru - Ncost in this example
    for p2 in [-1,0.2,0.5,1]: ## second parameter values to loop thru - pasture disease mult in this example
        for p3 in [200,300,400,500,700]: ## third parameter values to loop thru - canola price in this example
            print outputNames[0],p1,outputNames[1],p2,outputNames[2],p3  ## print the values this loop
            ################# update the parameter  - change these lines if varying different parameter values!
            parameters.update([('Ncost',p1)]) #update Ncost ie make N more or less expensive
            lulist[3].update([('diseasemult',p2)]) # update diseasemult in lu[3] (pasture) ie make pasture more or less effective against disease
            lulist[4].update([('price',p3)]) # update canola price - ie price in lu[4]
            #################################
            print parameters
            print lulist
            #b=testall(parameters['nyears'],len(lulist),parameters,lulist) #find best LUS (land use sequence) with these updated parameter values
            b=GA(int(parameters['nyears']),parameters,lulist)
            p=profit(b,parameters,lulist) #calculate profit of this best LUS
            output=[p1,p2,p3]  ##make output list with the three parameter values
            output.extend([lulist[i]['name'] for i in b]) # add the names of the LUS to the output list
            output.append(p) # add the nprofit to the output list
            print output
            thiswriter.writerow(output)  ## write the output list to the results file

f.close() #close the file
endtime=clock()
print 'that took',endtime-starttime,'seconds'

