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

###########################################################################################
#                                                                                         #
#                                    USER-INTERFACE CODES                                 #
#                                                                                         #
###########################################################################################
# Define UI for application
ui <- dashboardPage(
  dashboardHeader(title = "R77 Utility Heatmap"),
  dashboardSidebar(
    sidebarMenu(
      menuItem(tabName = "heatmap", "Heatmap")
    )
  ),
  dashboardBody(
    tabItems(
      selected = 1,
      tabItem(
        tabName = "heatmap",
        fluidRow(
          column(width = 14,
              box(
                title = "R77 Real-Time Occupancy",
                color = "black", ribbon = FALSE, title_side = "top", collapsible = FALSE,
                plotOutput("heatmap")
              )
          )
        ),
        fluidRow(
          column(width = 14,
                 box(
                   title = "Meeting Room Headcount",
                   color = "black", ribbon = FALSE, title_side = "top", collapsible = FALSE,
                   valueBoxOutput("mrcount", width = 8)
                 )
          )
        )
      )
    )
  ), theme = "cosmo"
)