# ----------------------------------
# Random Forest Table 1
# ----------------------------------

setwd("C:/Users/93672/Desktop/UW-MADISON/26 Spring/Econ 580/Replication/Wu-Gendered Language on the Economics Job Market Rumors Forum")

# load data
vocab      <- read.csv("vocab10K.csv", stringsAsFactors = FALSE)
i_keep     <- scan("i_keep_columns.txt")
importance <- scan("importance_rf_full.txt")

# LASSO coefficients (sign determines gender)
lasso_coef <- scan("coef_lasso_logit_full.txt")

# merge
vocab_rf <- vocab[match(i_keep + 1, vocab$index), ]
vocab_rf$importance <- importance

# align with LASSO length
n_lasso <- length(lasso_coef)
vocab_rf <- vocab_rf[1:n_lasso, ]
vocab_rf$lasso_coef <- lasso_coef


# split by gender
female <- vocab_rf[vocab_rf$lasso_coef <0, ]
male   <- vocab_rf[vocab_rf$lasso_coef >0, ]

# top 10 by RF importance
female_top <- female[order(-female$importance), ][1:10, c("word","importance")]
male_top   <- male[order(-male$importance),   ][1:10, c("word","importance")]

female_top$importance <- round(female_top$importance, 4)
male_top$importance   <- round(male_top$importance, 4)

# combine table
table1_rf <- data.frame(
  Most_Female = female_top$word,
  RF_Female   = female_top$importance,
  Most_Male   = male_top$word,
  RF_Male     = male_top$importance
)

# -------------------------------
# Export LaTeX
# -------------------------------
tex <- c(
  "\\begin{table}[ht]",
  "\\centering",
  "\\caption{Most Important Words by Gender (Random Forest)}",
  "\\begin{tabular}{l c l c}",
  "\\hline",
  "Most Female & RF Importance & Most Male & RF Importance \\\\",
  "\\hline",
  apply(table1_rf, 1, function(x)
    paste(x[1], "&", x[2], "&", x[3], "&", x[4], "\\\\")
  ),
  "\\hline",
  "\\end{tabular}",
  "\\end{table}"
)

writeLines(tex, "table1_rf.tex")

# -------------------------------
# Export text
# -------------------------------
txt <- c(
  "Table 1. Most Important Words by Gender (Random Forest)",
  "",
  sprintf("%-18s %-10s %-18s %-10s", "Most Female","RF","Most Male","RF"),
  paste(rep("-", 60), collapse = ""),
  apply(table1_rf, 1, function(x)
    sprintf("%-18s %-10s %-18s %-10s", x[1], x[2], x[3], x[4])
  )
)

writeLines(txt, "table1_rf.txt")

cat("Saved: table1_rf.tex and table1_rf.txt\n")



               




