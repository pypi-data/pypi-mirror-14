# Usage: R --no-save --slave --args <FUNCTION_DIR> <PID> <SPECTRUM_SUMMARY_DIR> <REPEAT_THRESHOLD> <CONSECUTIVE_FLAG> <MAPQ> <BANDING_FILE> <PLOT_FILE_FORMAT> < plot_spectrum.R
# Description: Makes a bar plot for each chromosome. The chromosome bands are plotted on the x-axis and the specific telomere reads per million bases 
#              and per billion reads are plotted on the y-axis. Attention: the "junction bands" are not divided by band length (for these bands
#              the y-axis is "specific telomere reads per billion reads"), so the scaling is not correct in comparison to "normal" bands!!! 

# Copyright 2015 Lina Sieverling, Philip Ginsbach, Lars Feuerbach

# This file is part of TelomereHunter.

# TelomereHunter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# TelomereHunter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TelomereHunter.  If not, see <http://www.gnu.org/licenses/>.

# get commandline arguments
commandArgs = commandArgs()
pipeline_dir = commandArgs[5]
pid = commandArgs[6]
spectrum_dir = paste0(commandArgs[7], "/", pid, "/")
repeat_threshold = commandArgs[8]
consecutive_flag = commandArgs[9]
mapq_threshold = commandArgs[10]
banding_file = commandArgs[11]
plot_reverse_complement = commandArgs[12]
plot_file_format = commandArgs[13]


if (consecutive_flag == "True"){
  count_type = "Consecutive"
}else{
  count_type = "Non-consecutive"
}

if (plot_reverse_complement == "True"){
  plot_reverse_complement = TRUE
}else{
  plot_reverse_complement = FALSE
}

if (plot_file_format=="all"){
  plot_file_format=c("pdf", "png", "svg")
}

source(file.path(pipeline_dir, "/functions_for_plots.R"))

# get samples
spectrum_tumor_file = paste0(spectrum_dir, "/tumor_TelomerCnt_", pid,"/", pid, ".spectrum")
spectrum_control_file = paste0(spectrum_dir, "/control_TelomerCnt_", pid,"/", pid, ".spectrum")

samples = c()
if (file.exists(spectrum_tumor_file)){samples = c(samples, "tumor"); names(samples)[samples=="tumor"]="Tumor"}
if (file.exists(spectrum_control_file)){samples = c(samples, "control"); names(samples)[samples=="control"]="Control"}


# get band lengths
band_info = read.table(banding_file)
colnames(band_info) = c("chr", "start", "end", "band_name", "stain")
band_info[,"chr"] = gsub("chr", "", band_info[,1])
band_info[,"length"] = band_info[,"end"] - band_info[,"start"]

# get plot directory
plot_dir = file.path(spectrum_dir, "plots")
if (!(file.exists(plot_dir))){dir.create(plot_dir, recursive=TRUE)}



spectrum_list = list()

for (sample in samples){
  #get spectrum
  spectrum = read.table(paste0(spectrum_dir, "/",sample, "_TelomerCnt_", pid, "/", pid, ".spectrum"), header=TRUE, comment.char="")
 
  # get total number of reads 
  read_count_file = paste0(spectrum_dir, "/",sample, "_TelomerCnt_", pid, "/", pid, "_readcount.tsv")
  readcount = read.table(read_count_file, header=TRUE, comment.char="")
  total_reads = sum(as.numeric(readcount$reads))
    
  #normalize
  spectrum[ ,4:ncol(spectrum)] = spectrum[ ,4:ncol(spectrum)] * (spectrum$reads_with_pattern / apply(spectrum[ ,4:ncol(spectrum)], 1,sum))
  spectrum[ ,4:ncol(spectrum)] = spectrum[ ,4:ncol(spectrum)]*1000000000 / total_reads
  
  spectrum_list[[sample]] = spectrum
}
  
  
for (chr in c(1:22, "X", "Y")){
  
  spectrum_chr_list =list()
  
  for (sample in samples){
    spectrum = spectrum_list[[sample]]
    spectrum_chr = spectrum[spectrum$chr==chr,]
        
    #normalize by band length
    band_info_chr = band_info[band_info$chr==chr,]
    spectrum_chr[2:(nrow(spectrum_chr)-1),3:ncol(spectrum_chr)] = spectrum_chr[2:(nrow(spectrum_chr)-1),3:ncol(spectrum_chr)] *(1000000/ band_info_chr$length) 
    
    height = t(spectrum_chr[ ,4:ncol(spectrum_chr)])
    spectrum_chr_list[[sample]] = spectrum_chr
  }
  
  bands=spectrum_chr_list[[1]][ , "band"]
  
  if (length(samples)==2){
    height = zipFastener(t(spectrum_chr_list[["tumor"]][ ,4:ncol(spectrum_chr)]), t(spectrum_chr_list[["control"]][ ,4:ncol(spectrum_chr)]))
    sub_title = "Left: Tumor, Right: Control"
    axis=TRUE
    axis_simple=FALSE
  }else{
    height = t(spectrum_chr_list[[1]][ ,4:ncol(spectrum_chr)])
    sub_title = paste0(names(samples), " Sample")
    axis=FALSE
    axis_simple=TRUE
  }
  
  colnames(height)=NULL
  
  main = paste0(pid,": Telomere Repeat Types in Chr", chr)
  plot_file_prefix = paste0(plot_dir,"/", pid, "_", chr)
  
  barplot_repeattype(height=height,
                     plot_file_prefix=plot_file_prefix, plot_file_format=plot_file_format, width=28, mar=c(5.1, 5.1, 5.1, 9.3),
                     main=main, ylab="Normalized Number of Telomere Reads", #bands: Telomere Reads (per Million Bases and per Billion Reads), junctions: Telomere Reads (per Billion Reads)
                     plot_reverse_complement=plot_reverse_complement,
                     repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold,
                     inset_legend=c(-0.18,0),
                     axis=axis, axis_simple=axis_simple, labels=bands, cex.axis=0.75, cex.lab=0.9, sub_title=sub_title) 
}

  
  
  