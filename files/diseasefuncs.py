from numpy import log, exp
from random import gauss

###### logistic functions
def invlogit(x):
    if x>100.: x=100
    if x< -100: x=-100
    ans = exp(x)/(1+exp(x))
    if ans > 0.9999: return 0.99999
    if ans < 0.00001: return 0.00001
    return ans

def logit(p):
    if p==0: return -99999.
    if p==1: return 99999.
    return log(p/(1-p))

########### disease functions
## these are called by the State class to update disease incidence level
## and then calculate disease Impact
## the functional forms can be changed here, as long as the function inputs are not changed

def updateDiseaseIncidence(olddisease,IncidenceEffectOfPrevCrop,lu,parameters,stochEffects=None,pureRandomEffects=False):
    logitDI = parameters['IEprevinc']  * logit(olddisease) + logit(IncidenceEffectOfPrevCrop) 
    if pureRandomEffects:
        logitDI = logitDI + gauss(0,1)*parameters['IErandom']
    if stochEffects!=None:
        logitDI = logitDI + logit(stochEffects['IEseason']) 
    newdisease=invlogit(logitDI)
    if newdisease<parameters['DImin']: newdisease=parameters['DImin']
    return newdisease




def calculateDiseaseImpact(disease,lu,parameters,stochEffects=None,pureRandomEffects=False):
    logitDD = parameters['DEinc']  * logit(disease) + logit(lu['DEcrop'])
    if pureRandomEffects:
        logitDD = logitDD + gauss(0,1)*parameters['DErandom']
    if stochEffects!=None:
        logitDD = logitDD + logit(stochEffects['DEseason'])
    diseaseImpact = invlogit(logitDD)
    return diseaseImpact
