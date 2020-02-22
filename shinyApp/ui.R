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
###########################################################################################
#                                                                                         #
#                                    USER-INTERFACE CODES                                 #
#                                                                                         #
###########################################################################################
# Define UI for application
ui <- dashboardPage(
  dashboardHeader(title = "R77 Utility Heatmap", inverted = TRUE),
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
          column(width = 16,
              title = "R77 Real-Time Occupancy",
              color = "black", ribbon = FALSE, title_side = "top", collapsible = FALSE,
              plotOutput("heatmap"))
        )
      )
    )
  ), theme = "cosmo"
)