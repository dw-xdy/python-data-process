import polars as pl
from plotnine import *

# 1. 准备数据
df = pl.DataFrame(
    {
        "f": [5.3, 5.5, 5.7, 5.9, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.3],
        "v": [1.14, 1.20, 1.37, 1.52, 1.84, 2.24, 2.66, 2.72, 2.44, 1.68, 1.36],
    }
)

# 2. 绘图
# 这里的 'Microsoft YaHei' 适用于 Windows。如果是 Mac，可以换成 'Arial Unicode MS' 或 'STHeiti'
zh_theme = theme(text=element_text(family="Microsoft YaHei"))

(
    ggplot(df, aes(x="f", y="v"))
    + geom_line(color="blue")
    + geom_point(color="blue")
    + geom_text(aes(label="v"), format_string="{:.2f}V", nudge_x=0.08, size=8)
    + labs(title="频率与 Vc (Vp-p) 关系曲线", x="频率 (MHz)", y="Vc (Vp-p) (V)")
    + theme_minimal()
    + zh_theme  # <--- 应用中文字体主题
    + theme(figure_size=(10, 6))
).show()
