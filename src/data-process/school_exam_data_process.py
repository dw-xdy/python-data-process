from pathlib import Path
from typing import Union

import polars as pl


def excel_data_process(
    input_file: Union[str, Path],    # 支持字符串或Path
    output_file: Union[str, Path],   # 支持字符串或Path
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
        ans = df.filter(pl.col(judge_column).is_in(keep_row)).select(
            pl.col(keep_column)
        )
        ans.write_excel(output_file)
        print("转换完成")
    except Exception as e:
        print(f"文件操作出现错误: {e}")





def batch_excel_data_process(
        input_folder: str,
        judge_column: str,
        keep_row: list[str],
        keep_column: list[str],
        output_folder: str = None,
) -> None:
    """
    关于这个方法:  是用来批量整理学校发的excel (必须是.xlsx后缀) 表中的数据, 并进行清洗,
    是一个非常简单的任务处理, 并不是非常专业的处理方式, 但是我想用来处理学校的excel绝对是足够了.
    可以根据需求决定是否需要转换成: word, 或者进一步转换成: PDF.
    后面会有对应的提示.
    :param input_folder: 必须是一个文件夹的路径
    :param judge_column: 根据这一列来判断行中的元素是不是需要保留.
    :param keep_row: 存放你想要保留的行
    :param keep_column: 需要保留的列.
    :param output_folder: 必须是保存文件夹子的路径
    :return: None
    """
    # 转换为 Path 对象
    input_path = Path(input_folder)

    # 设置输出路径
    output_path = Path(output_folder) if output_folder else input_path / "excel_output"
    output_path.mkdir(parents=True, exist_ok=True)

    # 获取 Excel 文件列表（Path 对象列表）
    excel_files = list(input_path.glob("*.xlsx"))

    if not excel_files:
        print(f"在文件夹 '{input_path}' 中没有找到Excel文件")
        return

    print(f"找到 {len(excel_files)} 个Excel文件")
    print(f"输出文件夹: {output_path}")
    print("-" * 50)

    for excel_file in excel_files:
        print(f"\n正在处理: {excel_file.name}")

        input_file = excel_file
        output_file = output_path / excel_file.name

        excel_data_process(
            input_file,
            output_file,
            judge_column,
            keep_row,
            keep_column,
        )

        print(f"{excel_file.name}处理完成")

    print("-" * 50)
    # 显示输出文件夹内容
    excel_files_finish = list(output_path.glob("*.xlsx"))
    if excel_files_finish:
        print(f"生成Excel文件数量: {len(excel_files_finish)} 个")
    else:
        print("警告: 输出文件夹中没有找到Excel文件")


input_folder = r"C:\Users\asus\Desktop\学校作业\信息论"
output_folder = None

judge_column = "题型"

keep_row = ["单选题"]

keep_column = ["题干", "正确答案", "选项A", "选项B", "选项C", "选项D"]

batch_excel_data_process(input_folder, judge_column, keep_row, keep_column, output_folder)
