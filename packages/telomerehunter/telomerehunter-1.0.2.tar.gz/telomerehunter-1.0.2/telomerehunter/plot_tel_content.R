# Usage: R --no-save --slave --args <FUNCTION_DIR> <PID> <SPECTRUM_SUMMARY_DIR> <REPEAT_THRESHOLD> <CONSECUTIVE_FLAG> <MAPQ> <PLOT_FILE_FORMAT> <GC_LOWER_LIMIT> <GC_UPPER_LIMIT> < plot_tel_content.R
# Description: makes a bar plot of the number of intratelomeric reads (per million reads) in the tumor and control sample.

# Copyright 2015 Lina Sieverling

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
plot_reverse_complement = commandArgs[11]
plot_file_format = commandArgs[12]
gc_lower_limit = as.numeric(commandArgs[13])
gc_upper_limit = as.numeric(commandArgs[14])


source(file.path(pipeline_dir, "/functions_for_plots.R"))

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


spectrum_tumor_file = paste0(spectrum_dir, "/tumor_TelomerCnt_", pid,"/", pid, ".spectrum")
spectrum_control_file = paste0(spectrum_dir, "/control_TelomerCnt_", pid,"/", pid, ".spectrum")

samples = c()
if (file.exists(spectrum_tumor_file)){samples = c(samples, "tumor"); names(samples)[samples=="tumor"]="Tumor"}
if (file.exists(spectrum_control_file)){samples = c(samples, "control"); names(samples)[samples=="control"]="Control"}

heights_samples_list = list()
for (sample in samples){
  #get spectrum
  spectrum = read.table(paste0(spectrum_dir, "/", sample, "_TelomerCnt_", pid,"/", pid, ".spectrum"), header=TRUE, comment.char="")
  spectrum = spectrum[spectrum$chr=="unmapped",]
  
  #get gc corrected telomere content
  summary = read.table(paste0(spectrum_dir, "/", sample, "_TelomerCnt_", pid,"/", pid, "_", sample, "_summary.tsv"), header=TRUE, sep="\t")
  tel_content = summary$tel_content
  
  #get relative telomere repeat type occurrences in telomere content
  spectrum[ ,4:ncol(spectrum)] = spectrum[ ,4:ncol(spectrum)] / sum(spectrum[ ,4:ncol(spectrum)]) * tel_content
  
  height = t(spectrum[ ,4:ncol(spectrum)])
  colnames(height) = names(samples)[samples==sample]
  
  heights_samples_list[[sample]] = height
}

if (length(samples)==2){
  height = cbind(heights_samples_list[[1]], heights_samples_list[[2]])
}else{
  height = heights_samples_list[[1]]
}


plot_dir = file.path(spectrum_dir, "plots")
if (!(file.exists(plot_dir))){dir.create(plot_dir, recursive=TRUE)}

plot_file_prefix = paste0(plot_dir,"/", pid, "_telomere_content")

barplot_repeattype(height=height,
                   width=14,
                   plot_file_prefix=plot_file_prefix,
                   plot_file_format=plot_file_format, 
                   main=paste0(pid,": GC Corrected Telomere Content"),
                   ylab=paste0("Telomere Content\n(Intratelomeric Reads per Million Reads with GC Content of ", gc_lower_limit, "-", gc_upper_limit, "%)"),
                   plot_reverse_complement=plot_reverse_complement,
                   cex.main=1,
                   repeat_threshold=repeat_threshold, count_type=count_type, mapq_threshold=mapq_threshold, 
                   axis=FALSE, axis_simple=TRUE, xlas=1, tick=FALSE, cex.axis=0.85, cex.lab=0.9, inset_legend=c(-0.63,0), cex.names=0.9) 

