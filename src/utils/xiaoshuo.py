from pathlib import Path
import re
import time
from typing import Tuple, Optional

# 在函数外部编译正则表达式（模块级别，只编译一次）
# 1. 删除特定文本的模式
DELETE_PATTERN = re.compile(
    r"-----------------------------------\n+本文件来自尚香书[苑院]。\n+发布页：sxsy\.org\n+-----------------------------------\n?"
)

# 2. 替换引号为直角引号的模式
QUOTE_PATTERNS = [
    (re.compile(r'"(.*?)"', re.DOTALL), r"「\1」"),  # 双引号
    (re.compile(r"'(.*?)'", re.DOTALL), r"「\1」"),  # 单引号
    (re.compile(r"“(.*?)”", re.DOTALL), r"「\1」"),  # 中文左双引号
    (re.compile(r"‘(.*?)’", re.DOTALL), r"「\1」"),  # 中文左单引号
    (re.compile(r"＂(.*?)＂", re.DOTALL), r"「\1」"),  # 全角双引号
]

# 3. 处理完成的标记
FINISHED_MARKER = "_finished"

# 4. 排除的文件夹名称列表（不会处理这些文件夹及其子文件夹中的文件）
EXCLUDED_FOLDERS = ["不进行格式化操作"]  # 可以在这里添加更多要排除的文件夹名称


def has_finished_marker(filename: str) -> bool:
    """检查文件名是否已包含完成标记"""
    stem = Path(filename).stem
    return stem.endswith(FINISHED_MARKER)


def remove_finished_marker(filename: str) -> str:
    """从文件名中移除完成标记（用于显示原始文件名）"""
    stem = Path(filename).stem
    suffix = Path(filename).suffix

    if stem.endswith(FINISHED_MARKER):
        stem = stem[: -len(FINISHED_MARKER)]
    return f"{stem}{suffix}"


def clean_filename(filename: str) -> Tuple[str, bool]:
    """清理文件名中的广告标记，返回清理后的文件名和是否有变化"""
    original = filename
    cleaned = (
        filename.replace("[sxsy.org]", "")
        .replace("soushu2025.com@", "")
        .replace("搜书吧", "")
        .replace("sxsy_org", "")
        .replace("[]", "")
        .strip()
    )

    # 清理可能产生的多余空格或符号
    cleaned = re.sub(r"[_\s]+$", "", cleaned)  # 删除末尾的下划线和空格

    return cleaned, cleaned != original


def ensure_unique_filename(new_path: Path) -> Path:
    """如果目标文件已存在，添加数字后缀"""
    counter = 1
    original_new_path = new_path
    while new_path.exists():
        stem = original_new_path.stem
        suffix = original_new_path.suffix
        new_path = original_new_path.parent / f"{stem}_{counter}{suffix}"
        counter += 1
    return new_path


def add_finished_marker(file_path: Path) -> Optional[Path]:
    """为文件添加完成标记，返回新的文件路径，如果已存在则返回 None"""
    if has_finished_marker(file_path.name):
        return file_path  # 已经有标记了

    stem = file_path.stem
    suffix = file_path.suffix
    new_name = f"{stem}{FINISHED_MARKER}{suffix}"
    new_path = file_path.parent / new_name

    new_path = ensure_unique_filename(new_path)

    try:
        file_path.rename(new_path)
        return new_path
    except Exception as e:
        print(f"添加完成标记失败 {file_path.name}: {e}")
        return None


def replace_quotes_in_file(file_path: Path) -> bool:
    """替换单个文件中的不同的双引号为直角引号，并删除特定文本"""
    try:
        content = file_path.read_text(encoding="utf-8")
        origin_content = content

        content = DELETE_PATTERN.sub("", content)
        for pattern, replacement in QUOTE_PATTERNS:
            content = pattern.sub(replacement, content)
        content = content.replace("♥", "❤️").replace("♡", "❤️")

        # 若是内容有变化，则将其写回文件
        if content != origin_content:
            file_path.write_text(content, encoding="utf-8")
            return True
        return False
    except Exception as e:
        print(f"处理文件 {file_path} 内容时出错: {e}")
        return False


