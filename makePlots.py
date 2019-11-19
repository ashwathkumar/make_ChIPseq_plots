import argparse
import pandas as pd
import plotData

def parseArgs ():
    """Parse command line arguements and returns them."""
    parser = argparse.ArgumentParser(description="Plot ChIP-seq signal over regions of interest")
    parser.add_argument("sampleInfo", type=str, help="File containing the sample information")
    parser.add_argument("regionBed", type=str, help="Bed file containing the regions to be plotted")
    parser.add_argument("--outputDir", type=str,default=".", help="Output directory for images")
    parser.add_argument("--binSize", type=int,default=100, help="Size of the bins in the plot (default:100bp)")
    parser.add_argument("--normalizeDepth", action="store_true",help="Normalizes signals for all samples for sequencing depth. Normalizes to 1,000,000 reads.")
    parser.add_argument("--noControl", action="store_true",help="Make plots without using control samples (IN/IgG)")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args_all = parseArgs()
    regions = pd.read_csv(args_all.regionBed,sep="\t",header=None)
    samples = pd.read_csv(args_all.sampleInfo,sep="\t",header=0)
    plotData.plotWrapper(samples,regions,args_all)
    