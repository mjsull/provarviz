# GWviz

## Tools for visualising cumulative and recurrent mutations using pairwise comparisons generated by nucdiff.

### getVar.py
Runs nucdiff on two genbank files and then annotates a gff of changes with genes affected.

### progressiveChanges.py
Creates figure of cumulative changes to a genome over time.

### tableChanges.py
Tool for identifying genes under selective pressure. Creates a figure/table of recurrent mutations between strains.



## Running GWviz

### getVar.py
Runs nucdiff on two genbank files and then annotates a gff of changes with genes affected and mutation type i.e. synonymous/nonsynonymous.
Takes a genbank query and reference. Concatenated genbanks (i.e. PROKKA output) are acceptable.


#### USAGE: getVar.py -qg <query.gbk> -rg <reference.gbk> -w <working_directory> -o <output.gff>

Arguments:

```
-h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Will create a gff of changes
  -qg genome.gbk, --query_genbank genome.gbk
                        Concatenated genbank of genome
  -rg genome.gbk, --ref_genbank genome.gbk
                        Concatenated genbank of genome
  -w WORKING_DIR, --working_dir WORKING_DIR
                        Folder to put intermediary files.
  -r, --reference       Look at changes to reference not query
  -n NUCDIFF, --nucdiff NUCDIFF
                        path to nucdiff.py
```

### progressiveChanges.py
Creates figure of cumulative changes to a genome over time. This is usefull for identifying lineages in an outbreak.

Takes a folder of gff files generated by getVar.py, all gffs should be created from the same reference.
Creates an svg of cumulative changes.

USAGE: python progressiveChanges.py <folder_of_gffs> <output.svg> <order_list>

<folder_of_gffs> a folder containing only the gffs to create figure from. All gffs should be generated from the same reference.

<output.svg> Where the svg of the figure will be created.

<order_list> order to arrange gffs in figure. Should contain a list of substrings unique to the name of the query genbank used to generate the gffs seperated by newlines.

### tableChanges.py
Tool for identifying genes under selective pressure. Creates a figure/table of recurrent mutations between strains.

USAGE: python tableChanges.py <folder_of_gffs> <output.svg> <order_list>

<folder_of_gffs> a folder containing only the gffs to create figure from.

<output.svg> Where the svg of the figure will be created.

<order_list> order to arrange gffs in figure. Should contain a list of substrings unique to the name of the query genbank used to generate the gffs seperated by newlines.



For the scripts used to generate the figures in the study "Colonizing and infecting subclones diverge during Staphylococcus aureus infection." please goto the mssa-paper branch. n.b. These scripts contain a lot of hardcoded information specific to the project and as should only be used to reproduce the initial study.
