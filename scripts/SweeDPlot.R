rm(list=ls())
args = commandArgs(trailingOnly=TRUE)

#checking the number of arguments
if (length(args)!=4) {
  stop("ERROR! 4 arguments should be applied in order to execute this script\n", call.=FALSE)
} 

insList=read.table(file=args[1], sep="\t")
tablelist=read.table(file=args[2],header = FALSE)
CTRLResPATH=args[3]
ResPATH=args[4]

#Initializing some structures to save data for ploting for sample type 00 and 11
thresholds0 <- array(NA, nrow(insList)); insData0 <- list()
thresholds1 <- array(NA, nrow(insList)); insData1 <- list()

#Calculation of threshold
x0=1; x1=1;
for(i in 1:nrow(insList)){
  chr=insList[i,1]
  pos=insList[i,2]
  type=insList[i,6]
  
  #checking type defined in the tab file
  if(type==0){
    type="00"
  }else{
    type="11"
  }

    maxLDs <- array(NA, nrow(tablelist)) 
    
    for(y in 1:nrow(tablelist)){
      #Read and keep the max value of each run in control areas
      controlCHR=strsplit(strsplit( as.character(tablelist[y,]), "chr")[[1]][2],"\\.")[[1]][1]
      controlNUM=strsplit(strsplit( as.character(tablelist[y,]), "chr")[[1]][2],"\\.")[[1]][2]
      ctrlfile=paste(CTRLResPATH,"SweeD_Report.chr",chr,".",pos,".",type,".at.chr",controlCHR,".",controlNUM,".grid.run",sep="")
      
      ctrlRes=read.table(file=ctrlfile,skip=4)
      cleanctrlRes=ctrlRes[1:(nrow(ctrlRes)-1),1:2]
      mMax=max(cleanctrlRes[,2])
      maxLDs[y]=mMax
    }
    #the 95% percentile of the maximum likelihoods values is used as threshold for each insertion
    threshold<-quantile(maxLDs, probs = c(0.95))  #CHANGE here if you want the percentile of the max values to be the threshold
    
  #read and clean the values of each run in insertion area
  ins=read.table(file=paste(ResPATH,"SweeD_Report.chr",chr,".",pos,".",type,".run",sep=''),skip=4)
  cleanIns=ins[1:(nrow(ins)-1),1:2]
  
  #save everything for ploting
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
for( j in 1:nrow(insList)){
  insChr=insList[j,1]
  insPos=insList[j,2]
  type=insList[j,6]
  #According to the type of sample list, we choose the input and the message to be printed over each plot
  if(type==0){
    plot(insData0[[x0]][,1], insData0[[x0]][,2], pch=19, cex=0.7, ylim=c(0,max(insData0[[x0]][,2]*1.2, thresholds0[x0]*1.2)), xlab="Position", ylab="CLR", main=paste("chr: ", insChr, " Position: ", insPos, " Type: 00" ))
    abline(h=thresholds0[x0], col="red")
    x0=x0+1
  }else{
    plot(insData1[[x1]][,1], insData1[[x1]][,2], pch=19, cex=0.7, ylim=c(0,max(insData1[[x1]][,2]*1.2, thresholds1[x1]*1.2)), xlab="Position", ylab="CLR", main=paste("chr: ", insChr, " Position: ", insPos, " Type: 11" ))
    abline(h=thresholds1[x1], col="red")
    x1=x1+1
  } 
}
dev.off()