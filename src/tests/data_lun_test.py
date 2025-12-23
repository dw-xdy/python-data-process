import polars as pl

data_lun_file_csv = r"C:\Users\asus\Desktop\学校作业\信息论第二章测试_习题导出.csv"
data_lun_file_xlsx = r"C:\Users\asus\Desktop\学校作业\信息论第二章测试_习题导出.xlsx"


df = pl.read_excel(data_lun_file_xlsx)

data_list = ["题干", "正确答案", "选项A", "选项B", "选项C", "选项D"]

# 注意这里: 要进行过滤, 然后再进行选择列.
ans = df.filter((pl.col("题型") == "单选题")).select(pl.col(data_list))

print(ans)

data_lun_output_xlsx_file = (
    r"C:\Users\asus\Desktop\学校作业\kaishi\信息论第二章测试_习题导出.xlsx"
)


ans.write_excel(data_lun_output_xlsx_file)


# 保存为.csv文件的时候指定编码可以使用如下方式.

# pandas_ans = ans.to_pandas()
#
# data_lun_output_csv_file = (
#     r"C:\Users\asus\Desktop\学校作业\kaishi\信息论第二章测试_习题导出.xlsx"
# )
#
#
#
# # 指定编码保存（支持多种编码）
# pandas_ans.to_csv(
#     data_lun_output_file,
#     index=False,
#     encoding="utf-8-sig",  # 既支持特殊符号 (比如说下标)，又能让 Excel 不乱码
# )
