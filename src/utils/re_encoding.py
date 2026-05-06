from pathlib import Path
import re
import time
import chardet


def convert_to_utf8(file_path: Path) -> tuple:
    """
    自动检测文件编码并转换为 UTF-8
    返回: (是否转换成功, 原编码)
    """
    try:
        # 读取二进制数据
        raw_data = file_path.read_bytes()

        # 检测编码
        detected = chardet.detect(raw_data)
        original_encoding = detected["encoding"]
        confidence = detected["confidence"]

        # 如果已经是 UTF-8 且置信度高，跳过
        if (
            original_encoding
            and original_encoding.lower() in ["utf-8", "ascii"]
            and confidence > 0.9
        ):
            return False, original_encoding

        # 尝试解码
        if original_encoding:
            try:
                content = raw_data.decode(original_encoding)
                # 转换为 UTF-8
                file_path.write_text(content, encoding="utf-8")
                print(
                    f"✅ 转换: {file_path.name} ({original_encoding} -> utf-8, 置信度: {confidence:.2%})"
                )
                return True, original_encoding
            except UnicodeDecodeError, LookupError:
                pass

        # 如果自动检测失败，尝试常见编码
        common_encodings = ["gbk", "gb2312", "big5", "utf-16", "utf-8", "latin-1"]
        for encoding in common_encodings:
            try:
                content = raw_data.decode(encoding)
                file_path.write_text(content, encoding="utf-8")
                print(
                    f"✅ 转换: {file_path.name} ({encoding} -> utf-8, 自动检测失败，使用备选编码)"
                )
                return True, encoding
            except UnicodeDecodeError, LookupError:
                continue

        print(f"⚠️  无法识别编码: {file_path.name}")
        return False, None

    except Exception as e:
        print(f"❌ 转换失败 {file_path.name}: {e}")
        return False, None


def convert_folder_to_utf8(folder_path: Path) -> tuple:
    """转换文件夹下所有 txt 文件为 UTF-8（自动检测原编码）"""
    start_time = time.perf_counter()
    converted_count = 0
    converted_files = []
    encoding_stats = {}  # 统计各种编码的数量

    for txt_file in folder_path.rglob("*.txt"):
        success, original_encoding = convert_to_utf8(txt_file)
        if success:
            converted_count += 1
            converted_files.append(txt_file)
            encoding_stats[original_encoding] = (
                encoding_stats.get(original_encoding, 0) + 1
            )

    elapsed = time.perf_counter() - start_time

    # 显示统计信息
    if encoding_stats:
        print("\n📊 编码统计:")
        for encoding, count in sorted(
            encoding_stats.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {encoding}: {count} 个文件")

    print(f"⏱️  编码转换耗时: {elapsed:.4f} 秒")
    return converted_count, converted_files


if __name__ == "__main__":
    folder_path = r"F:\备份\3_文档文件\小说"
    convert_folder_to_utf8(Path(folder_path))
