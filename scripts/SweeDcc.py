#!/usr/bin/python
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--input", dest="infile", help="a tab-delimited file with some basic information for the run. For more info, check https://github.com/kutsukos/SweeDKutsukosPipeline", metavar="FILE")
parser.add_option("-t", "--threads", dest="nthreads", help="Number of threads to used for this analysis", metavar="NUM")
parser.add_option("-g", "--grid", dest="ngrid", help="In case there is a grid file used, this option is ignored", metavar="NUM")
(options, args) = parser.parse_args()


## args and products
inputfile=options.infile
threads=options.nthreads
grid=options.ngrid
cmdsfile=inputfile.split(".tab")[0]+".SweeD.cmd"
##

file = open(inputfile, "r")
chr='';pos='';
cmds=[]

for line in file:
    newlineSHIET=line.split("\n")
    values=newlineSHIET[0].split('\t')
    chr=values[0]
    pos=values[1]
    vcffile=values[2];
    gridfile=""
    samplefile=""
    if values[3]!='.' :
        gridfile=" -gridFile " +values[3]
	grid=str(1312420)
    if values[4]!='.' :
	samplefile=" -sampleList " +values[4]
	samplestype=values[4].split(".")[3]
        
    #RUNnames and append command
    runID = "chr" + chr + "." + pos+"."+samplestype+".run"
    cmds.append( "sweed/SweeD-P -threads "+threads+" -name " + runID + " -input " + vcffile + gridfile + " -grid " + grid + samplefile)

file.close()

file2 = open(cmdsfile, "w")
for item in cmds:
    file2.write(str(item) + "\n")
file2.close()
