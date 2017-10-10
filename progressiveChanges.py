import sys
import os
import subprocess
import networkx as nx

def colorstr(rgb): return "#%02x%02x%02x" % (rgb[0],rgb[1],rgb[2])

def hsl_to_rgb(h, s, l):
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs(h *1.0 / 60 % 2 - 1))
    m = l - c/2
    if h < 60:
        r, g, b = c + m, x + m, 0 + m
    elif h < 120:
        r, g, b = x + m, c+ m, 0 + m
    elif h < 180:
        r, g, b = 0 + m, c + m, x + m
    elif h < 240:
        r, g, b, = 0 + m, x + m, c + m
    elif h < 300:
        r, g, b, = x + m, 0 + m, c + m
    else:
        r, g, b, = c + m, 0 + m, x + m
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return (r,g,b)

class scalableVectorGraphics:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.out = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   height="%d"
   width="%d"
   id="svg2"
   version="1.1"
   inkscape:version="0.48.4 r9939"
   sodipodi:docname="easyfig">
  <metadata
     id="metadata122">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title>Easyfig</dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <defs
     id="defs120" />
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="640"
     inkscape:window-height="480"
     id="namedview118"
     showgrid="false"
     inkscape:zoom="0.0584"
     inkscape:cx="2500"
     inkscape:cy="75.5"
     inkscape:window-x="55"
     inkscape:window-y="34"
     inkscape:window-maximized="0"
     inkscape:current-layer="svg2" />
  <title
     id="title4">Easyfig</title>
  <g
     style="fill-opacity:1.0; stroke:black; stroke-width:1;"
     id="g6">''' % (self.height, self.width)

    def drawLine(self, x1, y1, x2, y2, th=1, cl=(0, 0, 0), alpha = 1.0):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n        stroke-width="%d" stroke="%s" stroke-opacity="%f" stroke-linecap="round" />\n' % (x1, y1, x2, y2, th, colorstr(cl), alpha)

    def drawPath(self, xcoords, ycoords, th=1, cl=(0, 0, 0), alpha=0.9):
        self.out += '  <path d="M%d %d' % (xcoords[0], ycoords[0])
        for i in range(1, len(xcoords)):
            self.out += ' L%d %d' % (xcoords[i], ycoords[i])
        self.out += '"\n        stroke-width="%d" stroke="%s" stroke-opacity="%f" stroke-linecap="butt" fill="none" z="-1" />\n' % (th, colorstr(cl), alpha)


    def writesvg(self, filename):
        outfile = open(filename, 'w')
        outfile.write(self.out + ' </g>\n</svg>')
        outfile.close()

    def drawRightArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + wid - ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x1, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y, x, y+ht, x + wid, y1)

    def drawLeftArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x1, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y1, x1, y+ht, x1, y)

    def drawBlastHit(self, x1, y1, x2, y2, x3, y3, x4, y4, fill=(0, 0, 255), lt=2, alpha=0.1):
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0,0,0)), lt, alpha)
        self.out += '           points="%d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y2, x3, y3, x4, y4)

    def drawGradient(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n  </defs>\n'
        self.out += '  <rect fill="url(#MyGradient)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d"/>\n' % (x1, y1, wid, hei)

    def drawGradient2(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient2" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n</defs>\n'
        self.out += '  <rect fill="url(#MyGradient2)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawOutRect(self, x1, y1, wid, hei, fill=(255, 255, 255), outfill=(0, 0, 0), lt=1, alpha=1.0, alpha2=1.0):
        self.out += '  <rect stroke="%s" stroke-width="%d" stroke-opacity="%f"\n' % (colorstr(outfill), lt, alpha)
        self.out += '        fill="%s" fill-opacity="%f"\n' % (colorstr(fill), alpha2)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawAlignment(self, x, y, fill, outfill, lt=1, alpha=1.0, alpha2=1.0):
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), outfill, lt, alpha, alpha2)
        self.out += '  points="'
        for i, j in zip(x, y):
            self.out += str(i) + ',' + str(j) + ' '
        self.out += '" />\n'
             # print self.out.split('\n')[-2]



    def drawSymbol(self, x, y, size, fill, symbol, alpha=1.0, lt=1):
        x0 = x - size/2
        x1 = size/8 + x - size/2
        x2 = size/4 + x - size/2
        x3 = size*3/8 + x - size/2
        x4 = size/2 + x - size/2
        x5 = size*5/8 + x - size/2
        x6 = size*3/4 + x - size/2
        x7 = size*7/8 + x - size/2
        x8 = size + x - size/2
        y0 = y - size/2
        y1 = size/8 + y - size/2
        y2 = size/4 + y - size/2
        y3 = size*3/8 + y - size/2
        y4 = size/2 + y - size/2
        y5 = size*5/8 + y - size/2
        y6 = size*3/4 + y - size/2
        y7 = size*7/8 + y - size/2
        y8 = size + y - size/2
        if symbol == 'o':
            self.out += '  <circle stroke="%s" stroke-width="%d" stroke-opacity="%f"\n' % (colorstr((0, 0, 0)), lt, alpha)
            self.out += '        fill="%s" fill-opacity="%f"\n' % (colorstr(fill), alpha)
            self.out += '        xc="%d" yc="%d" r="%d" />\n' % (x, y, size/2)
        elif symbol == 'x':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y2, x2, y0, x4, y2, x6, y0, x8, y2,
                                                                                                                             x6, y4, x8, y6, x6, y8, x4, y6, x2, y8,
                                                                                                                             x0, y6, x2, y4)
        elif symbol == '+':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x2, y0, x6, y0, x6, y2, x8, y2, x8, y6,
                                                                                                                             x6, y6, x6, y8, x2, y8, x2, y6, x0, y6,
                                                                                                                             x0, y2, x2, y2)
        elif symbol == 's':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y0, x0, y8, x8, y8, x8, y0)
        elif symbol == '^':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y0, x2, y0, x4, y4, x6, y0, x8, y0, x4, y8)
        elif symbol == 'v':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y8, x2, y8, x4, y4, x6, y8, x8, y8, x4, y0)
        elif symbol == 'u':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x0, y8, x4, y0, x8, y8)
        elif symbol == 'd':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x0, y0, x4, y8, x8, y0)
        else:
            sys.stderr.write(symbol + '\n')
            sys.stderr.write('Symbol not found, this should not happen.. exiting')
            sys.exit()








    def drawRightFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht/2
            y2 = y + ht * 3/8
            y3 = y + ht * 1/4
        elif frame == 2:
            y1 = y + ht * 3/8
            y2 = y + ht * 1/4
            y3 = y + ht * 1/8
        elif frame == 0:
            y1 = y + ht * 1/4
            y2 = y + ht * 1/8
            y3 = y + 1
        x1 = x
        x2 = x + wid - ht/8
        x3 = x + wid
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawRightFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht / 4
        elif frame == 2:
            y1 = y + ht /8
        elif frame == 0:
            y1 = y + 1
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawLeftFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht
            y2 = y + ht * 7/8
            y3 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 7/8
            y2 = y + ht * 3/4
            y3 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht * 3/4
            y2 = y + ht * 5/8
            y3 = y + ht / 2
        x1 = x + wid
        x2 = x + ht/8
        x3 = x
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawLeftFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht / 2
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawPointer(self, x, y, ht, lt, fill):
        x1 = x - int(round(0.577350269 * ht/2))
        x2 = x + int(round(0.577350269 * ht/2))
        y1 = y + ht/2
        y2 = y + 1
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
        self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y2, x2, y2, x, y1)

    def drawDash(self, x1, y1, x2, y2, exont):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n' % (x1, y1, x2, y2)
        self.out += '       style="stroke-dasharray: 5, 3, 9, 3"\n'
        self.out += '       stroke="#000" stroke-width="%d" />\n' % exont

    def drawPolygon(self, x_coords, y_coords, colour=(0,0,255)):
        self.out += '  <polygon points="'
        for i,j in zip(x_coords, y_coords):
            self.out += str(i) + ',' + str(j) + ' '
        self.out += '"\nstyle="fill:%s;stroke=none" />\n'  % colorstr(colour)
    def writeString(self, thestring, x, y, size, ital=False, bold=False, rotate=0, justify='left', color=(0,0,0)):
        if rotate != 0:
            x, y = y, x
        self.out += '  <text\n'
        self.out += '    style="font-size:%dpx;font-style:normal;font-weight:normal;z-index:10\
;line-height:125%%;letter-spacing:0px;word-spacing:0px;fill:%s;fill-opacity:1;stroke:none;font-family:Sans"\n' % (size, colorstr(color))
        if justify == 'right':
            self.out += '    text-anchor="end"\n'
        elif justify == 'middle':
            self.out += '    text-anchor="middle"\n'
        if rotate == 1:
            self.out += '    x="-%d"\n' % x
        else:
            self.out += '    x="%d"\n' % x
        if rotate == -1:
            self.out += '    y="-%d"\n' % y
        else:
            self.out += '    y="%d"\n' % y
        self.out += '    sodipodi:linespacing="125%"'
        if rotate == -1:
            self.out += '\n    transform="matrix(0,1,-1,0,0,0)"'
        if rotate == 1:
            self.out += '\n    transform="matrix(0,-1,1,0,0,0)"'
        self.out += '><tspan\n      sodipodi:role="line"\n'
        if rotate == 1:
            self.out += '      x="-%d"\n' % x
        else:
            self.out += '      x="%d"\n' % x
        if rotate == -1:
            self.out += '      y="-%d"' % y
        else:
            self.out += '      y="%d"' % y
        if ital and bold:
            self.out += '\nstyle="font-style:italic;font-weight:bold"'
        elif ital:
            self.out += '\nstyle="font-style:italic"'
        elif bold:
            self.out += '\nstyle="font-style:normal;font-weight:bold"'
        self.out += '>' + thestring + '</tspan></text>\n'




def get_genes(gbk):
    with open(gbk) as gbk:
        gene_dict = {}
        seqDict = {}
        getseq2 = False
        getseq = False
        getproduct = False
        for line in gbk:
            if line.startswith('LOCUS'):
                contig_name = line.split()[1]
                gene_dict[contig_name] = {}
                genes = gene_dict[contig_name]
            elif line.startswith('     CDS             complement('):
                startstop = line.split('(')[1].split(')')[0]
                start, stop = map(int, startstop.split('..'))
                strand = '-'
                gene = 'none'
            elif line.startswith('     CDS '):
                startstop = line.split()[1]
                strand = '+'
                start, stop = map(int, startstop.split('..'))
                gene = 'none'
            elif line.startswith('                     /locus_tag'):
                locus_tag = line.split('"')[1]
            elif line.startswith('                     /gene='):
                gene = line.split('"')[1]
            elif line.startswith('                     /product=') or getproduct:
                if line.startswith('                     /product='):
                    getproduct = True
                    product = line.rstrip().split('=')[1]
                else:
                    product += ' ' + line.rstrip()[21:]
                if product.endswith('"'):
                    getproduct = False
            elif line.startswith('                     /translation='):
                seq = line.rstrip().split('"')[1]
                if line.count('"') == 2:
                    genes[locus_tag] = (start, stop, strand, gene, locus_tag, seq, product)
                else:
                    getseq = True
            elif getseq:
                seq += line.split()[0]
                if seq.endswith('"'):
                    genes[locus_tag] = (start, stop, strand, gene, locus_tag, seq[:-1], product)
                    getseq = False
            elif line.startswith('ORIGIN'):
                getseq2 = True
                seq = ''
            elif line.startswith('//'):
                seqDict[contig_name] = seq
                getseq2 = False
            elif getseq2:
                seq += ''.join(line.split()[1:])
    return gene_dict, seqDict


def table_changes(gff_folder, output, order_list):
    gff_filenames = os.listdir(gff_folder)
    gff_filenames.sort()
    change_dict = {}
    gene_dict = {}
    query_gbk_list = []
    for gff_filename in gff_filenames:
        with open(gff_folder + '/' + gff_filename) as gff:
            extra_dict = {}
            for line in gff:
                if line.startswith('# QUERY_GBK='):
                    query_gbk = line.split()[1].split('=')[1]
                    query_gbk_list.append(query_gbk)
                    query_genes, query_seq = get_genes(query_gbk)
                elif line.startswith('# REF_GBK='):
                    ref_gbk = line.split()[1].split('=')[1]
                    ref_genes, ref_seq = get_genes(ref_gbk)
                elif not line.startswith('#'):
                    contig, program, so, query_start, query_stop, score, strand, phase, extra = line.rstrip().split('\t')
                    extra_dict = {}
                    for i in extra.split(';'):
                        key, value = i.split('=')
                        extra_dict[key] = value
                    mut_type = extra_dict['Name']
                    ref_coord = extra_dict['ref_coord']
                    ref_sequence = extra_dict['ref_sequence']
                    if '-' in ref_coord:
                        ref_start, ref_stop = map(int, ref_coord.split('-'))
                    else:
                        ref_start = ref_stop = int(ref_coord)
                    if (ref_sequence, ref_start, ref_stop, mut_type) in change_dict:
                        change_dict[(ref_sequence, ref_start, ref_stop, mut_type)].add(query_gbk)
                    else:
                        if 'in_genes_name' in extra_dict and extra_dict['in_genes_name'] != 'none':
                            gene_names = extra_dict['in_genes_name']
                        elif 'in_genes' in extra_dict:
                            gene_names = extra_dict['in_genes']
                        else:
                            gene_names = ''
                        change_dict[(ref_sequence, ref_start, ref_stop, mut_type)] = set([query_gbk])
                        gene_dict[(ref_sequence, ref_start, ref_stop, mut_type)] = gene_names
    new_gbk_list = []
    with open(order_list) as f:
        for line in f:
            for j in query_gbk_list:
                print line.rstrip(), j
                if line.rstrip() in j:
                    print 'ding'
                    new_gbk_list.append(j)
                    break
    query_gbk_list = new_gbk_list
    draw_list = []
    for i in change_dict:
        if 'u00000' in i[0] and len(change_dict[i]) > 1:
            draw_list.append((i + (gene_dict[i],) + (change_dict[i],)))
    draw_list.sort()
    new_draw_list = []
    last_gene_name = None
    for i in draw_list:
        ref_sequence, ref_start, ref_stop, mut_type, gene_name, pset = i
        if last_gene_name is None:
            last_gene_name = gene_name
            last_ref_start = ref_start
        elif ref_start <= last_ref_stop + 5000 and pset == last_pset:
            if not gene_name in last_gene_name:
                last_gene_name += ',' + gene_name
            last_mut_type = 'multiple changes'
        else:
            new_draw_list.append((last_ref_seq, last_ref_start, last_ref_stop, last_mut_type, last_gene_name, last_pset))
            last_gene_name = gene_name
            last_ref_start = ref_start
        last_ref_seq = ref_sequence
        last_ref_stop = ref_stop
        last_mut_type = mut_type
        last_pset = pset
    new_draw_list.append((last_ref_seq, last_ref_start, last_ref_stop, last_mut_type, last_gene_name, last_pset))
    draw_list = new_draw_list


    color_list = [(240,163,255),(0,117,220),(153,63,0),(76,0,92),(0,92,49),(43,206,72),(255,204,153),
                  (128,128,128),(148,255,181),(143,124,0),(157,204,0),(194,0,136),(0,51,128),(255,164,5),(255,168,187),
                  (66,102,0),(255,0,16),(94,241,242),(0,153,143),(224,255,102),(116,10,255),(153,0,0),(255,255,128),
                  (255,255,0),(255,80,5)]
    color_dict = {}
    svg = scalableVectorGraphics(5000, 5000)
    x_margin = 100
    y_margin = 100
    grid_start = 400
    text_start = 300
    square_width = 9
    total_width = 10
    mut_freq_list = []
    y_height = len(draw_list) * total_width
    svg.drawOutRect(x_margin, y_margin, 50, y_height, lt=3)
    color_list_index = 0
    for num, i in enumerate(query_gbk_list):
        svg.writeString(i, grid_start + num * total_width, y_margin - 5, 8, rotate=-1, justify='right')
    for num, i in enumerate(draw_list):
        ref_sequence, ref_start, ref_stop, mut_type, gene_name, pset = i
        if mut_type in color_dict:
            color = color_dict[mut_type]
        else:
            color = color_list[color_list_index]
            color_list_index += 1
            color_dict[mut_type] = color
        ref_seq_len = len(ref_seq[ref_sequence])
        genome_y = ref_start * 1.0 / ref_seq_len * y_height + y_margin
        figure_y = num * total_width + y_margin
        svg.drawPath([x_margin, x_margin+50, text_start - 20, text_start], [genome_y, genome_y, figure_y + total_width/2, figure_y + total_width/2], th=2, cl=color)
        svg.writeString(gene_name, grid_start - 5, figure_y + total_width * 0.6, 8, justify='right')
        for num2, j in enumerate(query_gbk_list):
            if j in pset:
                svg.drawOutRect(grid_start + num2 * total_width, figure_y, square_width, square_width, fill=color, lt=0)
        svg.writeString(mut_type, grid_start + len(query_gbk_list) * total_width + 5, figure_y + total_width + 0.6, 8)



    #
    #
    # new_gene_list = []
    # for i in gene_list:
    #     if i[0] >= 2:
    #         new_gene_list.append(i[1])
    # gene_list = new_gene_list
    # for num, i in enumerate(mut_freq_list):
    #     if num < len(color_list):
    #         color_dict[i[1]] = color_list[num]
    #         svg.writeString(i[1], x_margin + 90, y_margin + (len(gene_list) + num) * total_width + 0.75 * square_width + 50, 10, justify='right')
    #         svg.drawOutRect(x_margin + 100, y_margin + (len(gene_list) + num) * total_width + 50, square_width, square_width, fill=color_list[num], lt=0)
    #     else:
    #         color_dict[i[1]] = (0, 0, 0)
    # svg.writeString('other', x_margin + 90, y_margin + (len(gene_list) + len(color_list)) * total_width + 0.75 * square_width + 50, 10, justify='right')
    # svg.drawOutRect(x_margin + 100, y_margin + (len(gene_list) + len(color_list)) * total_width + 50, square_width, square_width, fill=(0, 0, 0), lt=0)
    # for num, i in enumerate(gene_list):
    #     svg.writeString(i, x_margin - 10, y_margin + num * total_width + 0.75 * square_width, 10, justify='right')
    #     svg.writeString(gene_desc[i][0], x_margin + len(gff_filenames) * total_width + 20, y_margin + num * total_width + 0.75 * square_width, 10)
    #     for num2, j in enumerate(gff_filenames):
    #         if j in gff_muts[i]:
    #             color = color_dict[gff_muts[i][j]]
    #         else:
    #             color = color_dict['no change']
    #         svg.drawOutRect(x_margin + num2 * total_width, y_margin + num * total_width, square_width, square_width, fill=color, lt=0)
    # for i in color_dict:
    #     if color_dict[i] != (50, 50, 50):
    #         svg.writeString

    svg.writesvg(output + '.svg')



table_changes(sys.argv[1], sys.argv[2], sys.argv[3])


