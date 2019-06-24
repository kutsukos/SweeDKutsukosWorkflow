#!/usr/bin/python
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-O", "--osfOUT",action="store_true", dest="osfOUTflag", default=False,help="create commands for running SweeD to output osf files")
parser.add_option("-I", "--osfIN",action="store_true", dest="osfINflag", default=False,help="create commands for running SweeD with osf files as input")
parser.add_option("-S", "--SweeD",action="store_true", dest="SweeDflag", default=False,help="create commands for running SweeD with vcf files as input")
#osfOUT options
parser.add_option("-i", "--input", dest="infile", help="a tab-delimited file with some basic information for the run", metavar="FILE")
parser.add_option("-t", "--threads", dest="nthreads", help="number of threads to used for this analysis", metavar="NUM")
parser.add_option("-v", "--vcflist", dest="vcflist", help="a file that contains a list of filepaths to vcf files for the analysis", metavar="NUM")
#osfIN extra options
parser.add_option("-p", "--path", dest="npath", help="the path where the sf files are stored", metavar="NUM")
parser.add_option("-l", "--ctrllist", dest="controlList", help="a file containing a list of all grid point files", metavar="NUM")
parser.add_option("-L", "--ctrlpointspath", dest="ctrlpointspath", help="path where the control points are", metavar="NUM")
#sweed extra options 
parser.add_option("-g", "--grid", dest="ngrid", help="In case there is a grid file used, this option is ignored", metavar="NUM")
(options, args) = parser.parse_args()

## args
OUTflag=options.osfOUTflag
INflag=options.osfINflag
SWEEDflag=options.SweeDflag
## osfOUT
threads=options.nthreads
input_file=options.infile
vcfListFile=options.vcflist
## osfIN extra
sfpath=options.npath
control_pointlist_filepath=options.controlList
control_pointlist_path=options.ctrlpointspath
## SweeD
gridVal=options.ngrid
## end
cmdsfile=""

if(OUTflag+INflag+SWEEDflag==1):	# check that at least and only one flag is used to execute this script
	file = open(input_file, "r")		# Opening the tab-delimited file
	chr='';pos=''; cmds=[]				# A list of the commands that will be created

	if(OUTflag == True):			# Initialization of some lists for some extra info needed to execute SweeD, using OSF files
		file2 = open(vcfListFile, "r"); DB=[];	# A list of the vcf files that are going to be used
		for line in file2:
		    DB.append(line.split("\n")[0]);
		file2.close();
	if(INflag == True):
		file2 = open(control_pointlist_filepath, "r"); DB=[];	# A list of the grifFiles that are going to be used
		for line in file2:
		    newline=line.split("\n")[0]			# Removing the newline symbol from the line
		    DB.append(control_pointlist_path.split("/")[0]+"/"+newline)
		file2.close()
	
	for line in file:				# Starting to read the tab-delimited file
		newline=line.split("\n")	# Removing the newline symbol from the line
		values=newline[0].split('\t')		# An array with all the columns of each line
		chr=values[0]				# An identifier to the chromosome to be scanned
		pos=values[1]				# The position of the insertion
		samplefile=""				# The path to the file containing the samples' list
		gridfile=""					# The path to the file containing the grid points
		grid=" -grid "+gridVal		# Value of grid, in case you dont use gridFile option. See SweeD manual for moar!
		osf=""						# The path to the osf file to be scanned

		if(OUTflag == True):
			cmdsfile=input_file.split(".tab")[0]+".sfOUT.cmd"	# defining the output file name
			grid=""												# there is no grid in this case
			samplefile=" -sampleList " +values[2]
			samplestype=values[2].split(".")[3]					# how the samples are genotyped, defines the type
			for vcfPATH in DB:
				vcfchr=(vcfPATH.split('chr')[1]).split('.')[0]
				runID = " -name chr" + vcfchr + "."+ chr + "." + pos+"."+samplestype+".sfrun"
				osf=" -osf chr" + vcfchr + "."+ chr + "." + pos+"."+samplestype+".sf"
				inpuT=" -input "+vcfPATH
				cmds.append("sweed/SweeD-P -threads " + threads + runID + osf + inpuT + gridfile + grid + samplefile)

		if(INflag == True):
			cmdsfile=input_file.split(".tab")[0]+".sfIN.cmd"		# defining the output file name
			samplestype=values[2].split(".")[3]					# how the samples are genotyped, defines the type
			for grid_file in DB:
				control_chr=grid_file.split(".chr")[1].split(".")[0]
				osF=sfpath.split("/")[0]+"/"+"chr"+control_chr+ "."+ chr + "." + pos+ "." + samplestype+".sf"
				inpuT=" -input "+osF
				runID = " -name chr" + chr + "." + pos+"." + samplestype+".at."+grid_file.split("ctrl.")[1]+".run"
				gridfile=" -gridFile "+grid_file
				cmds.append("sweed/SweeD-P -threads " + threads + runID + osf + inpuT + gridfile + grid + samplefile)	

		if(SWEEDflag == True):
			cmdsfile=input_file.split(".tab")[0]+".SweeD.cmd"	# defining the output file name
			vcffile=values[2];
			if values[3]!='.' :
				gridfile=" -gridFile " +values[3]
			if values[4]!='.' :
				samplefile=" -sampleList " +values[4]
			samplestype=values[4].split(".")[3]					# how the samples are genotyped, defines the type
			inpuT=" -input "+vcffile
			runID = " -name chr" + chr + "." + pos+"."+samplestype+".run"
			cmds.append( "sweed/SweeD-P -threads " + threads + runID + osf + inpuT + gridfile + grid + samplefile)

	file.close()
	file2 = open(cmdsfile, "w")		# time to write the commands in a file
	for item in cmds:
		file2.write(str(item) + "\n")
	file2.close()
else:
	print("Error! Try again")