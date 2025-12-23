import polars as pl
import re


def data_process(
    input_file: str,
    output_file: str,
    judge_column: str,
    keep_row: list[str],
    keep_column: list[str],
) -> None:
    """
    关于这个方法:  是用来整理学校发的excel (必须是.xlsx后缀) 表中的数据, 并进行清洗,
    可以根据需求决定是否需要转换成: word, 或者进一步转换成: PDF,
    后面会有对应的提示.
    :param input_file: 必须是一个文件的路径(包括名字)
    :param output_file: 必须是保存文件的路径(包括名字)
    :param judge_column: 根据这一列来判断行中的元素是不是需要保留.
    :param keep_row: 存放你想要保留的行
    :param keep_column: 需要保留的列.
    :return: None
    """

    df = pl.read_excel(input_file)
    # keep_column = ["题干", "正确答案", "选项A", "选项B", "选项C", "选项D"]
    # keep_row = ["单选题", "多选题", "判断题", "应用题"]

    ans = df.filter((pl.col(judge_column).is_in(keep_row))).select(pl.col(keep_column))
    ans.write_excel(output_file)
