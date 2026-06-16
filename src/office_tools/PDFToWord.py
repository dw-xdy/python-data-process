from pathlib import Path
from pdf2docx import Converter
import traceback
import sys
import subprocess
import platform


def normalize_path(path_str):
    """标准化路径，处理各种输入格式"""
    # 去除首尾空格和引号
    path_str = path_str.strip().strip('"').strip("'")
    # 将反斜杠替换为正斜杠
    path_str = path_str.replace("\\", "/")
    return path_str


def get_input_path() -> Path:
    """获取输入路径（支持文件或文件夹，支持拖拽）"""
    # 检查是否有拖拽的路径（命令行参数）
    if len(sys.argv) > 1:
        # 处理拖拽的路径（可能多个，取第一个）
        for arg in sys.argv[1:]:
            path_str = normalize_path(arg)
            path = Path(path_str)
            if path.exists():
                print(f"📌 检测到拖拽路径: {path}")
                return path
            else:
                print(f"⚠️ 拖拽路径不存在: {path_str}")

    # 没有拖拽或拖拽路径无效，手动输入
    while True:
        print("\n提示：可以直接拖拽文件或文件夹到此窗口，然后按 Enter")
        path_str = input("请输入PDF文件或文件夹路径: ").strip()

        # 处理可能的拖拽引号
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
    """
    自动生成输出目录
    - 如果是文件：在文件所在目录创建 'word' 文件夹
    - 如果是文件夹：在该文件夹内创建 'word' 文件夹
    """
    if input_path.is_file():
        # 文件：在文件所在目录下创建 word 文件夹
        output_dir = input_path.parent / "word"
    else:
        # 文件夹：在该文件夹内创建 word 文件夹
        output_dir = input_path / "word"

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_pdf_files(input_path: Path) -> list:
    """
    获取要转换的PDF文件列表
    - 如果是文件：返回该文件（如果是PDF的话）
    - 如果是文件夹：返回文件夹内所有PDF文件
    """
    if input_path.is_file():
        if input_path.suffix.lower() == ".pdf":
            return [input_path]
        else:
            print(f"❌ 文件不是PDF格式: {input_path.name}")
            return []
    else:
        # 文件夹：查找所有PDF文件
        pdf_files = list(input_path.glob("*.pdf"))
        if not pdf_files:
            print(f"⚠️ 在 {input_path} 中没有找到 PDF 文件")
        return pdf_files


def batch_convert_pdfs_to_word(input_path: Path):
    """批量转换PDF为Word（自动处理文件或文件夹）"""

    # 获取要转换的PDF文件列表
    pdf_files = get_pdf_files(input_path)
    if not pdf_files:
        return

    # 自动生成输出目录
    output_dir = get_output_dir(input_path)

    print(f"\n📂 输入: {input_path}")
    print(f"📂 输出: {output_dir}")
    print(f"📁 找到 {len(pdf_files)} 个 PDF 文件")
    print("-" * 50)

    success_count = 0
    fail_count = 0

    for i, pdf_path in enumerate(pdf_files, 1):
        output_path = output_dir / f"{pdf_path.stem}.docx"

        # 检查输出文件是否已存在
        if output_path.exists():
            print(f"[{i}/{len(pdf_files)}] ⏭️  跳过（已存在）: {pdf_path.name}")
            continue

        print(f"[{i}/{len(pdf_files)}] 转换中: {pdf_path.name}")

        try:
            cv = Converter(str(pdf_path))
            cv.convert(str(output_path))
            cv.close()
            print(f"    ✅ 成功: {output_path.name}")
            success_count += 1
        except Exception as e:
            print(f"    ❌ 失败: {pdf_path.name}")
            print(f"    错误: {str(e)[:100]}")
            fail_count += 1
            traceback.print_exc()

    print("-" * 50)
    print(f"✨ 转换完成！成功: {success_count}, 失败: {fail_count}")
    print(f"📂 文件保存在: {output_dir}")

    # 打开输出文件夹
    if platform.system() == "Windows":
        subprocess.Popen(f'explorer "{output_dir}"')


if __name__ == "__main__":
    print("=" * 50)
    print("📄 PDF 转 Word 工具")
    print("=" * 50)
    print("支持: 单个PDF文件 或 包含PDF的文件夹")
    print("输出: 自动在输入路径下创建 'word' 文件夹")
    print("-" * 50)

    # 显示拖拽提示
    if len(sys.argv) > 1:
        print("📌 已检测到拖拽的文件/文件夹")

    input_path = get_input_path()

    batch_convert_pdfs_to_word(input_path)
