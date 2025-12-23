import polars as pl


def excel_data_process(
    input_file: str,
    output_file: str,
    judge_column: str,
    keep_row: list[str],
    keep_column: list[str],
) -> None:
    """
    关于这个方法:  是用来整理学校发的excel (必须是.xlsx后缀) 表中的数据, 并进行清洗,
    是一个非常简单的任务处理, 并不是非常专业的处理方式, 但是我想用来处理学校的excel绝对是足够了.
    可以根据需求决定是否需要转换成: word, 或者进一步转换成: PDF,
    后面会有对应的提示.
    :param input_file: 必须是一个文件的路径(包括名字)
    :param output_file: 必须是保存文件的路径(包括名字)
    :param judge_column: 根据这一列来判断行中的元素是不是需要保留.
    :param keep_row: 存放你想要保留的行
    :param keep_column: 需要保留的列.
    :return: None
    """
    # keep_column = ["题干", "正确答案", "选项A", "选项B", "选项C", "选项D"]
    # keep_row = ["单选题", "多选题", "判断题", "应用题"]
    try:
        df = pl.read_excel(input_file)
        ans = df.filter(pl.col(judge_column).is_in(keep_row)).select(pl.col(keep_column))
        ans.write_excel(output_file)
        print("转换完成")
    except Exception as e:
        print(f"文件操作出现错误: {e}")





excel_file = r"C:\Users\asus\Desktop\学校作业\信息论第二章测试_习题导出.xlsx"

output_file = r"C:\Users\asus\Desktop\学校作业\kaishi\信息论.xlsx"

judge_list = "题型"

keep_row = ["单选题"]

keep_column = ["题干", "正确答案", "选项A", "选项B", "选项C", "选项D"]

excel_data_process(excel_file, output_file, judge_list, keep_row, keep_column)
