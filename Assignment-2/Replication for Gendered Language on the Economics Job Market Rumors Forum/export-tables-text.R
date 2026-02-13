# ------------------------------------------------------------
# Export Tables 1 and 2 as text files (stargazer text output)
# ------------------------------------------------------------

# 1. Source the original tables/figures code
source("tables-figures.R")

# 2. Load stargazer
library(stargazer)

# 3. Export Table 1
capture.output(
  stargazer(tab1, type = "text", summary = FALSE),
  file = "Table1.txt"
)

# 4. Export Table 2
capture.output(
  stargazer(tab2, type = "text", summary = FALSE),
  file = "Table2.txt"
)