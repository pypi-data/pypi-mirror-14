from bokeh.plotting import figure, show, output_file, vplot
from cyvcf2 import VCF
import sys

vcffile = sys.argv[1]

depth = []
pos = []
for v in VCF(vcffile):
    
    if (v.end - v.start) == 1:
        depth.append(v.INFO.get('DP'))
        pos.append(v.POS)


p = figure()
p.xaxis.axis_label = "Position"
p.yaxis.axis_label = "Depth of Coverage"
p.circle(pos, depth, color='blue')

show(p)
