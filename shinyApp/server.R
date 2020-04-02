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
  
  mr_count <- reactive({
    invalidateLater(2 * 1000, session)
    connection_sqlInput <- 'select count from mr_count_hist order by mrcounttimestamp desc limit 1'
    connection_data <- dbGetQuery(con, connection_sqlInput)
  })
  
  output$Acount <- renderValueBox({
    valueBox(
      value = 6,
      subtitle = "Meeting Room A",
      color = "black",
      size = "tiny"
    )
  })
  
  output$Bcount <- renderValueBox({
    valueBox(
      value = 0,
      subtitle = "Meeting Room B",
      color = "black",
      size = "tiny"
    )
  })
  
  output$Ccount <- renderValueBox({
    valueBox(
      value = 3,
      subtitle = "Meeting Room C",
      color = "black",
      size = "tiny"
    )
  })
  
  output$Dcount <- renderValueBox({
    valueBox(
      value = 0,
      subtitle = "Meeting Room D",
      color = "black",
      size = "tiny"
    )
  })
  
  output$Ecount <- renderValueBox({
    valueBox(
      value = mr_count(),
      subtitle = "Meeting Room E",
      color = "black",
      size = "tiny"
    )
  })
  
  output$Fcount <- renderValueBox({
    valueBox(
      value = 0,
      subtitle = "Meeting Room F",
      color = "black",
      size = "tiny"
    )
  })
  
  output$Gcount <- renderValueBox({
    valueBox(
      value = 0,
      subtitle = "Meeting Room G",
      color = "black",
      size = "tiny"
    )
  })
  
  output$Hcount <- renderValueBox({
    valueBox(
      value = 0,
      subtitle = "Meeting Room H",
      color = "black",
      size = "tiny"
    )
  })
  
  output$Fcount <- renderValueBox({
    valueBox(
      value = 0,
      subtitle = "Meeting Room F",
      color = "black",
      size = "tiny"
    )
  })
  
  output$Gcount <- renderValueBox({
    valueBox(
      value = 0,
      subtitle = "Meeting Room G",
      color = "black",
      size = "tiny"
    )
  })
  
  hd4_status <- reactive({
    invalidateLater(2 * 1000, session)
    connection_sqlInput <- "select occstatus from hd_occ_hist where hotdeskid = '4' order by hdocctimestamp desc limit 1"
    connection_data <- dbGetQuery(con, connection_sqlInput)
  })
  
  hd5_status <- reactive({
    invalidateLater(2 * 1000, session)
    connection_sqlInput <- "select occstatus from hd_occ_hist where hotdeskid = '5' order by hdocctimestamp desc limit 1"
    connection_data <- dbGetQuery(con, connection_sqlInput)
  })
  
  hdfree <- reactive({
    free <- 0
    
    if(hd4_status()==0){
      free <- free + 1
    }
    
    if(hd5_status()==0){
      free <- free + 1
    }
  })
  
  hdidle <- reactive({
    idle <- 0
    
    if(hd4_status()==1){
      idle <- idle + 1
    }
    
    if(hd5_status()==1){
      idle <- idle + 1
    }
  })

  hdused <- reactive({
    used <- 0
    
    if(hd4_status()==2){
      used <- used + 1
    }
    
    if(hd5_status()==2){
      used <- used + 1
    }
  })
  
  output$rtHDfree <- renderValueBox({
    valueBox(
      value = 8,# + hdfree(),
      subtitle = "Not In Use",
      color = "green",
      size = "tiny"
    )
  })
  
  output$rtHDidle <- renderValueBox({
    valueBox(
      value = 3,# + hdidle(),
      subtitle = "Idle",
      color = "yellow",
      size = "tiny"
    )
  })
  
  output$rtHDused <- renderValueBox({
    valueBox(
      value = 13,# + hdused(),
      subtitle = "In Use",
      color = "red",
      size = "tiny"
    )
  })
  
  monthHDData <- read.csv("monthHD.csv")
  output$monthHD <- renderPlot({
    ggplot(data=monthHDData, aes(x=Day, y=Occupancy)) +
      geom_hline(yintercept = 70, aes(colour="blue")) +
      geom_line() +
      geom_point()
  })
  
  monthMRData <- read.csv("monthMR.csv")
  mr_selected_data <- reactive({
    monthMRData %>%
      filter(id == input$mr_selected)
  })
  
  output$monthMR <- renderPlot({
    ggplot(data=mr_selected_data(), aes(x=day, y=hours)) +
      geom_line() +
      geom_point() +
      ylim(low=0,high=10)
  })
}