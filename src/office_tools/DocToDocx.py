import win32com.client as win32
from pathlib import Path


def batch_convert(folder_path):
    """
    将指定文件夹下的所有 .doc 文件批量转换为 .docx

    Args:
        folder_path: 文件夹路径（字符串或Path对象）
    """
    # 转换为Path对象
    folder_path = Path(folder_path)

    # 检查文件夹是否存在
    if not folder_path.exists():
        print(f"错误：文件夹不存在 - {folder_path}")
        return

    if not folder_path.is_dir():
        print(f"错误：路径不是文件夹 - {folder_path}")
        return

    # 获取所有 .doc 文件（排除临时文件）
    file_paths = [
        str(folder_path / f.name)
        for f in folder_path.iterdir()
        if f.suffix.lower() == ".doc" and not f.name.startswith("~$")
    ]

    if not file_paths:
        print(f"在 {folder_path} 中未找到任何 .doc 文件")
        return

    # 开始转换
    print(f"准备转换 {len(file_paths)} 个文件...")
    print("-" * 50)

    try:
        # 启动 Word 应用程序
        word = win32.gencache.EnsureDispatch("Word.Application")
        word.Visible = False

        success_count = 0
        for doc_path in file_paths:
            doc_path_obj = Path(doc_path)
            abs_path = str(doc_path_obj.resolve())
            docx_path = str(doc_path_obj.with_suffix(".docx"))

            try:
                doc = word.Documents.Open(abs_path)
                doc.SaveAs2(docx_path, FileFormat=16)  # 16 对应 wdFormatDocumentDefault
                doc.Close()
                success_count += 1
                print(f"✓ 已转换: {doc_path_obj.name}")
            except Exception as e:
                print(f"✗ 转换失败 {doc_path_obj.name}: {e}")

        word.Quit()
        print("-" * 50)
        print(f"转换完成！成功: {success_count}/{len(file_paths)}")

    except Exception as e:
        print(f"错误：无法启动 Word 应用程序 - {e}")


if __name__ == "__main__":
    # 从命令行输入文件夹路径
    while True:
        folder_input = input("请输入要转换的文件夹路径：").strip()

        # 去除可能存在的引号
        folder_input = folder_input.strip('"').strip("'")

        if not folder_input:
            print("路径不能为空，请重新输入。")
            continue

        # 转换为绝对路径
        folder_path = Path(folder_input).resolve()

        if folder_path.exists() and folder_path.is_dir():
            batch_convert(folder_path)
            break
        else:
            print(f"错误：'{folder_input}' 不是一个有效的文件夹路径，请重新输入。")