def process_single_file(
    file_path: Path, add_marker: bool = True
) -> Tuple[bool, bool, Optional[Path]]:
    """
    处理单个文件
    返回: (内容是否修改, 是否重命名, 最终文件路径)
    """
    # 如果已经有完成标记，跳过处理
    if has_finished_marker(file_path.name):
        print(f"  ⏭️  跳过已处理的文件: {file_path.name}")
        return False, False, file_path

    # 1. 先清理文件名（移除广告标记）
    old_name = file_path.name
    cleaned_name, name_changed = clean_filename(old_name)

    if name_changed:
        new_path = file_path.parent / cleaned_name

        new_path = ensure_unique_filename(new_path)

        try:
            file_path.rename(new_path)
            file_path = new_path
            print(f"  📝 重命名: {old_name} -> {file_path.name}")
        except Exception as e:
            print(f"  ❌ 重命名失败 {old_name}: {e}")
            return False, False, file_path

    # 2. 处理文件内容
    content_modified = replace_quotes_in_file(file_path)
    if content_modified:
        print(f"  ✏️  修改内容: {file_path.name}")

    # 3. 添加完成标记
    final_path = file_path
    if add_marker and not has_finished_marker(file_path.name):
        marked_path = add_finished_marker(file_path)
        if marked_path:
            final_path = marked_path
            print(f"  ✅ 添加完成标记: {file_path.name} -> {final_path.name}")

    return content_modified, name_changed, final_path


def process_folder(folder_path_str: str, add_marker: bool = True):
    """
    处理文件夹下所有 .txt 文件

    Args:
        folder_path_str: 文件夹路径
        add_marker: 是否添加完成标记
    """
    folder_path = Path(folder_path_str).resolve()

    if not folder_path.is_dir():
        print(f"错误：'{folder_path}' 不是一个有效的文件夹路径")
        return

    total_start = time.perf_counter()

    # 获取所有 txt 文件（包括排除文件夹中的）
    all_txt_files = list(folder_path.rglob("*.txt"))

    # 分离文件：需要完整处理的 vs 只处理文件名的
    full_process_files = []  # 完整处理（内容+文件名）
    name_only_files = []  # 只处理文件名

    for file_path in all_txt_files:
        # 检查是否在排除文件夹中
        if any(excluded in file_path.parent.parts for excluded in EXCLUDED_FOLDERS):
            name_only_files.append(file_path)
        else:
            full_process_files.append(file_path)

    # 从完整处理中排除已标记的文件
    full_process_files = [
        f for f in full_process_files if not has_finished_marker(f.name)
    ]

    # 从只处理文件名中排除已标记的文件
    name_only_files = [f for f in name_only_files if not has_finished_marker(f.name)]

    # 合并所有需要处理文件名的文件
    all_files_to_rename = full_process_files + name_only_files

    # 统计信息
    excluded_count = len(
        [
            f
            for f in all_txt_files
            if any(excluded in f.parent.parts for excluded in EXCLUDED_FOLDERS)
        ]
    )
    skipped_marked_count = len(all_txt_files) - len(
        [f for f in all_txt_files if not has_finished_marker(f.name)]
    )

    if not all_files_to_rename:
        if excluded_count > 0:
            print(
                f"📁 在排除文件夹中找到 {excluded_count} 个文件（仅处理文件名，但都已标记完成）"
            )

        if skipped_marked_count > 0:
            print(f"📁 所有 {skipped_marked_count} 个文件都已处理完成，无需重复处理")
        else:
            print(f"在 {folder_path} 中没有找到 .txt 文件")
        return

    print(f"📁 找到 {len(all_files_to_rename)} 个需要处理文件名的文件")
    if excluded_count > 0:
        print(
            f"📝 其中 {len(name_only_files)} 个文件在排除文件夹中（仅重命名，不修改内容）"
        )
    if skipped_marked_count > 0:
        print(f"⏭️  跳过 {skipped_marked_count} 个已处理的文件")
    print()

    # 处理文件
    modified_content_count = 0
    renamed_count = 0
    processed_files = []
    failed_files = []

    for i, file_path in enumerate(all_files_to_rename, 1):
        # 判断是否在排除文件夹中
        is_excluded = any(
            excluded in file_path.parent.parts for excluded in EXCLUDED_FOLDERS
        )

        if is_excluded:
            print(
                f"[{i}/{len(all_files_to_rename)}] 处理（仅重命名）: {file_path.name}"
            )
        else:
            print(f"[{i}/{len(all_files_to_rename)}] 处理: {file_path.name}")

        # 处理文件名
        old_name = file_path.name
        cleaned_name, name_changed = clean_filename(old_name)

        current_path = file_path

        if name_changed:
            new_path = current_path.parent / cleaned_name
            new_path = ensure_unique_filename(new_path)

            try:
                current_path.rename(new_path)
                current_path = new_path
                print(f"  📝 重命名: {old_name} -> {current_path.name}")
                renamed_count += 1
            except Exception as e:
                print(f"  ❌ 重命名失败 {old_name}: {e}")
                failed_files.append(file_path)
                print()
                continue

        if not is_excluded:
            content_modified = replace_quotes_in_file(current_path)
            if content_modified:
                print(f"  ✏️  修改内容: {current_path.name}")
                modified_content_count += 1
        else:
            print("  ⏭️  跳过内容修改（在排除文件夹中）")

        # 添加完成标记（所有文件都添加）
        final_path = current_path
        if add_marker and not has_finished_marker(current_path.name):
            marked_path = add_finished_marker(current_path)
            if marked_path:
                final_path = marked_path
                print(f"  ✅ 添加完成标记: {current_path.name} -> {final_path.name}")

        if final_path:
            processed_files.append((file_path, final_path))

        print()

    total_elapsed = time.perf_counter() - total_start

    # 输出统计信息
    print("\n" + "=" * 50)
    print("📊 处理完成统计")
    print("=" * 50)
    print(f"✅ 成功处理: {len(processed_files)} 个文件")
    if failed_files:
        print(f"❌ 处理失败: {len(failed_files)} 个文件")
        for f in failed_files:
            print(f"   - {f.name}")

    print("\n📈 详细统计:")
    print(f"   - 重命名文件: {renamed_count} 个")
    print(
        f"   - 修改内容: {modified_content_count} 个文件（排除文件夹中的文件不修改内容）"
    )
    print(f"   - 排除文件夹中的文件: {len(name_only_files)} 个（仅重命名）")
    print(f"   - 添加完成标记: {len(processed_files)} 个文件" if add_marker else "")
    print(f"   - 总耗时: {total_elapsed:.4f} 秒")
    print("=" * 50 + "\n")

    return processed_files, failed_files


