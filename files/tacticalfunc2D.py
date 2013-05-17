##### procedure for analysing tactical desicions 

from random import *
from readers import *
from csv import *
from lusofuncs import *
from numpy import *
from pylab import *
import pickle

def tacticalfunc2D(parameters,lulist,options,
                 paramName1='seedbank0',luname1='general',valrange1=arange(.0,2.0,0.1)**2,reset1=False,
                 paramName2='seedbank0',luname2='general',valrange2=arange(.0,2.0,0.1)**2,reset2=False,
                 ny=4,filename='tactical_results',useGA=False,parameters2=None):
    """ run tactical analysis

    options: which land uses are still an option for THIS year, eg. lupins harvested and lupins manured
    paramName: name of parameter to analyse
    luname: name of land use to analyse ('general' means a general parameter, not a land use)
    valrange: range of values to consider
    ny: number of years to consider beyond current
    outputfilename: obviously :-)
    useGA: if True then faster but not exact
    """
    normalvalue1=getParameter(parameters,lulist,paramName1,luname1)
    pvals1=valrange1*normalvalue1
    #pvals1=array([(float(pvals1e[i])+pvals1e[i+1])/2 for i in range(len(pvals1e)-1)])
    normalvalue2=getParameter(parameters,lulist,paramName2,luname2)
    pvals2=valrange2*normalvalue2
    parameters2=parameters.copy()
    lulist2=[e.copy() for e in lulist]
    #pvals2=array([(float(pvals2e[i])+pvals2e[i+1])/2 for i in range(len(pvals2e)-1)])
    parameters.update([('nyears',ny)])
    starttime=clock()
    #### open results file and writer
    f=open(filename+'tactical2Dresults.csv','w')
    thiswriter=writer(f)
    #### prepare and write header row
    headerRow=['option']
    headerRow.append(paramName1)
    headerRow.append(paramName2)
    headerRow.append('best profit')
    for i in range(parameters['nyears']):
        headerRow.append('yr'+str(i))
    thiswriter.writerow(headerRow)
    #allpresults=[]
    #allbresults=[]
    allresultsarrayp=[]
    optionlist=[]
    resultsarrayp=ones((len(pvals1),len(pvals2)))*-999
    resultsarrayo=ones((len(pvals1),len(pvals2)))*-999
    totaltodo=len(options)*len(pvals1)*len(pvals2)
    totaldone=0
    for option in options:  ## loop thru options
        #optionpresults=[]
        #optionbresults=[]
        ii=0
        resultsarraypthis=ones((len(pvals1),len(pvals2)))*-999
        for pval1 in pvals1:  ## loop thru parameter values
            jj=0
            for pval2 in pvals2:
                print option,pval1,pval2,ii,jj,float(totaldone)/totaltodo*100,"%"
                updateParameter(pval1,parameters,lulist,paramName1,luname1)
                updateParameter(pval2,parameters,lulist,paramName2,luname2)
                if not reset1: updateParameter(pval1,parameters2,lulist2,paramName1,luname1)
                if not reset2: updateParameter(pval2,parameters2,lulist2,paramName2,luname2)
                ## get the best lu for this combo of parameter values
                if useGA:
                    b=GAtactical(option,int(parameters['nyears']),parameters,lulist,maxgens=200,
                                 maxstuck=50,popsize=1000,survivalrate=0.4,pointmutationrate=0.05,
                                 insertionmutationrate=0.1,parameters2=parameters2,lulist2=lulist2)
                else:
                    b=testalltactical(option,ny,len(lulist),parameters,lulist,suppress=True,parameters2=parameters2,lulist2=lulist2)
                p=profit(b,parameters,lulist,parameters2=parameters2,lulist2=lulist2) #calculate profit of this best LUS
                #optionpresults.append(p)
                #optionbresults.append(b)
                output=[lulist[option]['name'],pval1,pval2,p]
                output.extend([lulist[i]['name'] for i in b])
                print "output",output
                thiswriter.writerow(output)
                resultsarraypthis[ii,jj]=p
                if resultsarrayp[ii,jj]<p:
                    resultsarrayp[ii,jj]=p
                    resultsarrayo[ii,jj]=option
                jj=jj+1
                totaldone=totaldone+1
            ii=ii+1
        #allpresults.append(optionpresults)
        #allbresults.append(optionbresults)
        optionlist.append(lulist[option]['name'])
        allresultsarrayp.append(resultsarraypthis)
    f.close() #close the file
    endtime=clock()
    print 'that took',endtime-starttime,'seconds'
    picklefile=open(filename+'_tactical2Dresults.pickled','w')
    pickle.dump([allresultsarrayp,options,pvals1,pvals2,normalvalue1,normalvalue2,optionlist],picklefile)
    picklefile.close()

