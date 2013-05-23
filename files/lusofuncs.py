##  update 26 mar 2013  ## to modify input and output paths
##  update 24 feb 2012  ## to include variable season

from random import randint,random,choice,randrange,gauss
from csv import *
from time import clock
from math import exp
from numpy import *
from pylab import *
from diseasefuncs import *

######## generalise parameter setting and getting - should convert to a class one day :-)
def getParameter(parameters,lulist,paramName,luname='general'):
    if luname=='general':
        return parameters.get(paramName)
    else:
        return lulist[convertLUnameToLUI(luname,lulist)][paramName]

def updateParameter(newvalue,parameters,lulist,paramName,luname='general'):
    if luname=='general':
        parameters[paramName]=newvalue
    else:
        lulist[convertLUnameToLUI(luname,lulist)][paramName]=newvalue

###### logistic functions
def invlogit(x):
    return exp(x)/(1+exp(x))

def logit(p):
    if p==0: return -99999.
    if p==1: return 99999.
    return log(p/(1-p))


####state
class State:
    "State of the system"
    seedbank=0
    N=0
    disease=0
    blackleg=0
    discount=1
    previousLU="XXX"
    def __init__(self,parameters):
        self.seedbank=parameters['seedbank0']
        self.N=parameters['N0']
        self.disease=parameters['DI0']
        self.IEprevcrop=0.5
        self.watermult=1.0
    def update(self,lu,parameters,stochEffects=None,pureRandomEffects=False):
        noDisease=False
        noN=False
        nweeds=parameters['weedgermination']*self.seedbank
        nweeds=nweeds*lu['weedsurvival']
        #print lu['name']
        #if lu['name']=='hi wheat' and lu['price']!=350: print "!!!!!!!!!!!!!!!",lu['name'],lu['price'],lu
        #print nweeds
        cropcompfactor=lu['compindex']*lu['sowdensity']
        weedcompfactor=parameters['weedcompindex']*nweeds
        if stochEffects!=None:
            weedcompfactor=weedcompfactor*stochEffects['weedComp']
        #print cropcompfactor
        denom=weedcompfactor+cropcompfactor+1
        #print denom
        ### disease functions
        self.disease = updateDiseaseIncidence(self.disease,self.IEprevcrop,lu,parameters,stochEffects,pureRandomEffects)
        diseaseImpact = calculateDiseaseImpact(self.disease,lu,parameters,stochEffects,pureRandomEffects)
        if noDisease:
            diseaseImpact=0.
        yieldd=lu['yield']*(1-diseaseImpact)*cropcompfactor/denom*parameters['season']
        if lu['name']=='canola' and self.blackleg==1:
            yieldd=yieldd*0.2
        if yieldd<0:
            yieldd=0
        if stochEffects==None: yieldMult=1.0
        else: yieldMult=stochEffects[lu['name']]
        yieldd=yieldd*yieldMult*self.watermult
        income=yieldd*lu['price']
        nreq=lu['Nreq']
        if stochEffects!=None:
            nreq=nreq*stochEffects['NReq']
        if nreq<self.N:
            nreq=0
        else:
            nreq=nreq-self.N
        Ncost=nreq*parameters['Ncost']
        actualCost=lu['cost']
        if self.previousLU==lu['name']:
            actualCost=lu['costCont']
        undiscountedprofit=income-actualCost-Ncost-parameters['fixedcosts']
        profit=self.discount*undiscountedprofit
        self.discount=self.discount*(1-parameters['discountrate'])
        if lu['name']=='canola':
            self.blackleg=1
        else:
            self.blackleg=0
        weedseedset=weedcompfactor/denom*parameters['weedmaxseedset']*lu['weedseedreturn']
        if stochEffects!=None:
            weedseedset=weedseedset*stochEffects['weedSeed']
            self.N=self.N-stochEffects['Nlost']
        self.seedbank=self.seedbank*(1-parameters['weedgermination'])+weedseedset
        if noN:
            self.N=0
        else:
            self.N=lu['NboostperTonne']*yieldd
        self.previousLU=lu['name']
        self.IEprevcrop=lu['IEprevcrop']
        self.watermult=lu['watermult']
        #print lu['name']
        #print self.previousLU
        return dict([('name',lu['name']),
                     ('profit',profit),
                     ('undiscountedprofit',undiscountedprofit),
                     ('yield',yieldd),
                     ('income',income),
                     ('cost',actualCost+parameters['fixedcosts']),
                     ('Ncost',Ncost),
                     ('disease',self.disease),
                     ('diseaseImpact',diseaseImpact),
                     ('newseedbank',self.seedbank),
                     ('weedpenalty',(1-cropcompfactor/(denom))),
                     ('newN',self.N)])