def remove_finished_markers(folder_path_str: str):
    """
    移除所有文件的 _finished 标记（用于重新处理）

    Args:
        folder_path_str: 文件夹路径
    """
    folder_path = Path(folder_path_str).resolve()

    if not folder_path.is_dir():
        print(f"错误：'{folder_path}' 不是一个有效的文件夹路径")
        return

    finished_files = [
        f for f in folder_path.rglob("*.txt") if has_finished_marker(f.name)
    ]

    if not finished_files:
        print("没有找到带有 _finished 标记的文件")
        return

    print(f"找到 {len(finished_files)} 个带有标记的文件")

    for file_path in finished_files:
        new_name = remove_finished_marker(file_path.name)
        new_path = file_path.parent / new_name

        new_path = ensure_unique_filename(new_path)

        try:
            file_path.rename(new_path)
            print(f"  ✅ 移除标记: {file_path.name} -> {new_path.name}")
        except Exception as e:
            print(f"  ❌ 失败 {file_path.name}: {e}")


if __name__ == "__main__":
    folder_path = r"F:\备份\3_文档文件\小说"
    folder_path = folder_path.strip('"').strip("'")

    if Path(folder_path).is_dir():
        print("开始执行...\n")

        # 若是重新处理文件，可以移除标记之后处理:
        # remove_finished_markers(folder_path)

        process_folder(folder_path, add_marker=True)

    else:
        print(f"错误：'{folder_path}' 不是一个有效的文件夹路径")