def plot2DTactical(parameters,lulist,
                 fullParamName1='Parameter1',
                 fullParamName2='Parameter2',
                 filename='tactical_results',saveGraph=True,showGraph=False,iftitle=True):
    """plot the pickled results of tacticalfunc2D"""
    alloutput=calc2Dmats(filename)
    make2Dfigs(alloutput,fullParamName1=fullParamName1,
                 fullParamName2=fullParamName2,
                 filename=filename,saveGraph=saveGraph,showGraph=showGraph,iftitle=iftitle)


def calc2Dmats(filename='tactical_results'):
    print "reading in",filename
    picklefile=open(filename+'_tactical2Dresults.pickled','r')
    [allresultsarrayp,options,pvals1,pvals2,normalvalue1,normalvalue2,optionlist]=pickle.load(picklefile)
    picklefile.close()
    numoptions=len(allresultsarrayp)
    [d1,d2]=shape(allresultsarrayp[0])
    resultsarraydiff01=allresultsarrayp[0]-allresultsarrayp[1]
    resultsarraymargp=ones((d1,d2))*-999
    resultsarraybestoption=ones((d1,d2))*-999
    resultsarraybestp=ones((d1,d2))*-999
    allresultsarraypaa=array(allresultsarrayp)
    for ii in range(d1):
        for jj in range(d2):
            poss=allresultsarraypaa[:,ii,jj]
            best=max(poss)
            bestoption=[i for i in range(len(poss)) if best==poss[i]]
            resultsarraybestoption[ii,jj]=options[bestoption[0]]
            resultsarraybestp[ii,jj]=best
            poss.sort()
            resultsarraymargp[ii,jj]=poss[-1]-poss[-2]
    bestoptiontrimmed=ones((len(pvals1)-1,len(pvals2)-1))*-999
    for ii in range(d1-1):
        for jj in range(d2-1):
            bestoptiontrimmed[ii,jj]=(resultsarraybestoption[ii,jj]+resultsarraybestoption[ii+1,jj]+resultsarraybestoption[ii,jj+1]+resultsarraybestoption[ii+1,jj+1])/4.0
    return [[d1,d2],resultsarraydiff01,resultsarraymargp,resultsarraybestoption,resultsarraybestp,bestoptiontrimmed,allresultsarrayp,options,pvals1,pvals2,normalvalue1,normalvalue2,optionlist]