## convert a lu name to a lu index
def convertLUnameToLUI(luname,lulist):
    lui=99
    for lui in range(len(lulist)):
        if lulist[lui]['name']==luname:
            break
    return lui

## convert a lus to a label list string
def convertLUSToString(lus,lulist):
    outstr=""
    for lui in lus:
        outstr=outstr+lulist[lui]['label']+"-"
    return outstr[0:-1]
        

#### as the name says, make a random LUS
def makeARandomLUS(ny,nlu):
    lus=[0]*ny
    for i in range(ny):
        #print "nlu",nlu
        lus[i]=randint(0,nlu)
    return lus

### calculate the profit of a LUS (land use sequence)
def profit(lus,parameters,lulist,getDetails=False,parameters2=None,lulist2=None,stochMultsUsed=None,pureRandomEffects=False):
    if parameters2==None: parameters2=parameters
    if lulist2==None: lulist2=lulist
    p=0
    st=State(parameters)
    details=[]
    yr=0
    #print 'lus',lus
    for lui in lus:
        #print 'lui',lui
        lu=lulist[lui]
        #if yr>0 and lu['name']=='hi wheat' and lu['price']!=350: print "!!!!!!!!!!!!!!!",reset,yr,lu['name'],lu['price'],lui,lulist[lui]['price'],lus,lulist2
        #print lulist
        if stochMultsUsed==None:
            out=st.update(lu,parameters)
        else:
            out=st.update(lu,parameters,stochEffects=stochMultsUsed[yr],pureRandomEffects=pureRandomEffects)
        p=p+out['profit']
        out['cumprofit'] = p
        #print yr
        if stochMultsUsed!=None:
            out['iden'] = stochMultsUsed[yr]['label']
        out['year'] = yr
        if getDetails or getDetails=="both":
            details.append(out)
        parameters=parameters2
        lulist=lulist2
        yr=yr+1
    #if out['newseedbank']>500:
        #p=p-(out['newseedbank']-500)*parameters['costperweedseed']
    p=p-getFinalCostOfSeedbank(out['newseedbank'],parameters)
    #if out['newseedbank']>parameters['seedbank0']:
        #p=p-(out['newseedbank']-parameters['seedbank0'])*parameters['costperweedseed']
    if getDetails=="both":
        return [details,p]
    if getDetails:
        return details
    else:
        return p

def getFinalCostOfSeedbank(seedbank,parameters):
    return seedbank*parameters['costperweedseed']

### extract total profit from details (from function above)
def getProfitfromDetails(details):
    p=0
    for d in details:
        p=p+d['profit']
    p=p-getFinalCostOfSeedbank(out['newseedbank'],parameters)
    return p

##### add the years, cumulative profit and iden to details
def addToDetails(details,iden=999):
    yr=0
    cp=0
    for d in details:
        yr=yr+1
        cp=cp+d['profit']
        d.update([('year',yr),('cumprofit',cp),('iden',iden)])

##### add the years, cumulative profit and iden to details
def addValsToDetails(details,labels=['null'],vals=[999]):
    yr=0
    cp=0
    for d in details:
        yr=yr+1
        cp=cp+d['profit']
        d.update([('year',yr),('cumprofit',cp)])
        for i in range(len(labels)):
            d.update([(labels[i],vals[i])])


