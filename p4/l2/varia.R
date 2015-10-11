# Remove column from dataframe
data(mtcars)
mtcars$year <- c(1973, 1974)
mtcars <- mtcars[,!names(mtcars) %in% c('year')]

# Clear workspace
rm(list = ls())