##### procedure for analysing tactical decisions 

from random import *
from readers import *
from csv import *
from lusofuncs import *
from numpy import *
from pylab import *

print 'reading in tactcial luso func'

def tacticalfunc(parameters,lulist,options,paramName,luname='general',
                 valrange=arange(.0,2.0,0.1)**2,fullParamName='Parameter',
                 ny=5,outputfilename='tactical_results',useGA=True,reset1=False,
                 showGraph=False,iftitle=True):
    """ run tactical analysis

    options: which land uses are still an option for THIS year, eg. lupins harvested and lupins manured
    paramName: name of parameter to analyse
    luname: name of land use to analyse ('general' means a general parameter, not a land use)
    valrange: range of values to consider
    fullParamName: for output
    """
    normalvalue=getParameter(parameters,lulist,paramName,luname)
    pvals=valrange*normalvalue
    parameters.update([('nyears',ny)])
    starttime=clock()
    parameters2=parameters.copy()
    lulist2=[e.copy() for e in lulist]
    #### open results file and writer
    f=open(outputfilename+'.csv','w')
    thiswriter=writer(f)
    #### prepare and write header row
    headerRow=['option']
    headerRow.append(paramName)
    headerRow.append('best profit')
    for i in range(parameters['nyears']):
        headerRow.append('yr'+str(i))
    thiswriter.writerow(headerRow)
    allpresults=[]
    allbresults=[]
    leglab=[]
    totaltodo=len(options)*len(pvals)
    donesofar=0
    for option in options:  ## lo
        optionpresults=[]
        optionbresults=[]
        for pval in pvals: ##
            nowtime=clock()
            timetaken=nowtime-starttime
            propdone=donesofar/float(totaltodo)
            print pval, propdone*100,"%",
            if donesofar>0: print "about",timetaken/propdone-timetaken,"seconds to go"
            updateParameter(pval,parameters,lulist,paramName,luname)
            if not reset1: updateParameter(pval,parameters2,lulist2,paramName,luname)
            #if reset1: reset=[paramName,luname,normalvalue,pval]
            #if reset1: reset=[parameters2,lulist2]
            #if reset==None: print "??????????????????????????????????????"
            if useGA: b=GAtactical(option,int(parameters['nyears']),parameters,lulist,maxgens=200,
                                   maxstuck=50,popsize=1000,survivalrate=0.4,pointmutationrate=0.05,insertionmutationrate=0.1,
                                   parameters2=parameters2,lulist2=lulist2)
            else:
                b=testalltactical(option,ny,len(lulist),parameters,lulist,suppress=True,parameters2=parameters2,lulist2=lulist2)
            p=profit(b,parameters,lulist,parameters2=parameters2,lulist2=lulist2) #calculate profit of this best LUS
            optionpresults.append(p)
            optionbresults.append(b)
            output=[lulist[option]['name'],pval,p]
            output.extend([lulist[i]['name'] for i in b])
            print output
            thiswriter.writerow(output)
            donesofar=donesofar+1
        allpresults.append(optionpresults)
        allbresults.append(optionbresults)
        leglab.append(lulist[option]['name'])
    f.close() #close the file
    endtime=clock()
    print 'that took',endtime-starttime,'seconds'
    figure()
    plot(pvals,allpresults[0],'o:b',pvals,allpresults[1],'^:r',linewidth=3)
    if len(fullParamName)<12:
        titletext='Value of Options Changing with '+fullParamName
    else:
        titletext='Value Changing with '+fullParamName
    if iftitle: title(titletext,fontsize=18)
    xlabel(fullParamName,fontsize=16)
    ylabel('Profit',fontsize=16)
    legend(leglab,loc=0)
    savefig(outputfilename+'.eps')
    savefig(outputfilename+'.png')
    if showGraph: show()


