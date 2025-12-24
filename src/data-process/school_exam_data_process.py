from pathlib import Path
import polars as pl


def excel_data_process(
    input_file: str | Path,  # 支持字符串或Path
    output_file: str | Path,  # 支持字符串或Path
    header_row: int,
    judge_column: str,
    keep_row: list[str],
    keep_column: list[str],
) -> bool:
    """
    关于这个方法:  是用来整理学校发的excel (必须是.xlsx后缀) 表中的数据, 并进行清洗,
    是一个非常简单的任务处理, 并不是非常专业的处理方式, 但是我想用来处理学校的excel绝对是足够了.
    可以根据需求决定是否需要转换成: word, 或者进一步转换成: PDF,
    后面会有对应的提示.
    :param input_file: 必须是一个文件的路径(包括名字)
    :param output_file: 必须是保存文件的路径(包括名字)
    :param header_row: 第几行作为各个列的名字 (从 1 开始计数)
    :param judge_column: 根据这一列来判断行中的元素是不是需要保留.
    :param keep_row: 存放你想要保留的行
    :param keep_column: 需要保留的列.
    :return: bool 类型的值
    """

    try:
        df = pl.read_excel(input_file, read_options={"header_row": header_row - 1})
        ans = df.filter(pl.col(judge_column).is_in(keep_row)).select(
            pl.col(keep_column)
        )
        ans.write_excel(output_file)
        return True
    except Exception as e:
        print(f"文件操作出现错误: {e}")
        return False


def batch_excel_data_process(
    input_folder: str,
    judge_column: str,
    keep_row: list[str],
    keep_column: list[str],
    header_row: int,
    output_folder: str = None,
) -> None:
    """
    关于这个方法:  是用来批量整理学校发的excel (必须是.xlsx后缀) 表中的数据, 并进行清洗,
    是一个非常简单的任务处理, 并不是非常专业的处理方式, 但是我想用来处理学校的excel绝对是足够了.
    可以根据需求决定是否需要转换成: word, 或者进一步转换成: PDF.
    后面会有对应的提示.
    :param input_folder: 必须是一个文件夹的路径
    :param judge_column: 根据这一列来判断行中的元素是不是需要保留.
    :param header_row: 第几行作为各个列的名字 (从 1 开始计数)
    :param keep_row: 存放你想要保留的行
    :param keep_column: 需要保留的列.
    :param output_folder: 必须是保存文件夹的路径
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

        ans = excel_data_process(
            input_file,
            output_file,
            header_row,
            judge_column,
            keep_row,
            keep_column,
        )

        print(f"{excel_file.name}处理完成" if ans else f"{excel_file}处理失败")

    print("-" * 50)
    # 显示输出文件夹内容
    excel_files_finish = list(output_path.glob("*.xlsx"))
    if excel_files_finish:
        print(f"生成Excel文件数量: {len(excel_files_finish)} 个")
    else:
        print("警告: 输出文件夹中没有找到Excel文件")


input_folder = r"C:\Users\asus\Desktop\学校作业\信息论"
output_folder = None


header_row = int(input("请输入你想要作为列名的那一行(从 1 开始数): "))

# # 输入示例: 题型
judge_column = input(
    "请输入用于判断的列(通过这一列的数据来判断留下哪些行, 只能输入一个字符串): "
)


# # 输入示例：单选题 多选题
keep_row = list(
    input("请输入你想要保留的行(judge_column中你想要留下的行): ").split(" ")
)


# # 输入示例：题干 正确答案 选项A 选项B 选项C 选项D
keep_column = list(input("请输入你想要保留的列: ").split(" "))

batch_excel_data_process(
    input_folder, judge_column, keep_row, keep_column, header_row, output_folder
)
