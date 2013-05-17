#### read in libraries
from readers import *
from csv import *
from lusofuncs import *

## read in parameter files
lulist=readinLUlist('_LUSdetails_used.csv')
parameters=readinparams('_parameters_used.csv')
ny=5

#####################################################################################
## read in parameter files
lulist=readinLUlist('_LUSdetails_used.csv')
parameters=readinparams('_parameters_used.csv')

from tacticalfunc2D import *
filename='example2D'
paramName1='seedbank0'
fullParamName1='Initial Weed Seedbank'
luname1='general'
valrange1=arange(.0,2.01,0.5)**2
paramName2='weedcompindex'
fullParamName2='Weed Competetiveness'
luname2='general'
valrange2=arange(.0,2.01,0.5)**2

tacticalfunc2D(parameters,lulist,options=[2,5],  ##need to check/change these if land use file is changed
                 paramName1=paramName1,luname1=luname1,valrange1=valrange1,
                 paramName2=paramName2,luname2=luname2,valrange2=valrange2,
                 ny=4,filename=filename,useGA=False)

out=plot2DTactical(parameters,lulist,
               fullParamName1=fullParamName1,
               fullParamName2=fullParamName2,
               filename=filename,saveGraph=True,showGraph=True,iftitle=False)