def make2Dfigs(alloutput,
               fullParamName1='Parameter1',
                 fullParamName2='Parameter2',
                 filename='tactical_results',saveGraph=True,showGraph=False,iftitle=True):
    ############# 
    [[d1,d2],resultsarraydiff01,resultsarraymargp,resultsarraybestoption,resultsarraybestp,bestoptiontrimmed,allresultsarrayp,options,pvals1,pvals2,normalvalue1,normalvalue2,optionlist]=alloutput
    #############
    figure()
    pcolor(pvals1,pvals2,transpose(bestoptiontrimmed),cmap=cm.copper)
    if iftitle: title('Optimal Tactical Decision Changing with\n'+fullParamName1+' and '+fullParamName2,fontsize=16)
    xlabel(fullParamName1,fontsize=16)
    ylabel(fullParamName2,fontsize=16)
    plot([normalvalue1,normalvalue1],[pvals2[0],pvals2[-1]],'g--',lw=3)
    plot([pvals1[0],pvals1[-1]],[normalvalue2,normalvalue2],'g--',lw=3)
    xlim(pvals1[0],pvals1[-1])
    ylim(pvals2[0],pvals2[-1])
    if saveGraph: savefig(filename+'optimaloption2D.eps')
    if saveGraph: savefig(filename+'optimaloption2D.png')
    ############# 
    figure()
    contourf(pvals1,pvals2,transpose(resultsarraybestoption),cmap=cm.copper)
    if iftitle: title('Optimal Tactical Decision Changing with\n'+fullParamName1+' and '+fullParamName2,fontsize=16)
    xlabel(fullParamName1,fontsize=16)
    ylabel(fullParamName2,fontsize=16)
    plot([normalvalue1,normalvalue1],[pvals2[0],pvals2[-1]],'g--',lw=3)
    plot([pvals1[0],pvals1[-1]],[normalvalue2,normalvalue2],'g--',lw=3)
    xlim(pvals1[0],pvals1[-1])
    ylim(pvals2[0],pvals2[-1])
    if saveGraph: savefig(filename+'optimaloption2Dsmooth.eps')
    if saveGraph: savefig(filename+'optimaloption2Dsmooth.png')
    ###############
    figure()
    v=[-10000]
    v.extend(range(0,1405,200))
    v.append(5000)
    v=array(v)
    colmap=cm.hot
    colmap.set_over('white')
    colmap.set_under('black')
    nn=mpl.colors.Normalize(vmin=0,vmax=1400)
    contourf(pvals1,pvals2,transpose(resultsarraybestp),v,norm=nn,cmap=colmap)
    colorbar(format='%d',cmap=colmap,extend='both')
    if iftitle: title('Optimal Profit Changing with Parameters',fontsize=16) ##with\n'+fullParamName1+' and '+fullParamName2)
    contour(pvals1,pvals2,transpose(resultsarraybestp),[0],linewidths=3,colors='green')
    xlabel(fullParamName1,fontsize=16)
    ylabel(fullParamName2,fontsize=16)
    plot([normalvalue1,normalvalue1],[pvals2[0],pvals2[-1]],'g--',lw=3)
    plot([pvals1[0],pvals1[-1]],[normalvalue2,normalvalue2],'g--',lw=3)
    xlim(pvals1[0],pvals1[-1])
    ylim(pvals2[0],pvals2[-1])
    if saveGraph: savefig(filename+'optimalprofit2D.eps')
    if saveGraph: savefig(filename+'optimalprofit2D.png')
    ###############
    figure()
    v=[-10000]
    v.extend(range(-400,405,100))
    v.append(5000)
    v=array(v)
    colmap=cm.jet
    colmap.set_over('darkred')
    colmap.set_under('darkblue')
    nn=mpl.colors.Normalize(vmin=-500,vmax=500)
    contourf(pvals1,pvals2,transpose(resultsarraydiff01),v,norm=nn,cmap=colmap)
    colorbar(format='%d',cmap=colmap,extend='both')
    if iftitle: title('Profit Difference between Options Changing with Parameters',fontsize=16) #\n'+fullParamName1+' and '+fullParamName2)
    contour(pvals1,pvals2,transpose(resultsarraydiff01),[0],linewidths=3,colors='k')
    xlabel(fullParamName1,fontsize=16)
    ylabel(fullParamName2,fontsize=16)
    plot([normalvalue1,normalvalue1],[pvals2[0],pvals2[-1]],'w--',lw=3)
    plot([pvals1[0],pvals1[-1]],[normalvalue2,normalvalue2],'w--',lw=3)
    xlim(pvals1[0],pvals1[-1])
    ylim(pvals2[0],pvals2[-1])
    if saveGraph: savefig(filename+'profitdiff2D.eps')
    if saveGraph: savefig(filename+'profitdiff2D.png')
    ###############
    figure()
    v=[-10000]
    v.extend(range(0,405,50))
    v.append(5000)
    v=array(v)
    colmap=cm.pink
    colmap.set_over('white')
    colmap.set_under('black')
    nn=mpl.colors.Normalize(vmin=0,vmax=500)
    contourf(pvals1,pvals2,transpose(resultsarraymargp),v,norm=nn,cmap=colmap)
    colorbar(format='%d',cmap=colmap,extend='both')
    if iftitle: title('Marginal Profit of Best Option Changing with Parameters',fontsize=16) #\n'+fullParamName1+' and '+fullParamName2)
    xlabel(fullParamName1,fontsize=16)
    ylabel(fullParamName2,fontsize=16)
    plot([normalvalue1,normalvalue1],[pvals2[0],pvals2[-1]],'g--',lw=3)
    plot([pvals1[0],pvals1[-1]],[normalvalue2,normalvalue2],'g--',lw=3)
    xlim(pvals1[0],pvals1[-1])
    ylim(pvals2[0],pvals2[-1])
    if saveGraph: savefig(filename+'margprofit2D.eps')
    if saveGraph: savefig(filename+'margprofit2D.png')
    for i in range(len(allresultsarrayp)):
        figure()
        v=[-10000]
        v.extend(range(0,1405,200))
        v.append(5000)
        v=array(v)
        colmap=cm.hot
        colmap.set_over('white')
        colmap.set_under('black')
        nn=mpl.colors.Normalize(vmin=-0,vmax=1400)
        contourf(pvals1,pvals2,transpose(allresultsarrayp[i]),v,norm=nn,cmap=colmap)
        colorbar(format='%d',cmap=colmap,extend='both')
        if iftitle: title('Profit for Option '+str(i)+' Changing with Parameters',fontsize=16)
        #title('Profit for "'+optionlist[i]+'" Option Changing with Parameters') #\n'+fullParamName1+' and '+fullParamName2)
        xlabel(fullParamName1,fontsize=16)
        ylabel(fullParamName2,fontsize=16)
        plot([normalvalue1,normalvalue1],[pvals2[0],pvals2[-1]],'g--',lw=3)
        plot([pvals1[0],pvals1[-1]],[normalvalue2,normalvalue2],'g--',lw=3)
        xlim(pvals1[0],pvals1[-1])
        ylim(pvals2[0],pvals2[-1])
        if saveGraph: savefig(filename+'opt'+str(i)+'profit2D.eps')
        if saveGraph: savefig(filename+'opt'+str(i)+'profit2D.png')
    if showGraph: show()
    #return [allresultsarrayp,options,pvals1,pvals2,normalvalue1,normalvalue2]






