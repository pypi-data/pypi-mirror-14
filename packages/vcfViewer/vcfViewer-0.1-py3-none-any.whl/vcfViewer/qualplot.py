from cyvcf2 import VCF
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import Span, HoverTool, PanTool
import sys


# Create command line interface.
vcfFile = sys.argv[1]
threshold = int(sys.argv[2])

# Create empty lists, to be populated by the positions and quality scores of SNPs that
# either pass (gx and gy) or fail (rx and ry).  
gx = [] 
gy = []
rx = []
ry = []

# Source the above lists. This is necessary for the functionality of the HoverTool created later.
source1 = ColumnDataSource(data=dict(ggx=gx, ggy=gy))
source2 = ColumnDataSource(data=dict(rrx=rx, rry=ry))

# Parse the user-provided VCF file. If a variant's quality scores is greater than
# the user-provided threshold, add its position and quality score to 'gx' and 'gy,' respectively.
# Otherwise, add its position and quality to 'rx' and 'ry.' 
for v in VCF(vcfFile):
    if (v.end - v.start) == 1:
        if v.QUAL > threshold:
            gx.append(v.POS)
            gy.append(v.QUAL)
        elif v.QUAL < threshold:
            rx.append(v.POS)
            ry.append(v.QUAL)
        

# Name the bokeh output.
output_file("quality.html")

# Generate the dynamic bokeh figure, called 'p.'
p = figure(plot_width=1000, plot_height=500)
p.title = "Quality-ranked SNPs across Genomic Position"

# Generate a 'threshold line' based on the user's quality score threshold.
thresh_line = Span(location = threshold, dimension='width', line_color='blue', line_width=1)
p.renderers.extend([thresh_line])

# Add x and y axis labels.
p.yaxis.axis_label = "Phred-scaled Quality Score"
p.xaxis.axis_label = "Position"

# Generate the hover function for each red and green circle that is plotted.
r1 = p.circle(gx, gy, size=10, color='green', alpha=0.5, legend="Pass SNP", source=source1)
r1_hover = HoverTool(renderers=[r1], tooltips=[('Position', '@ggx') , ('Quality', '@ggy')])
p.add_tools(r1_hover)

r2 = p.circle(rx, ry, size=10, color='red', alpha=0.5, legend="Fail SNP", source=source2)
r2_hover = HoverTool(renderers=[r2], tooltips=[('Position', '@rrx') , ('Quality', '@rry')])
p.add_tools(r2_hover)

# Add a legend to the figure.
p.legend.orientation = "top_left"
show(p)
