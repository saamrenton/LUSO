## updated 1 June 2009

import csv
from lusofuncs import convertLUnameToLUI
import os 

### this reads in the .csv file for rotations and
### returns it in a list of dictionaries

def readinLUlist(filename):
    f=open("inputs/"+filename, 'r')
    print 'reading in',filename
    r=csv.DictReader(f)
    luslist=[]
    for row in r:
        for k, v in row.iteritems():
            try:
                row[k]=float(v)
            except ValueError:
                row[k]=v
        if row['hide']!='y':
            luslist.append(row)
    f.close()
    return luslist

### this reads in general global parameters and returns them in a dictionary
def readinparams(filename):
    f=open("inputs/"+filename, 'r')
    print 'reading in',filename
    r=csv.DictReader(f)
    params=r.next()
    for k, v in params.iteritems():
        try:
            params[k]=float(v)
        except ValueError:
            params[k]=v
    return params

### this reads in stochastic multipliers for stochLUSO
def readinstochMults(filename):
    f=open("inputs/"+filename, 'r')
    print 'reading in',filename
    r=csv.DictReader(f)
    stochMults=[]
    for row in r:
        for k, v in row.iteritems():
            if k!='label':
                try:
                    row[k]=float(v)
                except ValueError:
                    row[k]=v
        #if row['hide']!='y':
        stochMults.append(row)
    f.close()
    return stochMults

### this reads in optional params
def readoptionalparams(lulist,disallowedcombosfile='_disallowed_combinations.csv',addefffile='_additional_effects.csv',
                       pricevarfile='_price_variability.csv'):
    optionalparams={}
    if os.path.exists("inputs/"+disallowedcombosfile):
        optionalparams['disallowedcombos']=readDisallowedCombos(lulist,disallowedcombosfile)
    else:
        optionalparams['disallowedcombos']=[]
        print "NO DISALLOWED COMBOS FOUND"
    if os.path.exists("inputs/"+addefffile):
        optionalparams['addefflist']=readinadditionaleffects(lulist,addefffile)
    else:
        optionalparams['addefflist']=[]
        print "NO ADDITIONAL EFFECTS FOUND"
    if os.path.exists("inputs/"+pricevarfile):
        optionalparams['pricevarlist']=readPriceMultipliers(lulist,pricevarfile)
    else:
        optionalparams['pricevarlist']=[]
        print "NO PRICE VARIABILITY FOUND" 
    return optionalparams

### this reads in additional effects (eg 'water effects')
def readinadditionaleffects(lulist,filename):
    namelist=[lu['name'] for lu in lulist]
    f=open("inputs/"+filename, 'r')
    print 'reading in',filename
    r=csv.DictReader(f)
    addefflist=[]
    for row in r:
        for k, v in row.iteritems():
            try:
                row[k]=float(v)
            except ValueError:
                row[k]=v
        print row
        addefflist.append(row)
    f.close()
    for addeff in addefflist:
        if not ((addeff['laterlu'] in namelist) and (addeff['initiallu'] in namelist)):
            print 'warning!!!!!! bad name in additional effects file!!:',addeff['laterlu'],addeff['initiallu'],'....ignoring'
    addefflist = [addeff for addeff in addefflist if ((addeff['laterlu'] in namelist) and (addeff['initiallu'] in namelist))]
    for addeff in addefflist:
        addeff['laterlu']=convertLUnameToLUI(addeff['laterlu'],lulist)
        addeff['initiallu']=convertLUnameToLUI(addeff['initiallu'],lulist)
        addeff['yearsbetween']=int(addeff['yearsbetween'])
    return addefflist
    
### this reads in price multipliers for analysing price variability
def readPriceMultipliers(lulist,filename):
    namelist=[lu['name'] for lu in lulist]
    f=open("inputs/"+filename, 'r')
    print 'reading price multipliers'
    thisline=f.readline()
    alllines=[]
    while thisline!='':
        thisline=f.readline()
        thislinelist=thisline.split(',')
        thislineconv=[]
        if thisline!='':
            #print thisline,thislinelist
            for item in thislinelist:
                if '\n' in item:
                    item=item[0: (len(item)-1) ]
                #print "*",item
                try:
                    additem=float(item)
                except ValueError:
                    if item in namelist:
                        additem=convertLUnameToLUI(item,lulist)
                    elif item=='' or item=='/n':
                        additem = '???'
                    else:
                        print item,
                        for i in range(5): print 'warning!!!!!! bad name in price multipliers file!!:',item
                        additem = '???'
                if additem != '???': thislineconv.append(additem)
            print thislineconv
            alllines.append(thislineconv)
            alllines=[line for line in alllines if  type(line[0])==int]
    f.close()
    pricevarlist=[]
    for i in range(len(namelist)):
        pricevarlist.append([1.])
    for line in alllines:
        lui=line.pop(0)
        mults=line[:]
        pricevarlist[lui]=mults
    return pricevarlist

    
### this reads in disallowed combinations of land uses eg canola cant follow canola
def readDisallowedCombos(lulist,filename):
    namelist=[lu['name'] for lu in lulist]
    f=open("inputs/"+filename, 'r')
    print 'reading disallowed combinations'
    thisline=f.readline()
    alllines=[]
    while thisline!='':
        thisline=f.readline()
        thislinelist=thisline.split(',')
        thislineconv=[]
        if thisline!='':
            #print thisline,thislinelist
            for item in thislinelist:
                if '\n' in item:
                    item=item[0: (len(item)-1) ]
                #print "*",item
                try:
                    additem=int(item)
                except ValueError:
                    if item in namelist:
                        additem=convertLUnameToLUI(item,lulist)
                    elif item=='' or item=='/n':
                        additem = '???'
                    else:
                        print item,
                        for i in range(5): print 'warning!!!!!! bad name in disallowed combinations file!!:',item
                        additem = '???'
                if additem != '???': thislineconv.append(additem)
            print thislineconv
            alllines.append(thislineconv)
    f.close()
    return alllines




### this is the old reader, no longer used
def readinluslistold(filename):
    f=open("inputs/"+filename, 'r')
    print 'reading it in!'
    print 'lets go!'
    thisline=f.readline()
    alllines=[]
    while thisline!='':
        thisline=f.readline()
        thislinelist=thisline.split(',')
        thislineconv=[]
        if thisline!='':
            for item in thislinelist:
                try:
                    additem=float(item)
                except ValueError:
                    additem=item
                thislineconv.append(additem)
            print thislineconv
            alllines.append(thislineconv)
    f.close()
    return alllines

    
