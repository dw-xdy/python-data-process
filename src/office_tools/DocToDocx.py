import win32com.client as win32
from pathlib import Path
import sys


def convert_doc_to_docx(word, doc_path, docx_path):
    """将单个 .doc 文件转换为 .docx"""
    try:
        doc = word.Documents.Open(str(doc_path.resolve()))
        doc.SaveAs2(str(docx_path), FileFormat=16)  # 16 = wdFormatDocumentDefault
        doc.Close()
        print(f"  ✓ 已转换: {doc_path.name} -> {docx_path.name}")
        return True
    except Exception as e:
        print(f"  ✗ 转换失败 {doc_path.name}: {e}")
        return False


def process_single_file(word, file_path, output_folder):
    """处理单个 .doc 文件，转换为 .docx 并存放到指定输出文件夹"""
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False

    if file_path.suffix.lower() != ".doc":
        print(f"❌ 不支持的文件格式: {file_path.name}（仅支持 .doc）")
        return False

    # 输出路径：放在 docx 文件夹下，保持原文件名
    docx_path = output_folder / f"{file_path.stem}.docx"

    # 如果目标文件已存在，询问是否覆盖
    if docx_path.exists():
        print(f"⚠️ 目标文件已存在: {docx_path.name}")
        overwrite = input("是否覆盖？(y/n): ").strip().lower()
        if overwrite != "y":
            print(f"  ✗ 跳过: {file_path.name}")
            return False

    return convert_doc_to_docx(word, file_path, docx_path)


def process_folder(word, folder_path):
    """处理文件夹：查找所有 .doc 文件并转换"""
    folder_path = Path(folder_path)

    if not folder_path.exists() or not folder_path.is_dir():
        print(f"❌ 文件夹不存在或无效: {folder_path}")
        return

    # 在输入的文件夹下创建 docx 文件夹
    docx_folder = folder_path / "docx"
    docx_folder.mkdir(exist_ok=True)
    print(f"📂 docx 输出目录: {docx_folder}\n")

    # 查找所有 .doc 文件（排除临时文件）
    doc_files = [
        f
        for f in folder_path.iterdir()
        if f.is_file() and f.suffix.lower() == ".doc" and not f.name.startswith("~$")
    ]

    if not doc_files:
        print(f"⚠️ 在 {folder_path} 中未找到任何 .doc 文件")
        return

    print(f"📁 找到 {len(doc_files)} 个 .doc 文件")
    print("-" * 60)

    success_count = 0
    for file_path in doc_files:
        print(f"📄 正在处理: {file_path.name}")
        if process_single_file(word, file_path, docx_folder):
            success_count += 1
        print()

    print("-" * 60)
    print(f"✨ 完成！成功: {success_count}/{len(doc_files)} 个文件")


def normalize_path(path_str):
    """标准化路径，处理各种输入格式"""
    # 去除首尾空格和引号
    path_str = path_str.strip().strip('"').strip("'")
    # 将反斜杠替换为正斜杠
    path_str = path_str.replace("\\", "/")
    return path_str


def main():
    """主函数：支持拖拽文件/文件夹到脚本上运行，或直接双击运行后输入路径"""
    print("=" * 60)
    print(".doc 转 .docx 工具")
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
            return

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
        return

    # 处理每个路径
    for input_path in input_paths:
        if not input_path.exists():
            print(f"❌ 路径不存在: {input_path}")
            continue

        if input_path.is_file():
            # 单个文件处理：需要在文件所在目录创建 docx 文件夹
            docx_folder = input_path.parent / "docx"
            docx_folder.mkdir(exist_ok=True)
            print(f"📄 处理单个文件: {input_path}")
            process_single_file(word, input_path, docx_folder)
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