######### write details (from function above) to csv file
def detailsToCSV(details,filename):
    namesToWrite=['iden','year','name','undiscountedprofit','profit','cumprofit','income','yield','cost','Ncost','disease','diseaseImpact','weedpenalty','newN','newseedbank']
    headerdict=dict([(e,e) for e in namesToWrite])
    if filename!=None:
        f=open("outputs/"+filename,'w')
        thiswriter=DictWriter(f,fieldnames=namesToWrite,lineterminator = '\n')
        thiswriter.writerow(headerdict)
        for d in details:
            thiswriter.writerow(d)
        f.close()

######## plot details
def plotDetails(details,stufftoplot=['cost','profit','disease','newseedbank','weedpenalty','newN'],lus=None,lulist=None):
    for thing in stufftoplot:
        vals=[yeardetails[thing] for yeardetails in details]
        if thing=='newN':
            vals=[e*10 for e in vals]
        if thing=='weedpenalty' or thing=='disease':
            vals=[e*10 for e in vals]
        plot(vals)
    legend(stufftoplot)
    title('Values Changing Over Land Use Sequence')
    xlabel('time (year)')
    ylabel('value')
    loc,label=xticks()
    if not (lus==None or lulist==None):
        xticks(loc,[lulist[lu]['label'] for lu in lus])


######## plot details
def plotYields(details,lus,lulist,stochMultsUsed):
    figure()
    actualyields=[e['yield'] for e in details]
    baseyields=[lulist[e]['yield'] for e in lus]
    cropnames=[lulist[e]['name'] for e in lus]
    croplabels=[lulist[e]['label'] for e in lus]
    yieldMultsByYear=[stochMultsUsed[i][cropnames[i]] for i in range(len(lus))]
    potentialyields=[aa*bb for (aa,bb) in zip(baseyields,yieldMultsByYear)]
    bar(arange(len(potentialyields))+0.6,potentialyields,fc='r')
    bar(arange(len(actualyields))+0.6,actualyields,fc='g')
    xticks(arange(len(potentialyields))+1.0,[stochMultsUsed[i]['label'] for i in range(len(lus))])
    ylim((0,max(potentialyields)+0.5))
    xlabel('Year')
    ylabel('Yield')
    for i in range(len(lus)):
        text(arange(len(potentialyields))[i]+0.9, potentialyields[i]+0.1, croplabels[i])

########### given a list of lus, write details for each in turn to a csv file, with a unique ident for each lus
def multiLUSDetailsToCSV(luslist,filename,parameters,lulist):
    namesToWrite=['iden','year','name','profit','cumprofit','income','yield','cost','Ncost','disease','weedpenalty','newN','newseedbank']
    headerdict=dict([(e,e) for e in namesToWrite])
    f=open("outputs/"+filename,'w')
    thiswriter=DictWriter(f,fieldnames=namesToWrite)
    thiswriter.writerow(headerdict)
    i=0
    for lus in luslist:
        i=i+1
        details=profit(lus,parameters,lulist,getDetails=True)
        addToDetails(details,iden=i)
        for d in details:
            thiswriter.writerow(d)
    f.close()


#### optimise over all possible LUS by testing all
def testall(ny,nlu,parameters,lulist,stochMultsUsed=None):
    for i in range(5): print "#######################"
    print "testing all"
    starttime=clock()
    bestp=-99999
    bestlus=[]
    maxi=nlu**ny
    i=0
    while i < maxi:
        lus=[]
        ii=i
        for y in range(ny):
            thisbit=ii%nlu
            ii=(ii-thisbit)/nlu
            lus.append(thisbit)
        p=profit(lus,parameters,lulist,stochMultsUsed=stochMultsUsed)
        #print lus,p
        if bestp<p:
            bestp=p
            bestlus=lus[:]
            print 'new best LU'
            print [lulist[i]['name'] for i in lus],
            print bestp
        i=i+1
    endtime=clock()
    print 'that took',endtime-starttime,'seconds'
    return bestlus

