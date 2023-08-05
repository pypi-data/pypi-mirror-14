# MicrobeCensus
MicrobeCensus is a fast and easy to use pipeline for estimating the average genome size (AGS) of a microbial 
community from metagenomic data. 

In short, AGS is estimated by aligning reads to a set of universal single-copy gene families present in nearly all cellular microbes (Bacteria, Archaea, Fungi). 
Because these genes occur once per genome, the average genome size of a microbial community is inversely proportional to the fraction of reads which hit these genes.

Once AGS is obtained, it becomes possible to obtain the total coverage of microbial genomes present in a sample (genome equivalents = total bp sequenced/AGS in bp), which can be useful for normalizing gene abundances.

### Requirements
* Python dependencies (installed via setup.py): Numpy, BioPython
* Supported platforms: Mac OSX, Unix/Linux; Windows not currently supported
* Python version 2 or 3

### Installation
Download MicrobeCensus from: https://github.com/snayfach/MicrobeCensus/archive/v1.0.7.tar.gz  

Unpack the project: 
`tar -zxvf MicrobeCensus-1.0.7.tar.gz`

Navigate to the installation directory:  
`cd /path/to/MicrobeCensus`  

Run setup.py. This will install any dependencies:  
`python setup.py install` or  
`sudo python setup.py install` to install as a superuser

Alternatively, MicrobeCensus can be installed directly from PyPI:  
`pip install MicrobeCensus` or   
`sudo pip install MicrobeCensus` to install as a superuser, or  
`pip install --user MicrobeCensus` to install in your home directory  

### Using MicrobeCensus without installing
Although this is not recommended, users may wish to run MicrobeCensus without running setup.py.  

Both BioPython and Numpy will both need to be already installed.
You should be able to enter the following command in the python interpreter without getting an error:  
`>>> import Bio.SeqIO`  
`>>> import numpy`

Next, add the MicrobeCensus module to your PYTHONPATH environmental variable:  
`export PYTHONPATH=$PYTHONPATH:/path/to/MicrobeCensus` or  
`echo -e "\nexport PYTHONPATH=\$PYTHONPATH:/path/to/MicrobeCensus" >> ~/.bash_profile` to avoid entering the command in the future

Finally, add the scripts directory to your PATH environmental variable:  
`export PATH=$PATH:/path/to/MicrobeCensus/scripts` or  
`echo -e "\nexport PATH=\$PATH:/path/to/MicrobeCensus/scripts" >> ~/.bash_profile` to avoid entering the command in the future

Now, you should be able to enter the command into your terminal without getting an error:  
`run_microbe_census.py -h`

### Testing the software
After installing MicrobeCensus, we recommend testing the software:  
`cd /path/to/MicrobeCensus/test`  
`python test_microbe_census.py`

### Running MicrobeCensus
MicrobeCensus can either be run as a command-line script or imported to python as a module.

#### Command-line usage
**run_microbe_census.py [-options] seqfiles outfile**

Input/Output (required):
* **SEQFILES**  
path to input metagenome(s)  
for paired-end metagenomes use commas to specify each file (ex: read_1.fq.gz,read_2.fq.gz)  
can be FASTQ/FASTA  
can be gzip (.gz) or bzip (.bz2) compressed
* **OUTFILE**  
path to output file containing AGS estimate 

Pipeline throughput (optional):
* **-n NREADS**  
number of reads to sample from seqfile and use for AGS estimation.  
to use all reads set to large number, like 100000000  
(default = 2000000)
* **-t THREADS**  
number of threads to use for database search (default= 1)  
* **-e**  
quit after average genome size is obtained and do not estimate the number of genome equivalents in SEQFILES.  
useful in combination with -n for quick tests (default = False)  

File type (optional):
* **-f {fasta,fastq}**  
file type (default = autodetect)
* **-c {fastq-sanger,fastq-solexa,fastq-illumina}**  
quality score encoding (default = autodetect)

Quality control (optional):
* **-l {50,60,70,80,90,100,110,120,130,140,150,175,200,225,250,300,350,400,450,500}**  
all reads trimmed to this length; reads shorter than this are discarded  
(default = median read length)
* **-q MIN_QUALITY**  
minimum base-level PHRED quality score (default = -5)
* **-m MEAN_QUALITY**  
minimum read-level PHRED quality score (default = -5)
* **-d**  
filter duplicate reads (default = False)
* **-u MAX_UNKNOWN**  
max percent of unknown bases per read (default = 100)
                        
Misc options: 
* **-h, --help:**            show this help message and exit 
* **-v:**                    print program's progress to stdout (default = False) 
* **-V, --version:**         show program's version number and exit 

#### Module usage

