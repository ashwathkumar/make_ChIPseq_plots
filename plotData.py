import numpy as np
import pysam
import pandas as pd
from matplotlib import pyplot
from utils import makeXYbinned,getColorDict,makeColorList,getMinMaxY

def makePlot (numSamples,ip_in,col_bar,samples,row,outDir):
    """Make distribution plots (PNG files).

    Keyword arguments:
    numSamples -- Number of samples
    ip_in -- the count value to plot for each bin
    col_bar -- color values for each sample
    samples -- sample information
    outDir -- the imaginary part (default ".")
    """
    f, axarr = pyplot.subplots(numSamples, sharex=True, sharey=True,figsize=(5,(numSamples+1)))
    miny,maxy = getMinMaxY(ip_in)
    maxTick = len(ip_in[0])
    for plot in range(len(ip_in)):
        axarr[plot].bar(list(range(len(ip_in[plot]))),ip_in[plot],width=1.0,color=col_bar[plot])
        axarr[plot].set_ylabel(ylabel=samples.iloc[:,0][plot])
    f.subplots_adjust(hspace=0.2)
    for a in range(len(f.axes)):
        f.axes[a].set_yticks([miny,maxy],minor=False)
        if a == len(f.axes)-1:
            f.axes[a].set_xticks([0,maxTick],minor=False)
        else:
            f.axes[a].tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False) 
            f.axes[a].set_xticklabels([str(row[1]),str(row[2])])
    f.suptitle("Region: "+row[0]+":"+str(row[1])+"-"+str(row[2]))
    pyplot.savefig(outDir+"/"+row[0]+"_"+str(row[1])+"-"+str(row[2])+".png",bbox_inches='tight')


def plotWrapper (samples,regions,args):
    """Wrapper for making plots.

    Keyword arguments:
    samples -- sample information
    regions -- regions to be plotted
    args -- Extra arguments passed to other functions
    """
    if args.noControl:
        IP_samples = [pysam.AlignmentFile(i,"rb") for i in samples.iloc[:,2]]
    else:
        IP_samples = [pysam.AlignmentFile(i,"rb") for i in samples.iloc[:,2]]
        IN_samples = [pysam.AlignmentFile(i,"rb") for i in samples.iloc[:,3]]
    for index, row in regions.iterrows():
        if args.noControl:
            ipXY = [makeXYbinned(IP_sam,row[0],int(row[1]),int(row[2]),args) for IP_sam in IP_samples]
            ip_in = []
            for sample in range(len(ipXY)):
                ip_in.append([i for i in ipXY[sample][1]])
        else:
            ipXY = [makeXYbinned(IP_sam,row[0],int(row[1]),int(row[2]),args) for IP_sam in IP_samples]
            inXY = [makeXYbinned(IN_sam,row[0],int(row[1]),int(row[2]),args) for IN_sam in IN_samples]
            ip_in = []
            for sample in range(len(ipXY)):
                ip_in.append([i - j for i, j in zip(ipXY[sample][1], inXY[sample][1])])
        colList = getColorDict(samples)
        col_bar = makeColorList(ip_in,colList,samples)
        makePlot(len(ipXY),ip_in,col_bar,samples,row,args.outputDir)