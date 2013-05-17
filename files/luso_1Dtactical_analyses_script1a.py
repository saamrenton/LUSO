#### read in libraries
from readers import *
from csv import *
from lusofuncs import *
from tacticalfunc import *

## read in parameter files
lulist=readinLUlist('_LUSdetails_used.csv')
parameters=readinparams('_parameters_used.csv')

## run tactical analysis eg.1 
from tacticalfunc import *
tacticalfunc(parameters,lulist,
             options=[2,5],  ##need to check/change these if land use file is changed
             paramName='seedbank0',
             luname='general',
             valrange=arange(.0,1.01,0.1)**2,
             fullParamName='Initial Weed Seedbank',
             outputfilename='tacticalanalysis_lupins_seedbank',
             reset1=False,
             useGA=False,
             showGraph=True,
             iftitle=True)

