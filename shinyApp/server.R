###########################################################################################
#                                                                                         #
#                                 IMPORTING LIBRARIES                                     #
#                                                                                         #
###########################################################################################

library(plotly)
library(shiny)
library(shiny.semantic)
library(semantic.dashboard)
library(ggplot2)
library(png)
library(ggpubr)
library(RPostgres)
library(DT)
library(dplyr)

###########################################################################################
#                                                                                         #
#                                 IMPORTING HEATMAP BG                                    #
#                                                                                         #
###########################################################################################
imgfile <- system.file(file.path("r77_base_comp.png"), package = "ggpubr")

img <- png::readPNG("r77_base_comp.png")

###########################################################################################
#                                                                                         #
#                                 CONNECT TO DATABASE                                     #
#                                                                                         #
###########################################################################################

# Database Connection 
db <- 'R77_OCCUPANCY'  #provide the name of your db
host_db <- '18.141.11.6'   
db_port <- '5432'  # or any other port specified by the DBA
db_user <- 'postgres'  
db_password <- 'iott1t5'

#Connecting PSQL DB
con <- dbConnect(RPostgres::Postgres(), dbname = db, host=host_db, port=db_port, user=db_user, password=db_password)

###########################################################################################
#                                                                                         #
#                                       SERVER CODES                                      #
#                                                                                         #
###########################################################################################
# Define server logic 
server <- function(input, output, session) {
  

  positions <- read.csv("r77_polygons_comb.csv")
  
  datapoly <- reactive({
    invalidateLater(5 * 1000, session)
    connection_sqlInput <- 'select ID,OccStatus from curr_occ'
    connection_data <- dbGetQuery(con, connection_sqlInput)
    connection_data$id <- as.character(connection_data$id)
    connection_data$occstatus <- as.factor(connection_data$occstatus)
    connection_data <- merge(connection_data,positions, by = c("id"))
    connection_data[
      order( connection_data[,1], connection_data[,5] ),
      ]
  })
  
  output$heatmap <- renderPlot({
    ggplot(datapoly(), aes(x = x, y = y,fill = occstatus), height = 800, width=1200) +
      xlim(0, 900)+
      ylim(0, 600)+
      background_image(img)+
      geom_polygon(aes(group = id),alpha=0.8) +
      theme(axis.title.x=element_blank(),
            axis.text.x=element_blank(),
            axis.ticks.x=element_blank(),
            axis.title.y=element_blank(),
            axis.text.y=element_blank(),
            axis.ticks.y=element_blank()) +
      scale_x_continuous(limits = c(0,900),expand = c(0, 0)) + 
      scale_y_continuous(limits = c(0,601),expand = c(0, 0)) +
      coord_equal() +
      scale_fill_manual(values = c("#D0E6A5", "#FFDD94", "#FA897B"),name= "Status", labels = c("Not In Use","Idle","In Use"))
  })
}