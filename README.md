# SweeD Kutsukos Workflow 3.2
This series of steps was used to detect positive selection on ERV insertions in the human genome. For this example, we are going to use only two ERV insertions.

**Don't forget!** During this example-workflow, we are talking about ERVs insertions in human genome. This example may apply to insertions in other species. Use it wisely!



# Table of contents
1. [Required applications and OS](#reqs)
2. [Step 1 - Project initialization and SweeD downloading](#step1)
2. [Step 2 - Preparation of the required data ](#step2)
   1. [Step 2.1 - ERV Insertions Information](#step21)
   2. [Step 2.2 - Samples extraction from vcf file](#step22)
   3. [Step 2.3 - Grid points selection](#step23)
   4. [Step 2.4 - Files downloading for analysis](#step24)
3. [Step 3 - Preparing SweeD commands](#step3)
4. [Step 4 - Executing SweeD commands](#step4)
5. [Step 5 - Control runs](#step5)
6. [Step 6 - Preparation of the required data for control runs](#step6)
  1. [Step 6.1 - Files downloading for analysis](#step61)
  2. [Step 6.2 - Grid points selection REMINDER!](#step62)
7. [Step 7 - Preparing SweeD control commands - Stage1 [using -osf option]](#step7)
8. [Step 8 - Executing SweeD control commands- Stage1 [using -osf option] ](#step8)
9. [Step 9 - Preparing SweeD control commands - Stage2 [using -osf option] ](#step9)
10. [Step 10 - Executing SweeD control commands- Stage2 [using -osf option] ](#step10)
11. [Step 11 - Visualization of SweeD results ](#step11)
12. [Citations](#cite)
13. [Version Changelog](#version)
14. [Contact](#contact)


## Required applications and OS <a name="reqs"></a>
[![uses-bash](https://img.shields.io/badge/Uses%20-Bash-blue.svg)](https://www.gnu.org/software/bash/)

[![Python 2.7](https://img.shields.io/badge/Python-2.7-green.svg)](https://www.python.org/)
[![R 3.6.0](https://img.shields.io/badge/R-3.6.0-green.svg)](https://www.r-project.org/)
[![Gunzip](https://img.shields.io/badge/Gunzip-1.6-green.svg)](https://www.gzip.org/)

[![Git](https://forthebadge.com/images/badges/uses-git.svg)](https://git-scm.com/)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)



## Step 1 - Project initialization and SweeD downloading <a name="step1"></a>
In this workflow, we are going to use SweeD to detect positive selection. Information and download links for SweeD can be found here: 

1. [www.exelixis-lab.org/software.html](http://www.exelixis-lab.org/software.html) 
2. [github.com/idaios/sweed](https://github.com/idaios/sweed)


The first step should be to create a directory with your project name. Then, download and install SweeD inside this directory.


```console
$ mkdir your-project-name
$ cd your-project-name/
$ git clone https://github.com/idaios/sweed
$ cd sweed/
$ ./compile_rename_ALL.sh
$ cd ..
```

After the sequence of commands, you have successfully installed SweeD and you are ready to move to the next step.


<br>



## Step 2 - Preparation of the required data <a name="step2"></a>
In this step, we will prepare the files that are going to be used for using SweeD.

<br>

#### Step 2.1 - ERV Insertions Information <a name="step21"></a>
The group of individuals and the positions, that we are going to analyse, are defined in a VCF format file. 

This file is available in this repository, in directory "Support Data" and we are going to use it in the next steps.

<code>Copy this vcf file to your "your-project-name" directory.</code>

<br>

#### Step 2.2 - Samples extraction from vcf file <a name="step22"></a>
We will use the vcf file, that was mentioned above, to extract lists of samples.
<br> In our case, we are dealing with just two insertions. So, we are going to create two files for each insertion. One file containing a list of sample names that are genotyped with 0/0 (0|0) and one file with a list of sample names that are genotyped with 1/1 (1|1).
<br>For this procedure, we are going to use a python script, that is available inside this repository. Place VCF-SamplesListCreator folder inside your working directory.

```console
$ python VCF-SamplesListCreator/VCFSamplesListCreator.py -v ERVtest.vcf
```

This command will create a bunch of files in our main directory. The files containing the samples that are genotyped with 0/1 are useless, for this research. Our next steps are to remove them and move the rest files to a separate directory, named "sampleLists", in order to keep our main directory organized. 

```console
$ rm *.01.out
$ mkdir sampleLists
$ mv *.out sampleLists/
```

<p>Now inside "sampleLists" directory, there are four files:</p>
<ol>
<li>ERVtest.1.111802592.00.out</li>
<li>ERVtest.1.111802592.11.out</li>
<li>ERVtest.12.44313657.00.out</li>
<li>ERVtest.12.44313657.11.out</li>
</ol>
<p>
These files contain lists of samples that are genotyped with 0/0 or 1/1 for insertions in chr1:111802592 and chr12:44313657 respectively.</p>

**NOTE!**  The files above, will be in this repository in the directory Support Data/sampleLists/

<br>

#### Step 2.3 - Grid points selection <a name="step23"></a>
For this analysis, we want to apply SweeD in a specific area for each insertion.

There are two insertions, chr1:111802592 and chr12:44313657 and we want to create 101 equally distributed points, including the insertion position, in a 500Kb space before and after each insertion.

In chromosome 1, we want to do the analysis in 101 points, with a distance of 5000bp and the middle point to be 111802592. So starting point should be <code>middle_point-(100/2)*distance=111552592</code> and ending point should be equal to <code>middle_point+(100/2)*distance=112052592</code>.  We use 100 in this equation, to exclude the middle point and 100/2 to take the half points before and the half points after the middle point.


In chromosome 12, we want to do the analysis in 101 points, with a distance of 5000bp and the middle point to be 44313657. The same way as above, we calculate starting and ending point of our grid points.

For our needs above, we will run the following commands and make use of an another script, I have written in python.

```console
$ git clone https://github.com/kutsukos/GridFileCreator.git
$ python GridFileCreator/GridFileCreator.py -c 1 -s 111552592 -e 112052592 -d 5000
$ python GridFileCreator/GridFileCreator.py -c 12 -s 44063657 -e 44563657 -d 5000
$ mkdir gridLists
$ mv points.* gridLists/
```


Done! Now inside "gridLists" directory, there are two files containing the list of points that we are interested.

**NOTE!** The files above, will be at this repository in the directory Support Data/gridLists/

<br>

#### Step 2.4 - Files downloading for analysis <a name="step24"></a>
For this example-workflow, we want to run this process on chromosome 1 and chromosome 12 vcf files from 1000 genome project - [http://www.internationalgenome.org/data](http://www.internationalgenome.org/data)

```console
$ mkdir vcfFiles
$ wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ gunzip -k ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr12.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ gunzip -k ALL.chr12.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ mv ALL.* vcfFiles/
```


<br>

## Step 3 - Preparing SweeD commands <a name="step3"></a>
For this example, we have just 4 runs to execute, but in other cases, there can be more. So we developed SweeDcc python script in order to create a list of commands. Please place SweeDcc python script inside the main working directory.

In order to run SweeDcc, a tab-delimited file that, will contain all the necessary information for creating the commands and to define some options, is needed. 

**NOTE!** An example tab-delimited  file, will be in this repository in the directory Support Files/ named as "testproject.tab"

This file contains 6 fixed fields per line. All data lines are tab-delimited. Fixed fields are:
1. chr - an identifier to the chromosome to be scanned
2. position - the position of the insertion
3. input data filepath - the path to the vcf/bam file, that is going to be used for applying SweeD.
4. grid points filepath - the path to the file containing the grid points
5. sample list filepath - the path to the file containing the samples' list
6. samples type - the type of samples, contained in file above. [00/11]

In case, you do not want to use grid file or sample list, fill the corresponding field with a dot (“.”).
In our case, we will use both of those options.

SweeDcc need also some arguments:
1. -t | The number of threads to be used in  executing SweeD
2. -g | Grid. For more info, please read SweeD Manual. In case there is a grid file used, this option is ignored
3. -S | Flag to create commands for running SweeD with vcf files as input

For our example, we will choose <code>2</code> threads and <code>111</code> as grid, which will be ignored, because we use a grid file.

```console
$ python SweeDcc.py -S -i testproject.tab -t 2 -g 111
$ chmod +x testproject.SweeD.cmd
```
<br>

## Step 4 - Executing SweeD commands <a name="step4"></a>
The commands are written in <code>testproject.SweeD.cmd</code> file. The next step is to just execute this file, since it is already executable.

**NOTE!** In case, where this file has too many commands, there are ways to run these commands in parallel.

In our case, we have just 4 commands to run, so there is no need to hurry. :D

```console
$ ./testproject.SweeD.cmd
$ mkdir sweedResults
$ mv *run sweedResults/
```

Now inside sweedResults directory, there are the results from SweeD execution.

<br>

## **Ιmportant Note!**
By successfully executing the steps above, we have actually completed detection of selective sweeps using SweeD. The steps below are written for the "Detecting positive selection on ERV insertions in the human genome" project and what these steps describe is how to create control runs in order to define thresholds for each insertion's results and how to visually make conclusions.

<br>

## Step 5 - Control runs <a name="step5"></a>
In order to have a more clear view of the results, we need some control runs to define threshold for each insertion's SweeD results. 

In our case, we want to see how the values range in 500Kb areas of the genome, where there are no ERVs insertions, areas without any reference transposable elements (LTRs, SINEs and LINEs).

We used <code>RepeatMasker</code> with <code>Dfam2.0</code> and <code>RepBaseRepeat MaskerEdition 20170127</code> libraries on <code>GRCh37/hg19</code> human genome reference, to get the positions of reference transposable elements. This procedure produced four files. A file with alignments of the query with the matching repeats, the human genome in which all recognized interspersed or simple repeats have been masked, a table annotating the masked sequences and a table summarizing the repeat content of the query sequence.
<br>The outputs of RepeatMasker can be found here <code>https://figshare.com/articles/GRCh37_hg19_RepeatMasker/7851005/1</code> .

Regions without any reference transposable elements, were discovered using a script on RepeatMasker's results, while centromeres and telomeres were excluded manually.

In <code>https://github.com/kutsukos/kutsukos2019SupplementaryData</code>, you can access all control regions, that was discovered at the procedure explained above.

Then, SweeD will be applied on 350 (500Kb) subregions of those regions for each insertion's sample list.

Finally, the 95% percentile of the maximum likelihoods values will be used as thresholds, which will help us to infer which insertions have evidence for selection, visually.

For this example, we are going to use a few of those areas, just to show how the workflow worked for all of those. 
The files, we are going to use as grid points for the control runs are inside <code>gridListsCTRL</code> directory.

<br>

## Step 6 - Preparation of the required data for control runs <a name="step6"></a>

#### Step 6.1 - Files downloading for analysis <a name="step61"></a>
Lets say that, except chromosome 1 and 12, we have areas without ERVs insertions in chromosome 21 and 18. In fact, we do not have any areas, to satisfy our criteria, in chromosome 12.

```console
$ wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr18.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ gunzip -k ALL.chr18.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ gunzip -k ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ mv ALL.* vcfFiles/
```
<br>

#### Step 6.2 - Grid points selection REMINDER! <a name="step62"></a>
The files, we are going to use as grid points for the control runs are inside <code>gridListsCTRL</code> directory

<br>

## Step 7 - Preparing SweeD control commands - Stage1 [using -osf option] <a name="step7"></a>
In this example, we have many control areas in the same chromosomes and it will take us long time to execute the analysis in all of them.

SweeD give us the opportunity to firstly calculate osf for all samples of each insertion in whole chromosomes and then calculate values for each area separately.

For this procedure, we will use again, <code>SweeDcc</code> python script, you can find inside this repository, to create the commands. The script, in this case, needs a tab-delimited file with some mandatory information and a file containing a list of the input data filepaths that are going to be used for applying SweeD. 

**NOTE!** Both of those files, can be found in support data. Reach them to understand the format and the content of those files.

The tab-delimited file contains 3 fixed fields per line. Fixed fields are:
1. chr - an identifier to the insertion's chromosome
2. position - the position of the insertion
3. sample list filepath - the path to the file containing the samples' list

We will have also to define some arguments for SweeDcc:
1. -i | A tab-delimited file with some basic information for the run
2. -v | A file that contains a list of filepaths to vcf files for the analysis
3. -t | The number of threads to be used in  executing SweeD
4. -O | To create commands for running SweeD to output osf files

Now, we are ready to create some commands.

```console
$ python SweeDcc.py -O -i testproject.ctrlosf.tab -v vcfList.list -t 2
```
This command will create a file <code>testproject.ctrlosf.sfOUT.cmd</code> with the commands that we will need to execute in order to create sf files that are needed for the next stage of this analysis.

<br>

## Step 8 - Executing SweeD control commands- Stage1 [using -osf option] <a name="step8"></a>
Now we can execute the commands and create a folder to move the outputs there.

As mentioned above, there are ways to run these commands in parallel, but this workflow is not designed this way.
```console
$ chmod +x testproject.ctrlosf.sfOUT.cmd
$ ./testproject.ctrlosf.sfOUT.cmd
$ mkdir sweedCTRLOSF
$ mv *.sfrun sweedCTRLOSF/
$ mv *.sf sweedCTRLOSF/
```

<br>

## Step 9 - Preparing SweeD control commands - Stage2 [using -osf option] <a name="step9"></a>
For this procedure, we will use for one last time, <code>SweeDcc</code> python script, you can find inside this repository, to create the commands. This script needs a tab-delimited file with some basic information, we already have created for previous purpose. 
This file is <code>testproject.ctrl.list</code> and is provided in this repository in support data directory.

We will have also to define some arguments for SweeDCMDcreator.sfIN:
1. -i | A tab-delimited file with some basic information for the run
2. -t | The number of threads to be used
3. -p | The path where the sf files are stored. We created this directory in Step 6.2.1
4. -I | To create commands for running SweeD with osf files as input

Now, we are ready to create some commands.

```console
$ cd gridListsCTRL/
$ ls > ctrlpoints.list
//In this step remember to open ctrlpoints.list file and delete the last line.
$ cd ..
$ python SweeDcc.sfIN.py -I -i testproject.ctrlosf.tab -t 2 -p sweedCTRLOSF/ -l gridListsCTRL/ctrlpoints.list -L gridListsCTRL/
```

<br>

## Step 10 - Executing SweeD control commands - Stage2 [using -osf option] <a name="step10"></a>
```console
$ chmod +x testproject.ctrlosf.sfIN.cmd
$ ./testproject.ctrlosf.sfIN.cmd
$ mkdir sweedCTRLResults 
$ mv *run sweedCTRLResults/
```

<br>

## Step 11 - Visualization of SweeD results [optional] <a name="step11"></a>
If you have reached this step, you have actually finished, the detection of positive selection on ERV insertions in the human genome. Now, you can develop a script, that will define thresholds from the control runs and then these thresholds will may help you, to choose which insertions have evidence for positive selection.

We chose to calculate and draw the thresholds on the SweeD results plots, using a script in R.

**NOTE!** You can find this script, in this repository. If you have experience in R, it will be easy to edit this script and bring it to your feet! Also, in [step5](#step5) we had explained, how the thresholds will be defined, in this script. Take a look there, to understand more the whole procedure.



SweeDPlot.R script need 4 arguments to run. The first two are files, we created before in order to create the commands for running SweeD.

The last two arguments are the paths, first for the control results and second for the main SweeD results. So the command is the following...

```console
$ Rscript SweeDPlot.R testproject.tab gridListsCTRL/ctrlpoints.list sweedCTRLResults/ sweedResults/
```

This script creates a pdf file named "sweed.plot.pdf", that contains the plots we wanted to create.

<br>

## CITATIONS <a name="cite"></a>
1. Pavlidis, P., Živković, D., Stamatakis, A., & Alachiotis, N. (2013). SweeD: likelihood-based detection of selective sweeps in thousands of genomes. Molecular biology and evolution, 30(9), 2224-2234.

2. Smit, AFA and Hubley, R and Green, P. RepeatMasker Open-4.0. 2013--2015 [http://www.repeatmasker.org](http://www.repeatmasker.org)

3. Hubley, Robert, et al. "The Dfam database of repetitive DNA families." Nucleic acids research 44.D1 (2015): D81-D89.

4. Bao, Weidong, Kenji K. Kojima, and Oleksiy Kohany. "Repbase Update, a database of repetitive elements in eukaryotic genomes." Mobile Dna 6.1 (2015): 11.

5. Koutsoukos, I., Pavlidis, P.: GRCh37/hg19 RepeatMasker, [https://figshare.com/articles/GRCh37_hg19_RepeatMasker/7851005/1](https://figshare.com/articles/GRCh37_hg19_RepeatMasker/7851005/1), (2019)

## VERSION CHANGELOG <a name="version"></a>
<pre>
-3 
   + A more specialized workflow for this project
-3.1 - CURRENT
   + Comments added in python and R scripts
   + One python script to create commands for SweeD
</pre>


## Contact <a name="contact"></a>
Contact me at <code>skarisg@gmail.com</code> or <code>ioannis.kutsukos@gmail.com</code> for reporting bugs or anything else! :)