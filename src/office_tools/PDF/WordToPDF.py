import os
from pathlib import Path
from docx2pdf import convert


def convert_single_word_to_pdf(word_path, pdf_path=None):
    """
    将单个 Word 文件转换为 PDF
    :param word_path: 源 docx 文件路径
    :param pdf_path: 目标 pdf 路径（如果不填，默认在同级目录生成同名 pdf）
    """
    try:
        print(f"正在转换单个文件: {os.path.basename(word_path)}...")
        # docx2pdf 的 convert 函数非常智能
        # 如果只传一个参数，它会在原地生成 PDF
        convert(word_path, pdf_path)
        print(f"✅ 转换成功!")
    except Exception as e:
        print(f"❌ 转换失败: {e}")


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


# --- 执行示例 ---
if __name__ == "__main__":
    # 设置你的 Word 所在的文件夹
    WORD_INPUT = r"C:\Users\asus\Desktop\学校作业\信息论\output"
    # 设置你希望存放 PDF 的文件夹
    PDF_OUTPUT = r"C:\Users\asus\Desktop\学校作业\信息论\output\PDF_Final"

    batch_convert_folder_to_pdf(WORD_INPUT, PDF_OUTPUT)