#### optimise LUS by testing combinations of main landuses, breaks, break frequencies
def testBreak(ny,nlu,parameters,lulist):
    for i in range(5): print "#######################"
    print "testing break"
    starttime=clock()
    bestp=-99999
    bestlus=[]
    for mainlu in range(nlu):
        for breaklu in range(nlu):
            for freq in range(1,ny):
                lus=[mainlu]*ny
                bys = [i for i in range(ny) if i%freq==0]
                for i in bys:
                    lus[i]=breaklu
                p=profit(lus,parameters,lulist)
                #print lus,p
                if bestp<p:
                    bestp=p
                    bestlus=lus[:]
                    print 'new best LU'
                    print [lulist[i]['name'] for i in lus],
                    print bestp
    endtime=clock()
    print 'that took',endtime-starttime,'seconds'
    return bestlus

#### optimise LUS by testing combinations of main landuses, breaks, break frequencies
def testBreak2(ny,nlu,parameters,lulist,mainlu):
    bestlus=[mainlu]*ny
    for i in range(5): print "#######################"
    print "testing break2"
    starttime=clock()
    bestprofit=profit(bestlus,parameters,lulist)
    cont=True
    loop=0
    while cont:
        loop=loop+1
        print "loop",loop
        print 'new best LU'
        print [lulist[i]['name'] for i in bestlus],
        print bestprofit
        cont=False
        newbestlus=bestlus[:]
        for swap in range(ny-1):
            trylus=bestlus[:]
            a = trylus[swap]
            trylus[swap]=trylus[swap+1]
            trylus[swap+1]=a
            tryprofit=profit(trylus,parameters,lulist)
            if tryprofit>bestprofit:
                bestprofit=tryprofit
                newbestlus=trylus
                cont=True
        for lu in range(nlu):
            for ind in range(ny):
                trylus=bestlus[:]
                trylus.insert(ind,lu)
                trylus.pop()
                tryprofit=profit(trylus,parameters,lulist)
                if tryprofit>bestprofit:
                    bestprofit=tryprofit
                    newbestlus=trylus
                    cont=True
                trylus=bestlus[:]
                trylus[ind]=lu
                tryprofit=profit(trylus,parameters,lulist)
                if tryprofit>bestprofit:
                    bestprofit=tryprofit
                    newbestlus=trylus
                    cont=True
        bestlus=newbestlus[:]
    endtime=clock()
    print 'that took',endtime-starttime,'seconds'
    return bestlus

#### fix first year, then optimise over all possible LUS by testing all
def testalltactical(thisyear,ny,nlu,parameters,lulist,suppress=False,parameters2=None,lulist2=None):
    #print "reset",reset
    starttime=clock()
    bestp=-99999
    bestlus=[]
    maxi=nlu**ny
    i=0
    while i < maxi:
        lus=[thisyear]
        ii=i
        for y in range(ny):
            thisbit=ii%nlu
            ii=(ii-thisbit)/nlu
            lus.append(thisbit)
        p=profit(lus,parameters,lulist,parameters2=parameters2,lulist2=lulist2)
        #print lus,p
        if bestp<p:
            bestp=p
            bestlus=lus[:]
            if not suppress:
                print 'new best LU'
                print [lulist[i]['name'] for i in lus],
        i=i+1
    endtime=clock()
    print 'that took',endtime-starttime,'seconds'
    return bestlus

###### optimise over all possible LUS by testing all, and return best nsols solutions in list
def testallMultiSols(ny,nlu,nsols,parameters,lulist):
    bestluslist=[[-99999,'invalid']]*nsols
    for i in range(nlu**ny):
        lus=[]
        ii=i
        for y in range(ny):
            thisbit=ii%nlu
            ii=(ii-thisbit)/nlu
            lus.append(thisbit)
        p=profit(lus,parameters,lulist)
        if bestluslist[0][0]<p:
            bestluslist.pop(0)
            bestluslist.append([p,lus])
            bestluslist.sort()
            print 'new best LU'
            print [lulist[i]['name'] for i in lus],p
    return bestluslist


