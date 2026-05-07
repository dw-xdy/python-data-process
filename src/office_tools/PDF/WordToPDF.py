from pathlib import Path
from docx2pdf import convert


def batch_convert_folder_to_pdf(source_dir: Path, output_dir: Path):
    """
    批量将文件夹中的所有 Word 转换为 PDF 并移动到指定目录
    """
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🚀 开始批量转换任务: {source_dir} -> {output_dir}")

    try:
        # docx2pdf 的强大之处：可以直接传入两个目录
        # 它会自动匹配源目录下的所有 docx 并生成到目标目录
        convert(source_dir, output_dir)
        print(f"\n✨ 批量处理完成！PDF 已存入: {output_dir}")
    except Exception as e:
        print(f"⚠️ 批量转换过程中出现问题: {e}")


# --- 执行示例 ---
if __name__ == "__main__":
    # 设置你的 Word 所在的文件夹
    WORD_INPUT = r"C:\Users\asus\Desktop\学校作业\通信原理"
    # 设置你希望存放 PDF 的文件夹
    PDF_OUTPUT = r"C:\Users\asus\Desktop\学校作业\通信原理"

    batch_convert_folder_to_pdf(Path(WORD_INPUT), Path(PDF_OUTPUT))
