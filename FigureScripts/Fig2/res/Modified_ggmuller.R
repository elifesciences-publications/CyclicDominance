library(ggmuller)
library(ggplot2)
library(dplyr)

#get file index argument
#args <- commandArgs(TRUE)
#fidx <- args[1]
fidx = "1"


#read files
fname <- paste("pop", fidx, "_t.d", sep="")
pop = read.table(fname)
names(pop)[1]<-paste("Generation")
names(pop)[2]<-paste("Identity")
names(pop)[3]<-paste("Population")


fname <- paste("tree", fidx, ".d", sep="")
tree = read.table(fname)
names(tree)[1]<-paste("Parent")
names(tree)[2]<-paste("Identity")


#new codes 
Muller_plot2 <- function(Muller_df, colour_by = "Identity", palette = NA, add_legend = FALSE, xlab = NA, ylab = "Frequency", pop_plot = FALSE) {
  if(!pop_plot & "___special_empty" %in% Muller_df$Group_id) warning("Dataframe is set up for Muller_pop_plot. Use Muller_pop_plot to plot populations rather than frequencies.")
  
  y_factor <- ifelse(pop_plot, "Population", "Frequency")
  if("Time" %in% colnames(Muller_df) && !("Generation" %in% colnames(Muller_df))) x_factor <- "Time"
  else x_factor <- "Generation"
  if(is.na(xlab)) xlab <- x_factor
  direction <- 1
  if(is.na(palette[1])) {
    if(is.numeric(Muller_df[ , colour_by])) {
      palette <- "RdBu"
      direction <- -1
    }
    else {
      long_palette <- c("#8A7C64", "#599861", "#89C5DA", "#DA5724", "#74D944", "#CE50CA", 
                        "#3F4921", "#C0717C", "#CBD588", "#5F7FC7", "#673770", "#D3D93E", 
                        "#38333E", "#508578", "#D7C1B1", "#689030", "#AD6F3B", "#CD9BCD", 
                        "#D14285", "#6DDE88", "#652926", "#7FDCC0", "#C84248", "#8569D5", 
                        "#5E738F", "#D1A33D")
      palette <- rep(long_palette, ceiling(length(unique(Muller_df$Identity)) / length(long_palette)))
    }
  }
  # test whether palette is a vector of colours; if not then we'll assume it's the name of a predefined palette:
  palette_named <- !min(sapply(palette, function(X) tryCatch(is.matrix(col2rgb(X)), error = function(e) FALSE)))
  
  gg <- ggplot(Muller_df, aes_string(x = x_factor, y = y_factor, group = "Group_id", fill = colour_by)) + 
    geom_area() +
    theme(legend.position = ifelse(add_legend, "right", "none")) +
    guides(linetype = FALSE, color = FALSE) + 
    scale_x_continuous(name = xlab) + 
    scale_y_continuous(name = ylab)
  
  if(is.numeric(Muller_df[ , colour_by])) {
    gg <- gg + 
      scale_fill_distiller(palette = palette, direction = direction, name = colour_by) + 
      scale_color_distiller(palette = palette, direction = direction)
  }
  else {
    if(palette_named) {
      gg <- gg + 
        scale_fill_brewer(palette = palette, name = colour_by) + 
        scale_color_brewer(palette = palette)
    }
    else {
      id_list <- sort(unique(select(Muller_df, colour_by))[[1]]) # list of legend entries, omitting NA
      gg <- gg + 
        scale_fill_manual(values = palette, name = colour_by, breaks = id_list) + 
        scale_color_manual(values = palette)
    }
  }
  return(gg)
}

Muller_pop_plot2 <- function(Muller_df, colour_by = "Identity", palette = NA, add_legend = FALSE, xlab = NA, ylab = "Population") {
  
  # add rows for empty space (unless this has been done already):
  if(!"___special_empty" %in% Muller_df$Group_id) Muller_df <- add_empty_pop(Muller_df)
  
  Muller_plot2(Muller_df, colour_by = colour_by, palette = palette, add_legend = add_legend, pop_plot = TRUE, xlab = xlab, ylab = ylab)
}




#making ggmuller
Muller_df <- get_Muller_df(tree, pop)
#Muller_plot2(Muller_df)
Muller_pop_plot2(Muller_df)
