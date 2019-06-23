#!/usr/bin/python
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--input", dest="infile", help="a tab-delimited file with some basic information for the run. For more info, check https://github.com/kutsukos/SweeDKutsukosPipeline", metavar="FILE")
parser.add_option("-t", "--threads", dest="nthreads", help="number of threads to used for this analysis", metavar="NUM")
parser.add_option("-v", "--vcflist", dest="vcflist", help="a file that contains a list of filepaths to vcf files for the analysis", metavar="NUM")
(options, args) = parser.parse_args()

## args
threads=options.nthreads
inputfile=options.infile
vcfListFile=options.vcflist
cmdsfile=inputfile.split(".tab")[0]+".cmd"
##


file = open(inputfile, "r")
vcflist = open(vcfListFile, "r")
chr='';pos='';
cmds=[]

vcffiles=[];
for line in vcflist:
    vcffiles.append(line.split("\n")[0]);
vcflist.close();

for line in file:
    newlineSHIET=line.split("\n")
    values=newlineSHIET[0].split('\t')
    chr=values[0]
    pos=values[1]
    samplefile=" "
    if values[2]!=".":
        samplefile=" -sampleList " +values[2]
    samplestype=values[2].split(".")[3]
    for vcfPATH in vcffiles:
        vcfchr=(vcfPATH.split('chr')[1]).split('.')[0]
        runID = " -name chr" + vcfchr + "."+ chr + "." + pos+"."+samplestype+".sfrun"
        osf=" -osf chr" + vcfchr + "."+ chr + "." + pos+"."+samplestype+".sf"
        cmds.append("sweed/SweeD-P" + runID + " -threads " + threads + osf +" -input " + vcfPATH + samplefile)

file.close()
file2 = open(cmdsfile, "w")
for item in cmds:
    file2.write(str(item) + "\n")
file2.close()
