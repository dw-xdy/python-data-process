from pathlib import Path
from pdf2docx import Converter
import traceback


def get_input_path(prompt: str, check_exists: bool = False) -> Path:
    """获取输入路径，可选检查路径是否存在"""
    while True:
        path_str = input(prompt + ": ").strip()
        if not path_str:
            print("❌ 路径不能为空")
            continue

        path = Path(path_str)
        if check_exists and not path.exists():
            print(f"❌ 路径不存在: {path_str}")
            continue

        return path


def batch_convert_pdfs_to_word(source_dir: Path, output_dir: Path):
    """批量将文件夹中的所有 PDF 转换为 Word"""
    if not source_dir.exists():
        print(f"❌ 源文件夹不存在: {source_dir}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # 使用更简洁的方式查找PDF文件
    pdf_files = list(source_dir.glob("*.pdf")) + list(source_dir.glob("*.PDF"))

    if not pdf_files:
        print(f"⚠️ 在 {source_dir} 中没有找到 PDF 文件")
        return

    print(f"📁 找到 {len(pdf_files)} 个 PDF 文件")
    print("-" * 50)

    success_count = 0
    fail_count = 0

    for i, pdf_path in enumerate(pdf_files, 1):
        output_path = output_dir / f"{pdf_path.stem}.docx"
        print(f"[{i}/{len(pdf_files)}] 转换中: {pdf_path.name}")

        try:
            cv = Converter(str(pdf_path))
            cv.convert(str(output_path))  # 添加参数明确转换范围
            cv.close()
            print(f"    ✅ 成功: {output_path.name}")
            success_count += 1
        except Exception as e:
            print(f"    ❌ 失败: {pdf_path.name}")
            print(f"    错误: {str(e)[:100]}")  # 只显示前100个字符
            fail_count += 1
            # 可以选择是否打印详细错误
            traceback.print_exc()

    print("-" * 50)
    print(f"✨ 转换完成！成功: {success_count}, 失败: {fail_count}")
    print(f"📂 文件保存在: {output_dir}")


if __name__ == "__main__":
    PDF_INPUT = get_input_path("请输入PDF源文件夹路径", check_exists=True)
    WORD_OUTPUT = get_input_path("请输入Word目标文件夹路径")

    batch_convert_pdfs_to_word(PDF_INPUT, WORD_OUTPUT)
