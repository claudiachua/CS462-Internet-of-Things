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
monthMRData <- read.csv("monthMR.csv")

ui <- dashboardPage(
  dashboardHeader(title = "R77 Utility Dashboard"),
  dashboardSidebar(
    sidebarMenu(
      menuItem(tabName = "heatmap", "Heatmap"),
      menuItem(tabName = "hotdesk", "Hot Desk Utility"),
      menuItem(tabName = "meetingroom", "Meeting Room Utility")
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
                   title = "Real-Time Hot Desk Availability",
                   color = "black", ribbon = FALSE, title_side = "top", collapsible = FALSE,
                   div(style="display: inline-block; width: 220px; margin-left: 55px; margin-right: 35px; margin-bottom: 15px; margin-top: 15px",valueBoxOutput("rtHDfree", width = 4)),
                   div(style="display: inline-block; width: 220px; margin-right: 35px",valueBoxOutput("rtHDidle", width = 4)),
                   div(style="display: inline-block; width: 220px; margin-right: 35px",valueBoxOutput("rtHDused", width = 4))
                 )
          )
        ),
        fluidRow(
          column(width = 14,
              box(
                title = "Real-Time Occupancy",
                color = "black", ribbon = FALSE, title_side = "top", collapsible = FALSE,
                plotOutput("heatmap")
              )
          )
        ),
        fluidRow(
          column(width = 14,
                 box(
                   title = "Real-Time Meeting Room Headcount",
                   color = "black", ribbon = FALSE, title_side = "top", collapsible = FALSE,
                   div(style="display: inline-block; width: 170px; margin-left: 55px; margin-right: 35px; margin-bottom: 15px; margin-top: 15px",valueBoxOutput("Acount", width = 4)),
                   div(style="display: inline-block; width: 170px; margin-right: 35px",valueBoxOutput("Bcount", width = 4)),
                   div(style="display: inline-block; width: 170px; margin-right: 35px",valueBoxOutput("Ccount", width = 4)),
                   div(style="display: inline-block; width: 170px; margin-right: 35px",valueBoxOutput("Dcount", width = 4)),
                   div(style="display: inline-block; width: 170px; margin-left: 55px; margin-right: 35px",valueBoxOutput("Ecount", width = 4)),
                   div(style="display: inline-block; width: 170px; margin-right: 35px",valueBoxOutput("Fcount", width = 4)),
                   div(style="display: inline-block; width: 170px; margin-right: 35px",valueBoxOutput("Gcount", width = 4)),
                   div(style="display: inline-block; width: 170px; margin-right: 35px",valueBoxOutput("Hcount", width = 4))
                 )
          )
        )
      ),
      tabItem(
        tabName = "hotdesk",
        fluidRow(
          column(width = 14,
                 box(
                   title = "Daily Utility in the Last 30 Days",
                   color = "black", ribbon = FALSE, title_side = "top", collapsible = FALSE,
                   plotOutput("monthHD")
                 )
          )
        )
      ),
      tabItem(
        tabName = "meetingroom",
        fluidRow(
          column(width = 14,
          selectInput(inputId = "mr_selected", label = "Select Meeting Room:",
                      choices = levels(as.factor(monthMRData$id)), selected = "A"))
        ),
        fluidRow(
          column(width = 14,
          box(width = 16,
              title = "Daily Utility in the Last 30 Days",
              color = "black", ribbon = FALSE, title_side = "top", collapsible = FALSE,
              plotOutput("monthMR")))
        )
      )
    )
  ), theme = "cosmo"
)