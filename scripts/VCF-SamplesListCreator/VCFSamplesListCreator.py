from optparse import OptionParser

parser = OptionParser()
parser = OptionParser( description="VCF SampleLists v0.1.kutsukos "
                                   "This tool input is a vcf file. It is creating lists with samples, that have a variation in none, one or both haploids."
                                   "WARNING! Use phased flag if the vcf file is phased, or else there will be no output"
                                   "It can be used as input in some programs like SweeD or OmegaPlus.")

parser.add_option("-v", "--vcf", dest="vcffile",
                  help="vcf file to be used for the analysis", metavar="FILE")
parser.add_option("-P", "--phased", action="store_true", dest="phased", default=False,
                  help="use if vcf file is phased")
parser.add_option("-H", "--header", action="store_true", dest="header", default=False,
                  help="use if you want to export header from the vcf file")

(options, args) = parser.parse_args()
vcfile=options.vcffile
Fphased= options.phased
Fheader=options.header

header=""
headerSplit=""
zerozero="0/0"
oneone="1/1"
zeroone="0/1"
onezero="1|0"

if(Fphased==1):
    zerozero = "0|0"
    oneone = "1|1"
    zeroone = "0|1"

filename=vcfile.split(".vcf")[0]
headerFile = filename +  ".head.out"

file = open(vcfile, "r")
for line in file:
    words = line.split("\t")
    if ("#" not in line):
        lineChr = words[0]
        linePos = words[1]
        outputfile1 = filename + "." + lineChr + "." + linePos + ".11.out"
        outputfile2 = filename + "."+lineChr+"."+linePos+".00.out"
        outputfile3 = filename + "." + lineChr + "." + linePos + ".01.out"
        outputfile4 = filename + "." + lineChr + "." + linePos + ".10.out"
        outFile3 = open(outputfile3, "w")
        outFile2 = open(outputfile2, "w")
        outFile1 = open(outputfile1, "w")
        if(Fphased==1):
            outFile4 = open(outputfile4, "w")
        counter=0
        for word in words:
            if(zerozero in word):
                outFile2.write(headerSplit[counter]+'\n')
            elif(oneone in word):
                outFile1.write(headerSplit[counter]+'\n')
            elif(zeroone in word):
                outFile3.write(headerSplit[counter] + '\n')
            elif (onezero in word):
                outFile4.write(headerSplit[counter] + '\n')
            counter=counter+1;
        outFile1.close()
        outFile2.close()
        outFile3.close()
        if (Fphased == 1):
            outFile4.close()
    else:
        if("##" not in line):
            header=line;
            headerSplit=header.split("\t")
            if(Fheader == 1):
                headout = open(headerFile, "w")
                for item in headerSplit:
                    headout.write(item+'\n')
                headout.close()


file.close()