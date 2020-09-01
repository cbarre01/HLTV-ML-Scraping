hltv <- read.csv("~/hltv/hltv.csv")

hltvRemainders$ID = seq.int(nrow(hltv))

hltvScores = hltv[,5:33]
hltvRemainders = hltv[0:4]


hltvScoresReducedT1 = hltvScores
hltvScoresReducedT2 = hltvScores
hltvScoresChar = data.frame(lapply(hltvScores, as.character), stringsAsFactors = FALSE)
hltvScoresReducedT1[] = lapply(hltvScoresChar,FUN = function(inCell) strsplit(inCell,"-")[[1]][1])
hltvScoresReducedT2[] = lapply(hltvScoresChar,FUN = function(inCell) strsplit(inCell,"-")[[2]][1])


colnames(hltvScoresReducedT1) = paste(colnames(hltvScoresReducedT1), "T1")
colnames(hltvScoresReducedT2) = paste(colnames(hltvScoresReducedT2), "T2")

hltvScoresReducedT1$ID = seq.int(nrow(hltv))
hltvScoresReducedT2$ID = seq.int(nrow(hltv))

cleaned = merge(hltvScoresReducedT1, hltvScoresReducedT2, by = "ID")
cleanedFull = merge(hltvRemainders, cleaned, by = "ID")