####### optimise by making a random search thru the space of possible LUS
####### and record the best found
def randsearch(ny,nsols,parameters,lulist,maxstuck=10000,collectData=False):
    for i in range(5): print "#######################"
    print "random search"
    starttime=clock()
    nlu=len(lulist)
    lus=[0]*ny
    bestp=profit(lus,parameters,lulist)
    bestluslist=[[bestp,lus[:]]]*nsols
    stuck=0
    collectedData=[]
    while stuck<maxstuck:
        stuck=stuck+1
        for i in range(ny):
            lus[i]=randint(0,nlu-1)
        p=profit(lus,parameters,lulist)
        if bestluslist[0][0]<p:
            stuck=0
            bestluslist.pop(0)
            bestluslist.append([p,lus[:]])
            bestluslist.sort()
            print 'new best LU'
            print [lulist[i]['name'] for i in lus],p
            if collectData:
                collectedData.append([p,clock()-starttime])
    endtime=clock()
    print 'that took',endtime-starttime,'seconds'
    if collectData:
        return collectedData
    else:
        return bestluslist

###### optimise by using annealing algorithm (similar to Graeme's I think)
def anneal(lus,nt,parameters,lulist,starttemp=1000,mintemp=0.1,maxstuck=100000):
    for i in range(5): print "#######################"
    print "annealing"
    starttime=clock()
    tdr=pow(starttemp/mintemp,-1.0/nt)
    ctemp=starttemp
    nlu=len(lulist)
    ny=len(lus)
    cp=profit(lus,parameters,lulist)
    bestp=cp
    bestlus=lus
    print 'starting annealing'
    stuck=0
    t=0
    while t < nt:
        ichange=randint(0,ny-1)
        changefrom=lus[ichange]
        changeto=randint(0,nlu-1)
        lus[ichange]=changeto
        newp=profit(lus,parameters,lulist)
        diffavprofit=(newp-cp)/ny
        if exp(diffavprofit/ctemp)<=random():
                lus[ichange]=changefrom
                stuck=stuck+1
                #print 'keep'
        cp=profit(lus,parameters,lulist)
        ctemp=ctemp*tdr
        stuck=stuck+1
        if bestp<newp:
            stuck=0
            bestp=newp
            bestlus=lus[:]
            print 'new best LU'
            print [lulist[i]['name'] for i in lus],newp
        if stuck>maxstuck:
            print 'STUCK!'
            break
    endtime=clock()
    print 'that took',endtime-starttime,'seconds'
    return bestlus

