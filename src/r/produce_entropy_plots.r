library(pacman)
p_load(dplyr, magrittr, stringr, stringi, tidyr, ggplot2, readr)
args = commandArgs(trailingOnly = T)
if(length(args) != 1) {
  stop("This script requires one argument!")
}
ent_tb <- read_csv(paste0(args[1], "\\py_outputs\\phonological_entropy.csv"))
# STEP 1: CREATE POSITIONAL ENTROPY PLOT
label_names <- vector()
for (i in 1:length(ent_tb$entropy)) {
  labl <- ent_tb$syl[i] %>% strsplit("_") %>% unlist()
  if(labl[1] == "final") {
    label_names[i] <- paste0("Syllable ", labl[1], " ", labl[2])
  }else {
    label_names[i] <- paste0("Syllable ",as.numeric(labl[1]) + 1, " ", labl[2])
  }
}

ent_tb <- ent_tb %>% mutate(label_names = label_names)
ent_tb <- ent_tb[!grepl("final coda", ent_tb$label_names),]
ent_gg <- ggplot(ent_tb, aes(x = label_names, y = entropy)) + 
  geom_histogram(stat = "identity") + 
  theme(text = element_text(size=10),
  axis.text.x = element_text(angle=90, hjust=1))  + 
  scale_x_discrete(limits = ent_tb$label_names) + 
  xlab("Syllable") + 
  ylab("Shannon Entropy")
ggsave(paste0(args[1], "\\r_plots\\shannon_entropy.png"))
# save ent_tb
write_csv(ent_tb, paste0(args[1], "\\r_tables\\entropy_tab.csv"))

# STEP 2: CREATE WORD SURPRISAL PLOTS
sur_tab <- readr::read_csv(paste0(args[1], "\\py_outputs\\lexical_surprisals.csv"))
sur_tab$phoneme <- sur_tab$phoneme
sur_tab<- sur_tab %>% mutate(vowel_count = stri_count_regex(phoneme, "[\u0250\u0259iIuU]"),
                             vowel_initial = grepl("^[\u0250\u0259iIuU]", phoneme))
cat <- vector()
for(i in 1:length(sur_tab$phoneme)) {
  cat <- c(cat, paste0(sur_tab$vowel_initial[i], sur_tab$vowel_count[i], collapse = "_"))
}
cat <- cat %>% stri_replace_all_fixed("TRUE", "V_") %>% stri_replace_all_fixed("FALSE", "C_")
sur_tab <- sur_tab %>% mutate(cat=cat)

cats <- cat %>% unique()
mean_surp <- vector()
for(categ in cats) {
  mean_surp <- c(mean_surp, mean(sur_tab$mean_surprisal[sur_tab$cat == categ]))
}

out_tab <- cbind(cats, mean_surp) %>% data.frame(stringsAsFactors = F)
out_tab$mean_surp <- as.numeric(out_tab$mean_surp) %>% round(digits = 4)

# calculate difference from grand mean
out_tab <- out_tab %>% mutate(mean_diff = mean_surp - mean(mean_surp))
std_devs <- vector()
for(i in 1:length(out_tab$cats)) {
  std_devs <- c(std_devs, sd(sur_tab$mean_surprisal[sur_tab$cat == out_tab$cats[i]]))
}
out_tab <- out_tab %>% mutate(std_dev = std_devs)

sur_dens <- ggplot(sur_tab, aes(x = mean_surprisal)) + geom_density(alpha = 0.5)
ggsave(paste0(args[1], "\\r_plots\\surprisal_density_plot.png"))

sur_hist <- ggplot(out_tab, aes(x = cats, y = mean_surp)) + geom_histogram(stat='identity') +xlab("Category") + ylab("Mean Surprisal")
ggsave(paste0(args[1], "\\r_plots\\surprisal_by_category.png"))
# save surprisal tab
write_csv(out_tab, paste0(args[1], "\\r_tables\\surprisal_categories.csv"))
# save categories for each lexeme
write_csv(sur_tab, paste0(args[1], "\\r_tables\\lexemes_by_category.csv"))

# STEP 3ː Create frequency table of different categories, with sum entropy
cat_tab <- sur_tab$cat %>% table() %>% data.frame(stringsAsFactors = F)
tab_cats <- levels(droplevels(cat_tab$.))

#create numeric ent_tb col
syl_nums <- vector()
for(syl in ent_tb$syl) {
  syl_split <- syl %>% strsplit("_") %>% unlist()
  if(syl_split[1] == "final") {
    syl_nums <- c(syl_nums, 100) #assign 100 to ensure it is never accidentally captured
  } else {
    syl_nums <- c(syl_nums, as.numeric(syl_split[1]))
  }
}
ent_tb <- ent_tb %>% mutate(syl_num = syl_nums)
highest_num <- sort(syl_nums,partial=length(syl_nums)-1)[length(syl_nums)-1]

# produce sum entropy
entropy_col <- vector()
for (cat in tab_cats) {
  # get number of syllables in word
  cat_split <- cat %>% strsplit("_") %>% unlist()
  cat_num <- cat_split[2] %>% as.numeric()
  
  this_ent_tb <- ent_tb[ent_tb$syl_num < cat_num,]
  # remove last two rows and add final_nucleus. Unless
  # cat_num is equal to the highest number excluding 100
  row_num <- dim(this_ent_tb)[1]
  if (cat_num == highest_num) {
    this_ent_tb <- this_ent_tb[1:row_num-1,]
    this_ent_tb <- rbind(this_ent_tb, ent_tb[grepl("final", ent_tb$syl),])
  } else {
    this_ent_tb <- this_ent_tb[1:(row_num-2),]     
    this_ent_tb <- rbind(this_ent_tb, ent_tb[grepl("final", ent_tb$syl),])
  }
  entropy_col <- c(entropy_col, sum(this_ent_tb$entropy))
}
cat_tab <- cat_tab %>% mutate(sum_entropy = entropy_col)

# create plot with unique vowel count values
vowel_counts <- vector()
for (cat in tab_cats) {
  cat_split <- cat %>% strsplit("_") %>% unlist()
  vowel_counts <- c(vowel_counts, as.numeric(cat_split[2]))
}
vc_tab <- cbind(vowel_counts, cat_tab$sum_entropy) %>% data.frame()
vc_tab <- vc_tab[!duplicated(vc_tab),]
vc_tab$vowel_counts <- paste0(vc_tab$vowel_counts, " Vowels")
vc_tab$vowel_counts[1] <- vc_tab$vowel_counts[1] %>% stri_replace_all_regex("s$", "")

ent_gg <- ggplot(vc_tab, aes(x = vowel_counts, y = V2)) + 
  geom_histogram(stat = "identity") + 
  theme(text = element_text(size=10),
  axis.text.x = element_text(angle=90, hjust=1))  + 
  scale_x_discrete(limits = vc_tab$vowel_counts) + 
  xlab("Syllable") + 
  ylab("Shannon Entropy")
ggsave(paste0(args[1], "\\r_plots\\vowel_count_entropy.png"))
write_csv(cat_tab, paste0(args[1], "\\r_tables\\category_frequencies.csv"))
          
