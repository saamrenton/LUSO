## updated 1 June 2009

import csv

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

    
