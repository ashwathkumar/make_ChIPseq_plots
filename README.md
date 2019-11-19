# Make ChIP-seq signal distribution plots. 

Script `makePlots.py` is a helper script to make ChIP-seq signal distribution plots. It utilizes `pysam` module to obtain read counts over interested regions and divides them into bins of given size. 

The command for running the script is 

```
usage: makePlots.py [-h] [--outputDir OUTPUTDIR] [--binSize BINSIZE] [--normalizeDepth] [--noControl] sampleInfo regionBed

Plot ChIP-seq signal over regions of interest
positional arguments:
  sampleInfo            File containing the sample information
  regionBed             Bed file containing the regions to be plotted

optional arguments:
  -h, --help            show this help message and exit
  --outputDir OUTPUTDIR
                        Output directory for images
  --binSize BINSIZE     Size of the bins in the plot (default:100bp)
  --normalizeDepth      Normalizes signals for all samples for sequencing
                        depth. Normalizes to 1,000,000 reads.
  --noControl           Make plots without using control samples (IN/IgG)
```

The `sampleInfo` file should contain sample name, Group, IP bam file path and IN bam file path. The format for this file can be seen in the example file `test/sample_info.txt`. The input regions are given in bed format. Only the first three columns are used from this bed file i.e chr, start and stop. 

`normalizeDepth` parameter tells the script to normalize each sample by sequencing depth. The script normalizes all samples to 1 million read depth before plotting. The `noControl` option tells the script to not use the IN sample singal while plotting. By default, IN values are subtracted from IP values before plotting. 

## Examples

The example bam files and the input files are located in the `test/bam` folder and the input files are in the `test` folder. 

### With control:

First example images in the `test/withControl` folder are the result of the following command.
```
python3 makePlots.py test/sample_info.txt test/test_regions.bed --outputDir="./test/withControl"
```

### Without control:

Second example images in the `test/noControl` folder are the result of the following command.
```
python3 makePlots.py test/sample_info.txt test/test_regions.bed --outputDir="./test/noControl" --noControl
```
