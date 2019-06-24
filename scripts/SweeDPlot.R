rm(list=ls())

args = commandArgs(trailingOnly=TRUE)
if (length(args)!=4) {                              # checking the number of arguments
  stop("ERROR! 4 arguments should be applied in order to execute this script\n", call.=FALSE)
} 

insList=read.table(file=args[1], sep="\t")          # the tab-delimited file that contain all info about the insertions
ctrlList=read.table(file=args[2],header = FALSE)   # a list of control points
CTRLResPATH=args[3]                                 # the path to the control runs
ResPATH=args[4]                                     # the path to normal runs

#Initializing some structures to save clean data and thresholds for ploting for sample type 00 and 11
thresholds0 <- array(NA, nrow(insList)); insData0 <- list()
thresholds1 <- array(NA, nrow(insList)); insData1 <- list()

#Calculation of thresholds
x0=1; x1=1;
for(i in 1:nrow(insList)){      # for each insertion
  chr=insList[i,1]            # An identifier to the chromosome that was scanned
  pos=insList[i,2]            # The position of the insertion
  type=insList[i,6]           # how the samples are genotyped, defines the type
  
  #checking type defined in the tab file
  if(type==0){
    type="00"
  }else{
    type="11"
  }

    maxLDs <- array(NA, nrow(ctrlList))  # In this array we will collect all max LDs
    # Then the 95% of those maximums will define threshold for each insertion
    
    for(y in 1:nrow(ctrlList)){          # Reading all control runs and keeping the max value
      # Composition of the filename of each control run
      controlCHR=strsplit(strsplit( as.character(ctrlList[y,]), "chr")[[1]][2],"\\.")[[1]][1]
      controlNUM=strsplit(strsplit( as.character(ctrlList[y,]), "chr")[[1]][2],"\\.")[[1]][2]
      ctrlfile=paste(CTRLResPATH,"SweeD_Report.chr",chr,".",pos,".",type,".at.chr",controlCHR,".",controlNUM,".grid.run",sep="")
      # Reading the file and cleaning it from the last and the first 4 lines, that are useless
      ctrlRes=read.table(file=ctrlfile,skip=4)
      cleanctrlRes=ctrlRes[1:(nrow(ctrlRes)-1),1:2]
      # Finding and storing th max LD value of each control run
      mMax=max(cleanctrlRes[,2])
      maxLDs[y]=mMax
    }
    # The 95% percentile of the maximum likelihoods values is used as threshold for each insertion
    threshold<-quantile(maxLDs, probs = c(0.95))
    
  # Reading the sweed run in the insertion area and cleaning it from the last and the first 4 lines, that are useless
  ins=read.table(file=paste(ResPATH,"SweeD_Report.chr",chr,".",pos,".",type,".run",sep=''),skip=4)
  cleanIns=ins[1:(nrow(ins)-1),1:2]
  
  # Save everything for ploting
  if(type=="00"){
    insData0[[x0]] <- cleanIns
    thresholds0[x0] <- threshold
    x0=x0+1
  }else{
    insData1[[x1]] <- cleanIns
    thresholds1[x1] <- threshold
    x1=x1+1
  }
}

## Ploting Time
x0=1;x1=1;
pdf(paste(paste("sweed.plot.pdf", sep='')), height = 5*(nrow(insList)/2), width = 10)
layout( matrix(1:(nrow(insList)), ncol = 2, byrow = T))
for( j in 1:nrow(insList)){       # for each insertion
  insChr=insList[j,1]             # An identifier to the chromosome that was scanned
  insPos=insList[j,2]             # The position of the insertion
  type=insList[j,6]               # how the samples are genotyped, defines the type
  #According to the genotype of each insertion sample list, we choose the input and the message to be printed over each plot
  if(type==0){
    plot(insData0[[x0]][,1], insData0[[x0]][,2], pch=19, cex=0.7, ylim=c(0,max(insData0[[x0]][,2]*1.2, thresholds0[x0]*1.2)), xlab="Position", ylab="CLR", main=paste("chr: ", insChr, " Position: ", insPos, " Type: 00" ))
    abline(h=thresholds0[x0], col="red")    # drawing a red line where the threshold is defined
    x0=x0+1
  }else{
    plot(insData1[[x1]][,1], insData1[[x1]][,2], pch=19, cex=0.7, ylim=c(0,max(insData1[[x1]][,2]*1.2, thresholds1[x1]*1.2)), xlab="Position", ylab="CLR", main=paste("chr: ", insChr, " Position: ", insPos, " Type: 11" ))
    abline(h=thresholds1[x1], col="red")    # drawing a red line where the threshold is defined
    x1=x1+1
  } 
}
dev.off()