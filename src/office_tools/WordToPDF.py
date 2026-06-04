import win32com.client as win32
from pathlib import Path
import sys


def convert_doc_to_docx(word, doc_path, docx_path):
    """将 .doc 转换为 .docx"""
    try:
        doc = word.Documents.Open(str(doc_path.resolve()))
        doc.SaveAs2(str(docx_path), FileFormat=16)
        doc.Close()
        print(f"  ✓ 已转换为 .docx: {doc_path.name}")
        return True
    except Exception as e:
        print(f"  ✗ 转换 .doc 失败 {doc_path.name}: {e}")
        return False


def convert_to_pdf(word, file_path, pdf_path):
    """将 Word 文件（.doc 或 .docx）转换为 PDF"""
    try:
        doc = word.Documents.Open(str(file_path.resolve()))
        doc.SaveAs2(str(pdf_path), FileFormat=17)
        doc.Close()
        print(f"  ✓ 已转换为 PDF: {pdf_path.name}")
        return True
    except Exception as e:
        print(f"  ✗ 转换 PDF 失败 {file_path.name}: {e}")
        return False


def process_single_file(word, file_path):
    """处理单个文件：如果是 .doc 先转为 .docx 再转 PDF"""
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False

    suffix = file_path.suffix.lower()
    if suffix not in [".doc", ".docx"]:
        print(f"❌ 不支持的文件格式: {file_path.name}（仅支持 .doc 和 .docx）")
        return False

    # 在文件所在目录下创建 PDF 文件夹
    pdf_folder = file_path.parent / "PDF"
    pdf_folder.mkdir(exist_ok=True)

    # 确定 PDF 输出路径
    pdf_path = pdf_folder / f"{file_path.stem}.pdf"

    # 如果文件是 .doc，需要先转换为 .docx
    if suffix == ".doc":
        docx_path = file_path.with_suffix(".docx")
        if convert_doc_to_docx(word, file_path, docx_path):
            result = convert_to_pdf(word, docx_path, pdf_path)
            # 清理临时 .docx 文件
            if docx_path.exists():
                docx_path.unlink()
            return result
        return False
    else:  # .docx 文件
        return convert_to_pdf(word, file_path, pdf_path)


def process_folder(word, folder_path):
    """处理文件夹：查找所有 .doc 和 .docx 文件并转换"""
    folder_path = Path(folder_path)

    if not folder_path.exists() or not folder_path.is_dir():
        print(f"❌ 文件夹不存在或无效: {folder_path}")
        return

    # 在输入的文件夹下创建 PDF 文件夹
    pdf_folder = folder_path / "PDF"
    pdf_folder.mkdir(exist_ok=True)
    print(f"📂 PDF 输出目录: {pdf_folder}\n")

    # 查找所有 Word 文件
    word_files = []
    for f in folder_path.iterdir():
        if f.is_file() and not f.name.startswith("~$"):
            suffix = f.suffix.lower()
            if suffix in [".doc", ".docx"]:
                word_files.append(f)

    if not word_files:
        print(f"⚠️ 在 {folder_path} 中未找到任何 .doc 或 .docx 文件")
        return

    print(f"📁 找到 {len(word_files)} 个 Word 文件")
    print("-" * 60)

    success_count = 0
    for file_path in word_files:
        print(f"📄 正在处理: {file_path.name}")
        if process_single_file(word, file_path):
            success_count += 1
        print()

    print("-" * 60)
    print(f"✨ 完成！成功: {success_count}/{len(word_files)} 个文件")


def normalize_path(path_str):
    """标准化路径，处理各种输入格式"""
    # 去除首尾空格和引号
    path_str = path_str.strip().strip('"').strip("'")

    # 将反斜杠替换为正斜杠（避免转义问题）
    path_str = path_str.replace("\\", "/")

    return path_str


def main():
    """主函数：支持拖拽文件/文件夹到脚本上运行，或直接双击运行后输入路径"""
    print("=" * 60)
    print("Word 转 PDF 工具（支持 .doc/.docx）")
    print("=" * 60)
    print("\n提示：可以直接粘贴路径，支持使用反斜杠(\\ 或 /)")
    print("-" * 60)

    # 获取要处理的路径
    if len(sys.argv) > 1:
        # 从命令行参数获取路径（支持拖拽）
        input_paths = [Path(normalize_path(p)) for p in sys.argv[1:]]
    else:
        # 手动输入路径
        print("\n请输入要处理的文件或文件夹路径：")
        print("（支持多个路径，用空格分隔）")
        path_input = input(">>> ").strip()
        if not path_input:
            print("❌ 路径不能为空")
            input("\n按 Enter 键退出...")
            return

        # 分割多个路径（支持空格分隔）
        # 使用简单的分割，然后标准化每个路径
        raw_paths = path_input.split()
        input_paths = []
        for raw_path in raw_paths:
            normalized = normalize_path(raw_path)
            if normalized:
                input_paths.append(Path(normalized))

    # 启动 Word 应用程序
    print("\n🚀 正在启动 Word 应用程序...")
    try:
        word = win32.gencache.EnsureDispatch("Word.Application")
        word.Visible = False
        print("✓ Word 已启动\n")
    except Exception as e:
        print(f"❌ 无法启动 Word 应用程序: {e}")
        input("\n按 Enter 键退出...")
        return

    # 处理每个路径
    for input_path in input_paths:
        if not input_path.exists():
            print(f"❌ 路径不存在: {input_path}")
            print(f"   提示：请检查路径是否正确，或尝试使用正斜杠(/)或双反斜杠(\\\\)")
            continue

        if input_path.is_file():
            print(f"📄 处理单个文件: {input_path}")
            process_single_file(word, input_path)
        elif input_path.is_dir():
            print(f"📁 处理文件夹: {input_path}")
            process_folder(word, input_path)
        else:
            print(f"❌ 无效路径: {input_path}")

    # 关闭 Word 应用程序
    word.Quit()
    print(f"\n🎉 所有任务完成！")


if __name__ == "__main__":
    main()