###### optimise by using genetic algorithm
def GA(ny,parameters,lulist,maxgens=100,maxstuck=10,popsize=500,
       survivalrate=0.4,pointmutationrate=0.05,
       insertionmutationrate=0.1,crossType=0,
       collectData=False,startRand=True,stochMultsUsed=None):
    for i in range(5): print "#######################"
    print "GA", crossType
    collectedData=[]
    starttime=clock()
    nlu=len(lulist)
    bestp=-999
    bestlus=[-1]*ny
    nsurvivors=int(popsize*survivalrate)
    print 'starting virtual evolution'
    pop=[]
    stuck=0
    goodstart=[3,1,3]
    if nlu<4: goodstart=[0,1,0] 
    goodstart.extend([1]*(ny-3))
    pop.append(goodstart[:])
    pop.append(goodstart[:])
    if startRand:
        for i in range(popsize-2):
            pop.append(makeARandomLUS(ny,nlu))
    else:
        for i in range(popsize-2):
            pop.append([0]*ny)
    for gen in range(maxgens):
        #print 'gen',gen
        lusp=[]
        for lus in pop:
            lusp.append([profit(lus,parameters,lulist,stochMultsUsed=stochMultsUsed),lus])
        lusp.sort(reverse=True)
        #print "average profit",sum([lusp[i][0] for i in range(popsize)])/popsize
        if lusp[0][0]>bestp:
            stuck=0
            bestp=lusp[0][0]
            bestlus=lusp[0][1]
            print 'new best LU'
            print [lulist[i]['name'] for i in bestlus],bestp
        else:
            stuck=stuck+1
            if stuck>maxstuck:
                print "STUCK! evolution not going anywhere!!!!!!"
                break
        survivors=lusp[0:nsurvivors]
        pop=[s[1] for s in survivors]
        for i in range(popsize-nsurvivors):
            mother=randint(0,nsurvivors-1)
            father=randint(0,nsurvivors-1)
            if crossType==0:
                baby=[choice([survivors[mother][1][i],survivors[father][1][i]]) for i in range(ny)]
                #print baby
            else:
                crossyear=randrange(ny)
                #print "#######",crossyear
                baby=survivors[mother][1][0:crossyear]
                baby.extend(survivors[father][1][crossyear:ny])
                #print survivors[mother][1]
                #print survivors[father][1]
                #print baby, len(baby)
            for j in range(ny):
                if random()<pointmutationrate:
                    baby[j]=randint(0,nlu-1)
            if random()<insertionmutationrate:
                baby.insert(randint(0,ny-1),randint(0,nlu-1))
                baby.pop()
            pop.append(baby)
        if collectData:
            collectedData.append([bestp,clock()-starttime])
    endtime=clock()
    print 'best', [lulist[i]['name'] for i in bestlus],bestp
    print 'that took',endtime-starttime,'seconds'
    if collectData:
        return collectedData
    else:
        return bestlus

def GAtactical(option,ny,parameters,lulist,maxgens=100,
               maxstuck=10,popsize=500,survivalrate=0.4,pointmutationrate=0.05,insertionmutationrate=0.1):
    starttime=clock()
    nlu=len(lulist)
    bestp=-999
    bestlus=[-1]*ny
    nsurvivors=int(popsize*survivalrate)
    print 'starting virtual evolution'
    pop=[]
    stuck=0
    goodstart=[3,1,3]
    goodstart.extend([1]*(ny-3))
    pop.append(goodstart[:])
    pop.append(goodstart[:])
    for lus in pop:
        lus.insert(0,option)
    for i in range(popsize-2):
        pop.append(makeARandomLUS(ny,nlu))
    for gen in range(maxgens):
        #print 'gen',gen
        lusp=[]
        for lus in pop:
            lusp.append([profit(lus,parameters,lulist),lus])
        lusp.sort(reverse=True)
        #print "average profit",sum([lusp[i][0] for i in range(popsize)])/popsize
        if lusp[0][0]>bestp:
            stuck=0
            bestp=lusp[0][0]
            bestlus=lusp[0][1]
            print 'new best LU'
            print [lulist[i]['name'] for i in bestlus],bestp
        else:
            stuck=stuck+1
            if stuck>maxstuck:
                print "STUCK! evolution not going anywhere!!!!!!"
                break
        survivors=lusp[0:nsurvivors]
        pop=[s[1] for s in survivors]
        for i in range(popsize-nsurvivors):
            mother=randint(0,nsurvivors-1)
            father=randint(0,nsurvivors-1)
            baby=[choice([survivors[mother][1][i],survivors[father][1][i]]) for i in range(ny)]
            for j in range(ny):
                if random()<pointmutationrate:
                    baby[i]=randint(0,nlu-1)
            if random()<insertionmutationrate:
                baby.insert(randint(0,ny-1),randint(0,nlu-1))
                baby.pop()
            baby[0]=option
            pop.append(baby)
    endtime=clock()
    print 'best', [lulist[i]['name'] for i in bestlus],bestp
    print 'that took',endtime-starttime,'seconds'
    return bestlus
