# 文件路径处理
from pathlib import Path

# excel处理
import polars as pl

# word处理
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

# PDF处理
from docx2pdf import convert

"""
    这个文件的作用是: 将excel中的数据进行处理, 
    然后生成对应的 word 文件, 最后转成 PDF 文件
    实现逻辑: 每一个处理都是对单个文件的处理, 然后在套上一个方法: 批处理调度器
    本质逻辑还是单个文件处理. 主要是处理一些简单的excel表格, 
    若是特殊表格, 那么只能是特殊情况特殊处理了.
    excel --> word 方法都将其单独整理出来了.
    word --> PDF 方法都将其单独整理出来了.
    所以也可以直接调用, 该有的说明都有.
    
    # TODO
        还差边界情况的处理和 main 函数的逻辑流程没有完成
"""


# 这里的两个代码是进行将 excel 进行批量整理的代码
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


# --- 这里的代码是将 excel 中的数据批量导入 word 并整理好格式的代码 ---


def set_global_font(doc, font_name):
    """设置文档全局中西文字体"""
    style = doc.styles["Normal"]
    style.font.name = font_name
    style.font.size = Pt(11)

    # 获取或创建底层 XML 节点以支持中文字体
    rPr = style._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:eastAsia"), font_name)


def save_as_pretty_word(df, output_path, title_text="复习题库"):
    """将单个 DataFrame 转换为格式美观的 Word"""
    doc = Document()
    set_global_font(doc, "霞鹜文楷")

    # 1. 写入大标题
    title = doc.add_heading("", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(title_text)
    run.font.name = "霞鹜文楷"
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "霞鹜文楷")

    records = df.to_dicts()

    for i, row in enumerate(records, 1):
        # 1. 题干 (加粗, 12pt)
        p = doc.add_paragraph()
        run = p.add_run(f"{i}. {row['题干']}")
        run.bold = True
        run.font.size = Pt(12)

        # 2. 选项 (A,B,C,D)
        for opt in ["A", "B", "C", "D"]:
            col_name = f"选项{opt}"
            # 检查列是否存在且不为空
            if col_name in row and row[col_name]:
                opt_p = doc.add_paragraph(style="List Bullet")
                opt_run = opt_p.add_run(f"{opt}. {row[col_name]}")
                opt_run.font.bold = True

        # 3. 正确答案 (深蓝色, 10pt)
        ans_p = doc.add_paragraph()
        ans_run = ans_p.add_run(f"【正确答案】：{row['正确答案']}")
        ans_run.font.color.rgb = RGBColor(0, 102, 204)
        ans_run.font.size = Pt(10)
        ans_run.font.bold = True

        # 4. 分割线
        doc.add_paragraph("-" * 80)

    doc.save(output_path)


# --- 批量处理逻辑 ---

def batch_process_folder(source_dir, output_dir):
    """
    遍历 source_dir 下所有 Excel，转换并保存到 output_dir
    """
    src_path = Path(source_dir)
    out_path = Path(output_dir)

    # 创建输出文件夹
    out_path.mkdir(parents=True, exist_ok=True)

    # 筛选所有 .xlsx 文件
    files = list(src_path.glob("*.xlsx"))

    if not files:
        print(f"❌ 错误: 在路径 {source_dir} 下没找到 .xlsx 文件")
        return

    print(f"🚀 开始转换任务，共 {len(files)} 个文件...")

    for file in files:
        try:
            # 1. 读取 Excel
            df = pl.read_excel(file)

            # 2. 确定输出路径和文档标题
            file_stem = file.stem
            target_word = out_path / f"{file_stem}.docx"

            # 3. 执行转换
            save_as_pretty_word(df, target_word, title_text=file_stem)
            print(f"✅ 已完成: {file_stem}.docx")

        except Exception as e:
            print(f"⚠️ 处理文件 {file.name} 时发生异常: {e}")


# 将一个文件夹中的 Excel 批量转为 PDF .
# 这个批量处理的方法已经完全足够了, 并不需要和上面一样进行套壳. docx2pdf 的 convert 已经可以处理的非常好了.
def batch_convert_folder_to_pdf(source_dir, output_dir):
    """
    批量将文件夹中的所有 Word 转换为 PDF 并移动到指定目录
    """
    src_path = Path(source_dir)
    out_path = Path(output_dir)

    # 确保输出目录存在
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"🚀 开始批量转换任务: {source_dir} -> {output_dir}")

    try:
        # docx2pdf 的强大之处：可以直接传入两个目录
        # 它会自动匹配源目录下的所有 docx 并生成到目标目录
        convert(str(src_path), str(out_path))
        print(f"\n✨ 批量处理完成！PDF 已存入: {output_dir}")
    except Exception as e:
        print(f"⚠️ 批量转换过程中出现问题: {e}")

# 这里将来的输入函数,
# 但是还是有点问题毕竟最后是一个 main 函数进行调用了, 所以调用逻辑我还需要思考
# input_folder = r"C:\Users\asus\Desktop\学校作业\信息论"
# output_folder = None
#
#
# header_row = int(input("请输入你想要作为列名的那一行(从 1 开始数): "))
#
# # # 输入示例: 题型
# judge_column = input(
#     "请输入用于判断的列(通过这一列的数据来判断留下哪些行, 只能输入一个字符串): "
# )
#
#
# # # 输入示例：单选题 多选题
# keep_row = list(
#     input("请输入你想要保留的行(judge_column中你想要留下的行): ").split(" ")
# )
#
#
# # # 输入示例：题干 正确答案 选项A 选项B 选项C 选项D
# keep_column = list(input("请输入你想要保留的列: ").split(" "))
#
# batch_excel_data_process(
#     input_folder, judge_column, keep_row, keep_column, header_row, output_folder
# )