First, import the module:  
`>>> from microbe_census import microbe_census`

Next, setup your options and arguments, formatted as a dictionary. The path to your metagenome is the only requirement (default values will be used for all other options):  
`>>> args = {'seqfiles':['MicrobeCensus/microbe_census/example/example.fq.gz']}`

If you have paired-end libraries, separate them with a comma:  
`>>> args = {'seqfiles':['seqfile_1.fq.gz', 'seqfile_2.fq.gz']}`

Alternatively, other options can be specified:  
```
>>> args = {
  'seqfiles':['MicrobeCensus/microbe_census/example/example.fq.gz'],
  'nreads':100000,
  'read_length':100,
  'file_type':'fastq',
  'quality_type':'fastq-sanger',
  'threads':1,
  'min_quality':10,
  'mean_quality':10,
  'filter_dups':False,
  'max_unknown':0,
  'verbose':True}
```

Finally, the entire pipeline can be run by passing your arguments to the run_pipeline function. MicrobeCensus returns the estimated AGS of your metagenome, along with a dictionary of used arguments:
`average_genome_size, args = microbe_census.run_pipeline(args)`

For normalization, you can also estimate the number of genome equivalents in your metagenome:  
`count_bases = microbe_census.count_bases(args['seqfiles'])`  
`genome_equivalents = count_bases/average_genome_size`


#### Recommended options
* When in doubt, use default parameters! In most cases, MicrobeCensus tries to pick the best parameters for you. 
* For more accurate estimates of AGS, use -n to increase the number of reads sampled. The default value of 2,000,000 should give good results, but more reads may result in slightly more accurate estimates, particularly when AGS is very large.
* Don't use quality filtering options (-q, -m, -d, -u) if you plan on using MicrobeCensus for normalization. In this case, MicrobeCensus should be directly run on the metagenome you used for estimating gene-family abundances.
* Use -v/--verbose to print program progress

### Output format
**Parameters**  
*metagenome*: path to your metagenome(s)  
*reads_sampled*: the number of reads sampled from the metagenome to estimate AGS  
*trimmed_length*: reads were trimmed to this length to estimate AGS  
*min_quality*: minimum per-base quality  
*mean_quality*: minimum average-base quality  
*filter_dups*: filter exact duplicate reads  
*max_unknown*: filter reads where the % of Ns is greater than this

**Results**  
*average_genome_size*: the average genome size (in bp) of your input metagenome  
*total_bases*: the total number of base-pairs of your input metagenome  
*genome_equivalents*: the total coverage of microbial genomes in your input metagenome

### Normalization
The number of genome equivalents can be used to normalize count data obtained from metagenomes using the statistic **RPKG (reads per kb per genome equivalent)**. This is similar to the commonly used statistic RPKM, but instead of dividing by the number of total mapped reads, we divide by the number of genome equivalents:

>RPKG = (reads mapped to gene)/(gene length in kb)/(genome equivalents)

Use case: 
We have two metagenomic libraries, L1 and L2, and we use MicrobeCensus to estimate the number of genome equivilants in each: 
>GE_L1 = 40  
>GE_L2 = 20  

Next, we map reads from each library to a reference database which contains a gene of interest G. G is 1000 bp long. 
We get 100 reads mapped to gene G from each library:
>LENGTH_G = 1,000 bp  
>MAPPED_READS_G_L1 = 100  
>MAPPED_READS_G_L2 = 100

Finally, we quantify RPKG for gene G in each library:
>RPKG for G in L1 = (100 mapped reads)/(1 kb)/(40 GE) = 2.5  
>RPKG for G in L2 = (100 mapped reads)/(1 kb)/(20 GE) = 5.0  

### Software speed
* Run times are for a 150 bp library. Expect longer/shorter runtimes depending on read length.

Threads (-t)  | Reads/Second
------------- | -------------
1  | 830
2  | 1,300
4  | 1,800
8  | 2,000

### Known bugs/issues
* MicrobeCensus cannot hande FASTQ files with invalid formatting. See: https://en.wikipedia.org/wiki/FASTQ_format#Format. Common mistakes include differences in descriptions between sequence and quality headers:
```
@SEQ_ID
GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
+SEQ_ID not ok
!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65
```
```
@SEQ_ID this is ok
GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
+SEQ_ID this is ok
!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65
```


### Training
We have included scripts and documentation for retraining MicrobeCensus, using user-supplied training genomes and gene families. Documentation and scripts can be found under: MicrobeCensus/training

### Citing
If you use MicrobeCensus, please cite:  

Nayfach, S. and Pollard, K.S. Average genome size estimation improves comparative metagenomics and sheds light on the functional ecology of the human microbiome. _Genome biology 2015;**16**(1):51_.

