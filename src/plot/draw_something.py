import polars as pl
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt

# 设置 matplotlib 中文字体（plotnine 底层使用 matplotlib）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 数据
f = np.array([5.3, 5.5, 5.7, 5.9, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.3])
Vc = np.array([1.14, 1.20, 1.37, 1.52, 1.84, 2.24, 2.66, 2.72, 2.44, 1.68, 1.36])

# 创建DataFrame
df = pl.DataFrame({
    'frequency': f,
    'voltage': Vc,
    'label': [f'{v:.2f}V' for v in Vc]
})

# 绘图 - 在 theme 中指定字体
plot = (
    ggplot(df, aes(x='frequency', y='voltage')) +
    geom_line(color='blue', size=1) +
    geom_point(color='blue', size=2) +
    geom_text(aes(label='label'), 
              nudge_x=0.08, nudge_y=0.05, 
              size=8, ha='center') +
    labs(title='频率与 Vc (Vp-p) 关系曲线',
         x='频率 (MHz)',
         y='Vc (Vp-p) (V)') +
    theme_minimal() +
    theme(
        figure_size=(10, 6),
        plot_title=element_text(family='SimHei', size=14),
        axis_title=element_text(family='SimHei', size=12),
        axis_text=element_text(family='SimHei', size=10),
        text=element_text(family='SimHei')  # 全局字体设置
    )
)

# 显示图形
plot.show()
