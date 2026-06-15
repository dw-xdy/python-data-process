import win32com.client as win32
from pathlib import Path
import sys
import subprocess
import platform


def normalize_path(path_str):
    """标准化路径，处理各种输入格式"""
    path_str = path_str.strip().strip('"').strip("'")
    path_str = path_str.replace("\\", "/")
    return path_str


def get_input_path() -> Path:
    """获取输入路径（支持文件或文件夹，支持拖拽）"""
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            path_str = normalize_path(arg)
            path = Path(path_str)
            if path.exists():
                print(f"📌 检测到拖拽路径: {path}")
                return path
            else:
                print(f"⚠️ 拖拽路径不存在: {path_str}")

    while True:
        print("\n提示：可以直接拖拽文件或文件夹到此窗口，然后按 Enter")
        path_str = input("请输入 .doc 文件或文件夹路径: ").strip()
        path_str = path_str.strip().strip('"').strip("'")

        if not path_str:
            print("❌ 路径不能为空")
            continue

        path = Path(path_str)
        if not path.exists():
            print(f"❌ 路径不存在: {path_str}")
            continue

        return path


def get_output_dir(input_path: Path) -> Path:
    """自动生成输出目录"""
    output_dir = input_path.parent / "docx" if input_path.is_file() else input_path / "docx"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_doc_files(input_path: Path) -> list:
    """获取要转换的 .doc 文件列表"""
    if input_path.is_file():
        if input_path.suffix.lower() == ".doc":
            return [input_path]
        else:
            print(f"❌ 文件不是 .doc 格式: {input_path.name}")
            return []
    else:
        doc_files = [f for f in input_path.glob("*.doc") if not f.name.startswith("~$")]
        if not doc_files:
            print(f"⚠️ 在 {input_path} 中没有找到 .doc 文件")
        return doc_files


def batch_convert_doc_to_docx(input_path: Path):
    """批量转换 .doc 为 .docx"""
    doc_files = get_doc_files(input_path)
    if not doc_files:
        return

    output_dir = get_output_dir(input_path)

    print(f"\n📂 输入: {input_path}")
    print(f"📂 输出: {output_dir}")
    print(f"📁 找到 {len(doc_files)} 个 .doc 文件")
    print("-" * 50)

    # 启动 Word
    try:
        word = win32.gencache.EnsureDispatch("Word.Application")
        word.Visible = False
    except Exception as e:
        print(f"❌ 无法启动 Word: {e}")
        return

    success_count = 0
    fail_count = 0

    for i, doc_path in enumerate(doc_files, 1):
        output_path = output_dir / f"{doc_path.stem}.docx"

        if output_path.exists():
            print(f"[{i}/{len(doc_files)}] ⏭️  跳过（已存在）: {doc_path.name}")
            continue

        print(f"[{i}/{len(doc_files)}] 转换中: {doc_path.name}")

        try:
            doc = word.Documents.Open(str(doc_path.resolve()))
            doc.SaveAs2(str(output_path), FileFormat=16)
            doc.Close()
            print(f"    ✅ 成功: {output_path.name}")
            success_count += 1
        except Exception as e:
            print(f"    ❌ 失败: {doc_path.name}")
            print(f"    错误: {str(e)[:100]}")
            fail_count += 1

    word.Quit()

    print("-" * 50)
    print(f"✨ 转换完成！成功: {success_count}, 失败: {fail_count}")
    print(f"📂 文件保存在: {output_dir}")

    # 打开输出文件夹
    try:
        if platform.system() == "Windows":
            subprocess.Popen(f'explorer "{output_dir}"')
    except:
        pass


if __name__ == "__main__":
    print("=" * 50)
    print("📄 .doc 转 .docx 工具")
    print("=" * 50)
    print("支持: 单个 .doc 文件 或 包含 .doc 的文件夹")
    print("输出: 自动在输入路径下创建 'docx' 文件夹")
    print("-" * 50)

    if len(sys.argv) > 1:
        print("📌 已检测到拖拽的文件/文件夹")

    input_path = get_input_path()
    batch_convert_doc_to_docx(input_path)
