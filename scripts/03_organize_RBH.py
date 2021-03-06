#!/usr/local/public/python-2.6.5/bin/python2.6
#/usr/bin/python
## AUTHOR: Eric Fontanillas
## LAST VERSION: 03/09/14 by Julie BAFFARD


def launching (RBH_folder) :
    os.system("bash %s/XXX_pipeline_%s.sh %s" %(RBH_folder,RBH_folder,RBH_folder))


import sys, string, os, itertools, re, zipfile
from multiprocessing import Pool

L2 = [] #list on input file
list_RBH = []
m=1

zfile = zipfile.ZipFile(sys.argv[3])
for name in zfile.namelist() :
	zfile.extract(name)
	L2.append(name)

list_pairwise = itertools.combinations(L2, 2)

for pairwise in list_pairwise :
    print "Pair of species:"
    print pairwise
    DIR1 = pairwise[0]
    DIR2 = pairwise[1]

    S1 = string.split(DIR1, ".")
    S1 = S1[0]
    S1 = string.split(S1, '_')
    shortDIR1 = S1[0]

    S2 = string.split(DIR2, ".")
    S2 = S2[0]
    S2 = string.split(S2, "_")
    shortDIR2 = S2[0]

    RBH_folder = shortDIR1 + "_" + shortDIR2
    list_RBH.append(RBH_folder)

    os.mkdir("./%s" %RBH_folder)

    os.system("cp -fr /w/galaxy/galaxy4kevin/galaxy-dist/tools/julie/oasearch/pairwise/03_run_BLAST_with.K.filter.sh ./%s/" %(RBH_folder))
    os.system("cp -fr /w/galaxy/galaxy4kevin/galaxy-dist/tools/julie/oasearch/pairwise/10_run_BLAST2_with.K.filter.sh ./%s/" %(RBH_folder)) 

    if L2 != [] :
	    os.system("cp -fr %s ./%s/%s" %(DIR1, RBH_folder, DIR1))   
    os.system("cp -fr %s ./%s/%s" %(DIR2, RBH_folder, DIR2))

    pipeline_script = open("./%s/XXX_pipeline_%s.sh" %(RBH_folder,RBH_folder), "w")
    pipeline_patron = open("/w/galaxy/galaxy4kevin/galaxy-dist/tools/julie/oasearch/pairwise/XXX_patronPipeline.sh", "r")

    F1 = pipeline_patron.read()
    F1 = string.replace(F1, "XX1", "./%s/%s" %(RBH_folder,DIR1))
    F1 = string.replace(F1, "XX2", "./%s/%s" %(RBH_folder,DIR2))
    F1 = string.replace(F1, "XX3", DIR1)
    F1 = string.replace(F1, "XX4", DIR2) 
    F1 = string.replace(F1, "XX5", sys.argv[2])
    F1 = string.replace(F1, "WORK_DIR", "%s" %RBH_folder)
    
    pipeline_script.write(F1)

    pipeline_patron.close()
    pipeline_script.close()


## Multithreading
pool = Pool(processes=int(sys.argv[1]))
result = pool.map(launching, list_RBH)
