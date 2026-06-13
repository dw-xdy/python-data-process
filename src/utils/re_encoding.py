from pathlib import Path
import time
import chardet
import shutil


def convert_to_utf8(file_path: Path, backup=True) -> tuple:
    """改进版：通过双向转换验证编码正确性"""
    try:
        raw_data = file_path.read_bytes()

        # 检测编码
        detected = chardet.detect(raw_data)
        original_encoding = detected["encoding"]
        confidence = detected["confidence"]

        # 如果已经是 UTF-8 且置信度高，直接跳过（不显示任何信息）
        if (
            original_encoding
            and original_encoding.lower() in ["utf-8", "ascii"]
            and confidence > 0.9
        ):
            return False, original_encoding

        # 创建备份（只在需要转换时创建）
        if backup:
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            if not backup_path.exists():
                shutil.copy2(file_path, backup_path)

        # 验证函数：检查编码是否正确
        def verify_encoding(data, encoding):
            try:
                # 1. 原数据解码
                decoded = data.decode(encoding)
                # 2. 重新编码回原格式
                reencoded = decoded.encode(encoding)
                # 3. 比较是否与原数据一致
                if len(data) == len(reencoded):
                    return data == reencoded, decoded
                else:
                    return False, decoded
            except:
                return False, None

        # 尝试检测到的编码
        if original_encoding and confidence > 0.5:
            is_valid, content = verify_encoding(raw_data, original_encoding)
            if is_valid and content:
                # 验证通过，转换为 UTF-8
                file_path.write_text(content, encoding="utf-8")
                # 简化的提示信息，只显示文件名和转换方向
                print(f"✅ 转换: {file_path.name} ({original_encoding} -> utf-8)")
                return True, original_encoding

        # 尝试常见编码并验证
        common_encodings = ["gbk", "gb2312", "big5", "gb18030", "latin-1"]

        for encoding in common_encodings:
            is_valid, content = verify_encoding(raw_data, encoding)
            if is_valid and content:
                file_path.write_text(content, encoding="utf-8")
                print(f"✅ 转换: {file_path.name} ({encoding} -> utf-8)")
                return True, encoding

        # 无法验证时，选择解码错误最少的编码
        best_encoding = None
        best_content = None
        min_errors = float("inf")

        for encoding in common_encodings:
            try:
                content = raw_data.decode(encoding, errors="replace")
                error_count = content.count("�")
                if error_count < min_errors:
                    min_errors = error_count
                    best_encoding = encoding
                    best_content = content
            except:
                continue

        if best_content and min_errors < len(best_content) * 0.01:  # 错误少于1%
            file_path.write_text(best_content, encoding="utf-8")
            print(
                f"⚠️  转换: {file_path.name} ({best_encoding} -> utf-8, 有{min_errors}个字符无法识别)"
            )
            return True, best_encoding

        # 转换失败，如果有备份则恢复
        if backup:
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            if backup_path.exists():
                shutil.copy2(backup_path, file_path)
                backup_path.unlink()  # 删除备份文件
        print(f"❌ 无法转换: {file_path.name}")
        return False, None

    except Exception as e:
        print(f"❌ 转换失败 {file_path.name}: {e}")
        # 如果有备份，尝试恢复
        if backup:
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            if backup_path.exists():
                shutil.copy2(backup_path, file_path)
        return False, None


def convert_folder_to_utf8(folder_path: Path) -> tuple:
    """转换文件夹下所有 txt 文件为 UTF-8（自动检测原编码）"""
    start_time = time.perf_counter()
    converted_count = 0
    skipped_count = 0
    failed_count = 0
    converted_files = []
    encoding_stats = {}  # 统计各种编码的数量

    # 先统计总文件数
    total_files = len(list(folder_path.rglob("*.txt")))
    print(f"📁 扫描到 {total_files} 个 txt 文件\n")

    for txt_file in folder_path.rglob("*.txt"):
        success, original_encoding = convert_to_utf8(txt_file)
        if success:
            converted_count += 1
            converted_files.append(txt_file)
            encoding_stats[original_encoding] = (
                encoding_stats.get(original_encoding, 0) + 1
            )
        elif original_encoding:
            # 已经是 UTF-8，跳过
            skipped_count += 1
        else:
            failed_count += 1

    elapsed = time.perf_counter() - start_time

    # 显示干净的统计信息
    print(f"\n{'=' * 50}")
    print("📊 转换完成")
    print(f"  ✅ 转换: {converted_count} 个文件")
    print(f"  ⏭️  跳过: {skipped_count} 个文件 (已是 UTF-8)")
    if failed_count > 0:
        print(f"  ❌ 失败: {failed_count} 个文件")

    if encoding_stats:
        print("\n📈 原编码统计:")
        for encoding, count in sorted(
            encoding_stats.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {encoding}: {count} 个")

    print(f"⏱️  耗时: {elapsed:.4f} 秒")
    print(f"{'=' * 50}")
    return converted_count, converted_files


def clean_bak_files(folder_path: Path, silent=False):
    """
    递归删除指定文件夹下所有 .bak 备份文件

    Args:
        folder_path: 要清理的文件夹路径
        silent: 是否静默模式（不显示删除详情）

    Returns:
        删除的文件数量
    """
    if not folder_path.exists():
        print(f"❌ 文件夹不存在: {folder_path}")
        return 0

    # 递归查找所有 .bak 文件
    bak_files = list(folder_path.rglob("*.bak"))

    if not bak_files:
        if not silent:
            print("📭 没有找到任何 .bak 备份文件")
        return 0

    # 删除文件
    deleted_count = 0
    for bak_file in bak_files:
        try:
            bak_file.unlink()
            deleted_count += 1
            if not silent:
                print(f"🗑️  删除: {bak_file}")
        except Exception as e:
            print(f"❌ 删除失败 {bak_file}: {e}")

    if not silent:
        print(f"\n✅ 已删除 {deleted_count} 个 .bak 备份文件")

    return deleted_count


if __name__ == "__main__":
    folder_path = r"F:\备份\3_文档文件\小说"
    convert_folder_to_utf8(Path(folder_path))
    clean_bak_files(Path(folder_path))
