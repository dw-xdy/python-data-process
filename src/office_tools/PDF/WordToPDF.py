from pathlib import Path
from docx2pdf import convert


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


def batch_convert_folder_to_pdf(source_dir: Path, output_dir: Path):
    """批量将文件夹中的所有 Word 转换为 PDF"""
    if not source_dir.exists():
        print(f"❌ 源文件夹不存在: {source_dir}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"🚀 开始转换: {source_dir} -> {output_dir}")

    try:
        convert(str(source_dir), str(output_dir))
        print(f"\n✨ 转换完成！PDF 已保存到: {output_dir}")
    except Exception as e:
        print(f"⚠️ 转换失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    WORD_INPUT = get_input_path("请输入Word源文件夹路径", check_exists=True)
    PDF_OUTPUT = get_input_path("请输入PDF目标文件夹路径")
    batch_convert_folder_to_pdf(WORD_INPUT, PDF_OUTPUT)
