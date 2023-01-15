# 这个代码块定义了流程必要参数
if (TRUE) {
    rm(list = ls())
    # cat("多张热图合并")
    dd <- "C:\\Users\\leois\\Desktop\\nkdaxue\\data.xlsx" # nolint 数据，横轴分组为class列。纵轴长度为sheet表的个数。
    opt <- "./result"
    groups_index <- 1 # 表示横轴分组信息放在data.xlsx的哪一列。默认第一列。
    gene_index <- 5
    num_index <- 9 # 表达量数据位置
    # 默认纵向信息在SheetName里读取x
}


# 这个代码块读取了数据，创建了输出目录
if (TRUE) {
    if (!dir.exists(opt)) {
        dir.create(opt, recursive = TRUE)
    }
    lst <- list()
    if (!endsWith(dd, "xlsx")) {
        cat("输入文件应该为xlsx格式的表格。")
    } else {
        # library(tidyverse)
        library(openxlsx)
        all_sheets <- openxlsx::getSheetNames(dd)
    }
    for (sheet in all_sheets) {
        df <- read.xlsx(dd, sheet)
        lst[[sheet]] <- df
    }
}


# 这个代码块定义了在apply族中可能用到的函数
if (TRUE) {
    is_in <- function(x, result = c()) {
        return(x %in% result)
    }

    get_one_gene <- function(string) {
        x <- strsplit(string, ";")[[1]][1]
        if (is.na(x)) {
            return(NA)
        } else {
            return(x)
        }
    }
}



# 这个区块处理了数据
if (TRUE) {
    groups <- levels(factor(lst[[1]][, groups_index]))
    for (group in groups) {
        if (group == "ECM-associated") {
            next
        }
        print(group)
        # 选出每组里的所有基因
        for (sheet in all_sheets) {
            d <- lst[[sheet]]
            x <- unlist(lapply(d[d[[groups_index]] == group, gene_index], get_one_gene)) # nolint
            x <- na.omit(x)
            assign(paste(group, sheet, sep = ""), x) #  nolint
        }
        inter_set <- get(paste(group, all_sheets[1], sep = ""))
        # 选取共有的基因
        for (i in seq_len(length(all_sheets))) {
            vir <- paste(group, all_sheets[i + 1], sep = "")
            next_one <- get(vir)
            inter_set <- intersect(inter_set, next_one)
            cat("交集大小为：", length(inter_set), "\n")
            if (i + 1 == length(all_sheets)) {
                break
            }
        }
        cat("最后交集大小为", length(inter_set), "\n")
        # inter_set为保存共有基因的变量
        # 构建矩阵用于绘图
        single_group_data <- c()
        for (i in seq_len(length(all_sheets))) {
            sheet <- all_sheets[i]
            dd <- lst[[sheet]]
            dd <- dd[which(dd[, groups_index] == group), ]
            dd1 <- dd[, c(gene_index, num_index)]
            dd1$gene <- unlist(lapply(dd1[, 1], get_one_gene))
            dd2 <- dd1[dd1[, "gene"] %in% inter_set, ]
            x <- as.numeric(tapply(dd2[, 2], dd2[, 3], max))
            single_group_data <- c(single_group_data, x)
            cat(i, "挑选出交集的行后dd2的大小为", nrow(dd2), "dd1", nrow(dd1), "交集", length(inter_set), "基因表达值向量长度", length(x), "矩阵现在的大小:", length(single_group_data), "\n", sep = "\t") # nolint
        }


        temp <- matrix(single_group_data, ncol = length(inter_set), nrow = length(all_sheets), byrow = TRUE) # nolint
        matrix_data <- assign(paste0("matrix_", group), log(temp + 1, 2))
    }
}

# 这个代码块完成画图

if (TRUE) {
    ht_lst <- NULL
    get_color_ob_maxnum <- (-1)
    get_color_ob_min <- 0
    for (group in groups) {
        if (group == "ECM-associated") {
            next
        }
        data_m <- get(paste0("matrix_", group))
        data_m[is.na(data_m)] <- 0
        if (max(data_m) > get_color_ob_maxnum) {
            get_color_ob_maxnum <- max(data_m)
        }

        if (min(data_m) < get_color_ob_min) {
            get_color_ob_maxnum <- min(data_m)
        }
    }
    get_color_ob_maxnum <- max(abs(ceiling(get_color_ob_min)), abs(ceiling(get_color_ob_maxnum))) # nolint
    # startDraw
    library(ComplexHeatmap)
    library(circlize)
    library(RColorBrewer)
    get_color_ob <- colorRamp2(c(-get_color_ob_maxnum, 0, get_color_ob_maxnum), colors = c("blue", "white", "red")) # nolint

    mypalette <- c("#19a2ec", "#33a02c", "#fdbf6f")

    for (i in seq_len(length(groups)))
    {
        if (groups[i] == "ECM-associated") {
            next
        }
        lg_show <- FALSE
        lg <- list()
        if (i == 1) {
            lg_show <- TRUE
            lg <- list(title = NULL, legend_height = unit(9, "cm")) # nolint
        }
        group <- groups[i]
        data_m <- get(paste0("matrix_", group))
        col_ <- rep(mypalette[i], ncol(data_m))
        names(col_) <- rep(groups[i], ncol(data_m))
        data_m <- data_m[, !apply(data_m, 2, function(x) any(is.na(x)))]

        col_Annotation <- HeatmapAnnotation(foo = anno_block(gp = gpar(fill = i + 3))) # nolint
        ht <- Heatmap(data_m,
            # clustering_distance_columns  = "pearson",
            column_title = group,
            col = get_color_ob,
            column_title_side = "bottom",
            column_title_gp = gpar(fontsize = 20, fontface = 1),
            cluster_rows = FALSE,
            show_heatmap_legend = lg_show,
            column_dend_height = unit(3, "cm"),
            heatmap_legend_param = lg,
            width = unit(ncol(data_m) * 0.3, "cm"),
            height = 400,
            column_title_rot = 45,
            bottom_annotation = col_Annotation,
        )

        ht_lst <- ht_lst + ht
    }
}
draw(ht_lst, heatmap_legend_side = "left")
library(Cairo)
Cairo::CairoPNG(
    filename = "ComplexHeatmap.png",
    width = 23, # 宽
    height = 8, # 高
    units = "in", # 单位
    dpi = 300
) # 分辨率
draw(ht_lst, heatmap_legend_side = "left")
dev.off()
