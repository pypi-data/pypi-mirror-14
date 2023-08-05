# Usage: R --no-save --slave --args <PID> <SPECTRUM_SUMMARY_DIR> <REPEAT_THRESHOLD> <CONSECUTIVE_FLAG> <MAPQ> <T_TYPE> <C_TYPE> <G_TYPE> <J_TYPE> <PLOT_FILE_FORMAT> < plot_repeat_frequency_intratelomeric.R
# Description: Makes a histograms of the telomere repeats per intratelomeric read in the tumor and control sample

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
pid = commandArgs[5]
spectrum_dir = paste(commandArgs[6], "/", pid, "/", sep="")
repeat_threshold = commandArgs[7]
consecutive_flag = commandArgs[8]
mapq_threshold = commandArgs[9]
repeat_types = commandArgs[10]
plot_file_format = commandArgs[11]

library(ggplot2)
library(grid)
library(gridExtra)

if (consecutive_flag == "True"){
  count_type = "consecutive"
}else{
  count_type = "non-consecutive"
}

if (plot_file_format=="all"){
  plot_file_format=c("pdf", "png", "svg")
}


frequency_table_file_T = paste0(spectrum_dir, "/tumor_TelomerCnt_", pid, "/", pid, "_repeat_frequency_per_intratelomeric_read.tsv")


colors = c() 

if (file.exists(frequency_table_file_T)){
  colors = c(colors, "maroon2") 
  frequency_table_T = read.table(frequency_table_file_T, header=TRUE)
  frequency_table_T$sample="Tumor"
  frequency_table_T$percent = frequency_table_T$count / sum(frequency_table_T$count) * 100
  frequency_table_T$percent_cumulative = cumsum(frequency_table_T$percent)
  #frequency_table_T$percent_cumulative = rev(cumsum(rev(frequency_table_T$percent)))
}else{
  frequency_table_T = matrix(, nrow = 0, ncol = 5)
}


frequency_table_file_C = paste0(spectrum_dir, "/control_TelomerCnt_", pid, "/", pid, "_repeat_frequency_per_intratelomeric_read.tsv")

if (file.exists(frequency_table_file_C)){
  colors = c(colors, "turquoise3") 
  frequency_table_C = read.table(frequency_table_file_C, header=TRUE)
  frequency_table_C$sample="Control"
  frequency_table_C$percent = frequency_table_C$count / sum(frequency_table_C$count) * 100
  frequency_table_C$percent_cumulative = cumsum(frequency_table_C$percent)
  #frequency_table_C$percent_cumulative = rev(cumsum(rev(frequency_table_C$percent)))
}else{
  frequency_table_C = matrix(, nrow = 0, ncol = 5)
}


df = data.frame(rbind(as.matrix(frequency_table_T),as.matrix(frequency_table_C)))
df$sample = factor(df$sample, levels=c("Tumor", "Control"))
df$number_repeats = as.numeric(levels(df$number_repeats))[df$number_repeats]
df$percent = as.numeric(levels(df$percent))[df$percent]
df$percent_cumulative = as.numeric(levels(df$percent_cumulative))[df$percent_cumulative]

if (nchar(repeat_types) < 43){
  filtering_criteria = paste0("Filtering Criteria: ",
                              repeat_threshold, " ", count_type, " repeats",
                              ", mapq threshold = ", mapq_threshold,
                              ", repeat types = ", repeat_types)
}else{
  filtering_criteria = paste0("Filtering Criteria: ",
                              repeat_threshold, " ", count_type, " repeats",
                              ", mapq threshold = ", mapq_threshold,
                              "\nrepeat types = ", repeat_types)
}


plot_dir= paste0(spectrum_dir, "plots/")

if (!(file.exists(plot_dir))){
  dir.create(plot_dir, recursive=TRUE)
}



plot_file = paste0(plot_dir, pid, "_hist_telomere_repeats_per_intratelomeric_read")

for (plot_type in plot_file_format){
  
  if (plot_type=="png"){png(paste0(plot_file,".png"), width=30, height=25, units="cm", res=300)}     
  if (plot_type=="pdf"){pdf(paste0(plot_file,".pdf"), width=30*0.4, height=25*0.4)}
  if (plot_type=="svg"){svg(paste0(plot_file, ".svg"), width=30/2.56, height=25/2.56)}
  
  # make histogram
  p_hist = ggplot(df, aes(x=number_repeats, y=percent)) +
    geom_bar(stat = "identity") +
    facet_wrap(~ sample) +
    theme(plot.title = element_text(face="bold")) +
    xlab("Number of Repeats") +
    ylab("Percent of Intratelomeric Reads")

  p_hist_text = arrangeGrob(p_hist, sub = textGrob(filtering_criteria, vjust=0, gp = gpar(fontsize = 12)), heights=c(0.9, 0.1))
  
  
  #make cumulative line plot
  p_cum = ggplot(df, aes(x=number_repeats, y=percent_cumulative, group=sample)) +
    geom_line(aes(colour = sample)) +
    ggtitle(paste0(pid, ": Frequency of Telomere Repeat Occurrences in Intratelomeric Reads")) +
    theme(plot.title = element_text(face="bold")) +
    scale_color_manual(values=colors) +
    theme(legend.title=element_blank()) +
    #theme(legend.position="top") +
    theme(legend.justification=c(0,-2.3), legend.position=c(0,0)) +
    xlab("Number of Repeats") +
    ylab("Percent (Cumulative)")
  
  final_plot=arrangeGrob(p_cum, p_hist_text, ncol=1, heights=c(0.4, 0.6))
    
  grid::grid.draw(final_plot)   #prevent blank page in pdf file
  
  invisible(dev.off())
}





