###########################################################################################
#                                                                                         #
#                                 IMPORTING LIBRARIES                                     #
#                                                                                         #
###########################################################################################

packages = c('plotly','shiny','shiny.semantic',
             'semantic.dashboard','ggplot2','png','ggpubr')

for (p in packages){
  if(!require(p, character.only = T)){
    install.packages(p)
  }
  library(p,character.only = T)
}

imgfile <- system.file(file.path("r77_base_comp.png"), package = "ggpubr")

img <- png::readPNG("r77_base_comp.png")

ids <- factor(c("A","B","C","D","E","F","G","H","1","2","3","4","5","6","7","8"))

values <- data.frame(
  id = ids,
  value = c("X","X","O","X","O","X","X","X","X","O","X","O","O","X","X","X")
)

positions <- read.csv("r77_polygons_comb.csv")

datapoly <- merge(values, positions, by = c("id"))

###########################################################################################
#                                                                                         #
#                                       SERVER CODES                                      #
#                                                                                         #
###########################################################################################
# Define server logic 
server <- function(input, output, session) {
  
  output$heatmap <- renderPlot({
    ggplot(datapoly, aes(x = x, y = y), height = 800, width=1200) +
      xlim(0, 900)+
      ylim(0, 600)+
      background_image(img)+
      geom_polygon(aes(fill = value, group = id),alpha=0.5) +
      theme(axis.title.x=element_blank(),
            axis.text.x=element_blank(),
            axis.ticks.x=element_blank(),
            axis.title.y=element_blank(),
            axis.text.y=element_blank(),
            axis.ticks.y=element_blank()) +
      scale_x_continuous(limits = c(0,900),expand = c(0, 0)) + 
      scale_y_continuous(limits = c(0,601),expand = c(0, 0)) +
      coord_equal()
  })
}