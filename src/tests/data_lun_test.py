import polars as pl
import pandas as pd

data_lun_file_csv = r"C:\Users\asus\Desktop\学校作业\信息论第二章测试_习题导出.csv"


df = pl.read_csv(data_lun_file_csv)

data_list = ["题干", "正确答案", "选项A", "选项B", "选项C", "选项D"]

ans = df.filter((pl.col("题型") == "单选题")).select(pl.col(data_list))

print(ans)

pandas_ans = ans.to_pandas()

data_lun_output_file = (
    r"C:\Users\asus\Desktop\学校作业\kaishi\信息论第二章测试_习题导出.csv"
)

# 指定编码保存（支持多种编码）
pandas_ans.to_csv(
    data_lun_output_file,
    index=False,
    encoding="utf-8-sig",  # 既支持特殊符号，又能让 Excel 不乱码
)
