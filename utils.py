import matplotlib
import numpy as np
import pysam
import pandas as pd


def makeXYbinned (inSam,chr,start,stop,args):
    """Get binned counts for sample.

    Keyword arguments:
    inSam -- input file
    chr -- chromosome of region
    start -- start position
    stop -- stop position
    args -- Extra arguments such as bin size
    """
    temp = []
    for i in range(start,stop,args.binSize):
        cnt = inSam.count(chr,i,i+args.binSize-1)
        temp.append(cnt)
    if args.normalizeDepth:
        temp2 = [(x/inSam.mapped)*1000000 for x in temp]
        return (list(range(len(temp2))),temp2)    
    else:
        return (list(range(len(temp))),temp)

def getColorDict (samples):
    """Make a color dictionary used in plotting each sample."""
    cmap = matplotlib.cm.get_cmap('tab20',20) #set colormap. This does pose a 10 unique label limit as of now. Can change to continuous colormap if needed for more samples but currently no use for me. 
    cmap_hex = []
    for i in range(cmap.N):
        rgb = cmap(i)[:3]
        cmap_hex.append(matplotlib.colors.rgb2hex(rgb))
    tmp_dict = {}
    count = 0
    for label in samples.iloc[:,1]:
        if label not in tmp_dict:
            tmp_dict[label] = [cmap_hex[count*2+1],cmap_hex[count*2]]
            count = count + 1
    return tmp_dict

def makeColorList(ip_in,colList,samples):
    """Make a color list from the color dictionary directly used in coloring the plots."""
    col_bar = []
    for sample in range(round(len(ip_in))):
        col_bar.append([colList[samples.iloc[sample,1]][0] if i < 0 else colList[samples.iloc[sample,1]][1] for i in ip_in[sample]])
    return col_bar
    

def getMinMaxY(ip_in):
    """Get the maximum and minimum y axis value across all samples."""
    miny = 0
    maxy = 0
    for plot in range(len(ip_in)):
        if max(ip_in[plot]) > maxy:
            maxy = round(max(ip_in[plot]),2)
        if min(ip_in[plot]) < miny:
            miny = round(min(ip_in[plot]),2)
    return miny,maxy
