==============
TelomereHunter
==============

TelomereHunter is a tool for estimating telomere content from human whole-genome sequencing data. It is designed to take BAM files from a tumor and a matching control sample as input. However, it is also possible to run TelomereHunter with one input file.

TelomereHunter extracts and sorts telomeric reads from the input sample(s). For the estimation of telomere content, GC biases are taken into account. Finally, the results of TelomereHunter are visualized in several diagrams.

The individual steps of the tool are explained in more detail in the following sections.

Usage: telomerehunter -ibt TUMOR_BAM -ibc CONTROL_BAM -o OUTPUT_DIRECTORY -p PID [options]

All possible TelomereHunter options can be found using the -h/--help option.


---------------------------
Filtering of telomere reads
---------------------------
From each input sample, all reads containing a specified number of telomeric repeats are extracted. Besides the number of telomeric repeats, the user can also specify whether the repeats should be consecutive or non-consecutive (default: non-consecutive) and which hexameric repeat types to search for (default:TTAGGG, TCAGGG, TGAGGG and TTGGGG). Using default filtering criteria, TelomereHunter searches for all four telomeric repeat types and the number of repeats is calculated depending on the read length with the following formula: floor(read_length*0.06).

Secondary and supplementary alignments in the BAM file are not extracted. If the -d/--removeDuplicates option is specified, reads marked as duplicates are also not extracted. All extracted telomere reads are written into an indexed BAM file (\*_filtered.bam). This BAM file is additionally sorted by read names (\*_filtered_name_sorted.bam).

For each telomeric and non-telomeric read, the chromosome and band to which it was mapped are retrieved. Reads aligned to sequences other than autosomes or allosomes, or reads with a mapping quality lower than a specified threshold (default: 8) are considered unmapped. This information is used to generate a text file containing a table with the total number of reads mapped to each chromosome band and the total number of unmapped reads (\*_readcount.tsv).

During the filtering step, the GC content of each read is determined if the amount of Ns in the read sequence is less than or equal to 20%. A table with the total number of reads for each possible GC content is generated (\*_gc_content.tsv).

Because the filtering of telomere reads is the most time-consuming step of TelomereHunter, the user is asked whether he wants to run this step again if the output files already exist. If the answer is no, the filtering step will be skipped and TelomereHunter will start with the sorting step. Alternatively, the user can set the -nf/--noFiltering option. In this case, the filtering step is only run if the output files don't already exist. Setting this option is recommended when automatically (re-)submitting TelomereHunter jobs, because it does not require a user input.


-------------------------
Sorting of telomere reads
-------------------------
The extracted telomere reads from the filtering step are sorted into four different fractions depending on their mapping position. If the input is paired-end sequencing data and both mates have been extracted as telomere reads, the mapping position of the mate is also taken into account for the sorting.

If both mates are considered unmapped, i.e. they have a mapping quality below the specified threshold, they are sorted into the intratelomeric fraction. The junction spanning group comprises pairs in which one mate is unmapped and the other is mapped to the first or last band of a chromosome. Subtelomeric reads are those in which both mates are aligned to a first or last chromosome band. Reads are defined as intrachromosomal if at least one mate is mapped to a band that is not the first or last band of a chromosome.

Single-end reads or paired-end reads whose mates are not considered to be telomeric are sorted into the intratelomeric, subtelomeric or intrachromosomal fraction depending only on their mapping position.

For each of the four sorting fractions, a BAM file containing the telomere reads of the group is generated (\*_filtered_intratelomeric.bam, \*_filtered_junctionspanning.bam, \*_filtered_subtelomeric.bam, \*_filtered_intrachromosomal.bam). Furthermore, the number of telomere reads in each chromosome band and the number of junction spanning telomere reads at each chromosome end can be obtained from an output table called \*.spectrum. The occurrences of the searched telomere repeat types in the telomere reads of every band are also presented in this table.


---------------------------
Estimating telomere content
---------------------------
To account for different library sizes and GC biases, the telomere content of a sample is estimated from the number of intratelomeric reads normalized by the total number of reads with a GC composition similar to that of telomeres. Because the GC content of the generic t-type repeat is 50%, the default GC content used for the normalization is 48-52%. However, the user can also define other limits for the GC correction using the options -gc1/--lowerGC and -gc2/--upperGC. 

The results of the telomere content estimation can be found in the output \*_summary.tsv file. The telomere content estimated by TelomereHunter is the number of intratelomeric reads per million reads with telomeric gc content:

tel_content = intratel_reads * 1,000,000 / total_reads_with_tel_gc



---------------------------------------
Visualization of TelomereHunter results
---------------------------------------
The results of TelomereHunter are summarized in several different diagrams:

- Bar plots for each chromosome showing the number of telomere reads mapped to each band normalized by band length in bases and the total number of reads in the sample:

  telomere_reads_band * 1,000,000/band_length * 1,000,000,000/total number of reads

  Junction spanning reads shown in these plots are only normalised by the total number of reads:

  telomere_reads_junction * 1,000,000,000/total number of reads

- Bar plot summarizing the number of telomere reads (per million total reads) in each of the four telomere read fractions.

- Bar plot showing the gc corrected telomere content of the analyzed samples.

In all bar plots mentioned above, the relative occurrences of the searched telomere repeat types are represented as stacks. If the -prc/--plotRevCompl option is set, TelomereHunter distinguishes between forward and reverse repeats as seen in the BAM file. Please note that reads aligned to the reverse strand may already be reverse complemented by the alignment tool and can therefore lead to confounding results in the barplot.


- Diagram with the GC content distribution in all reads (top) and in intratelomeric reads (bottom). The GC bins used for the GC correction in the telomere content estimation are highlighted.

- Histograms of repeat frequencies per intratelomeric read in each sample. Above the histograms, the cumulative percentage of reads containing each possible number of telomere repeats is shown.

Using default settings, all of the diagrams are generated in pdf format. However, the user can also specify which specific diagrams to generate and whether these should be in png, svg and/or pdf format.

To generate the diagrams, TelomereHunter requires R with the following libraries: ggplot2, reshape2, grid, gridExtra, RColorBrewer. If it is not possible or you do not wish to install this on your computer, please use the option -p6/--plotNone.

|
|

Contact Lina Sieverling (l.sieverling@dkfz-heidelberg.de) for questions and support on TelomereHunter.