# stateData.csv
# subsetting
stateInfo <- read.csv("stateData.csv")
head(stateInfo)
str(stateInfo)
View(stateInfo)

subset(stateInfo, state.region == 1)
stateInfo[stateInfo$state.region == 1, ]

stateInfo[stateInfo$illiteracy <=  0.5, ]


# reddit.csv
getwd()
reddit <- read.csv('reddit.csv')
head(reddit)
summary(reddit)
str(reddit)

table(reddit$employment.status)

# figure out factors, possible values and plot it
levels(reddit$age.range)
library(ggplot2)
qplot(data = reddit, x = age.range)
# ... but we want to add some order to the factor, to see 'Under 18' before '18-24'
age.range.ordered = c("Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or Above")
reddit$age.range = factor(reddit$age.range, age.range.ordered, ordered=T)
qplot(data = reddit, x = age.range)

