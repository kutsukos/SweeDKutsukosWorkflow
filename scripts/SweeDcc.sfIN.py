#!/usr/bin/python
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--input", dest="infile", help="a tab-delimited file with some basic information for the run. For more info, check https://github.com/kutsukos/SweeDKutsukosPipeline", metavar="FILE")
parser.add_option("-t", "--threads", dest="nthreads", help="number of threads to used for this analysis", metavar="NUM")
parser.add_option("-p", "--path", dest="npath", help="path where the sf files are stored", metavar="NUM")
parser.add_option("-l", "--ctrllist", dest="controlList", help="a file containing a list of all grid point files", metavar="NUM")
parser.add_option("-L", "--ctrlpointspath", dest="ctrlpointspath", help="path where the control points are", metavar="NUM")
(options, args) = parser.parse_args()

##
inputfile=options.infile
cmdsfile=inputfile.split(".tab")[0]+".sfIN.cmd"
threads=options.nthreads
sfpath=options.npath
control_pointlist_filepath=options.controlList
control_pointlist_path=options.ctrlpointspath
##

file = open(inputfile, "r")
chr='';pos='';
cmds=[]

file2 = open(control_pointlist_filepath, "r")
controlsPointsPATHS=[];
for line in file2:
    newlineSHIET=line.split("\n")[0]
    controlsPointsPATHS.append(control_pointlist_path.split("/")[0]+"/"+newlineSHIET)
file2.close()

for line in file:
    newlineSHIET=line.split("\n")
    values=newlineSHIET[0].split('\t')
    chr=values[0]
    pos=values[1]
    samples=values[2]
    samplestype=values[2].split(".")[3]

    for gridfile in controlsPointsPATHS:
        control_chr=gridfile.split(".chr")[1].split(".")[0]
        osf=sfpath.split("/")[0]+"/"+"chr"+control_chr+ "."+ chr + "." + pos+ "." + samplestype+".sf"
        runID = "chr" + chr + "." + pos+"." + samplestype+".at."+gridfile.split("ctrl.")[1]+".run"
        cmds.append("sweed/SweeD-P -name "+runID+" -input "+osf + " -gridFile "+gridfile+ " -grid 1312 -threads "+threads)


        
file.close()

file2 = open(cmdsfile, "w")
for item in cmds:
    file2.write(str(item) + "\n")
file2.close()
