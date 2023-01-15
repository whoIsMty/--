rm(list = ls())
wd <- "C:\\Users\\leois\\Desktop\\nkdaxue\\data"
all_data <- list()
for (d in 1:3) {
    path <- paste0(wd, "\\", d, ".txt")
    all_data[[length(all_data) + 1]] <- read.delim2(path, sep = "\t", header = TRUE, ) # nolint
}
groups <- levels(factor(all_data[[1]][, 1]))

all_category <- c()
for (i in seq_len(3)) {
    df <- all_data[[i]]
    second_category <- df[, 2]
    all_category <- c(all_category, sort(unique(second_category)))
}
all_category <- sort(unique(all_category))
dd <- list()

# 
for (i in seq_len(3)) {
    df <- all_data[[i]]
    second_category <- df[, 2]
    p <- c()
    for (sc in all_category) {
        p <- c(p, sum(second_category == sc) / length(second_category))
    }
    dd[[length(dd) + 1]] <- p
}
dd <- data.frame(dd)
dd1 <- t(as.matrix(dd))
colnames(dd1) <- all_category
rownames(dd1) <- seq_len(3)
dd1 <- data.frame(dd1)
library(ggradar)
library(Cairo)
Cairo::CairoPNG(
    filename = "name.png", # 文件名称
    width = 7, # 宽
    height = 7, # 高
    units = "in", # 单位
    dpi = 300
) # 分辨率
# 2. 绘图
ggradar(dd1)
# 3. 关闭画布
dev.off()
