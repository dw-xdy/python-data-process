import os
import glob
import re
import time

# 在函数外部编译正则表达式（模块级别，只编译一次）
# 1. 删除特定文本的模式
DELETE_PATTERN = re.compile(
    r"-----------------------------------\n本文件来自尚香书[苑院]。\n发布页：sxsy\.org\n-----------------------------------\n?"
)

# 2. 替换双引号为直角引号的模式
QUOTE_PATTERN = re.compile(r'[“"＂](.*?)[”"＂]')


def replace_quotes_in_file(file_path):
    """替换单个文件中的不同的双引号为直角引号，并删除特定文本"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        original_content = content

        # 1. 删除特定文本
        content = DELETE_PATTERN.sub("", content)

        # 2. 替换双引号为直角引号
        content = QUOTE_PATTERN.sub(r"「\1」", content)

        # 如果内容有变化，则写回文件
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            return True
        return False
    except Exception as e:
        print(f"处理文件 {file_path} 内容时出错: {e}")
        return False


def rename_files(folder_path):
    """重命名文件，删除文件名中的 [sxsy.org]"""
    start_time = time.perf_counter()

    pattern = os.path.join(folder_path, "**/*.txt")
    txt_files = glob.glob(pattern, recursive=True)

    renamed_count = 0
    renamed_files = []  # 记录重命名的文件

    for file_path in txt_files:
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        new_filename = (
            filename.replace("[sxsy.org]", "")
            .replace("soushu2025.com@", "")
            .replace("搜书吧", "")
            .replace("sxsy_org", "")
            .replace("[]", "")
        )

        if new_filename != filename:
            new_file_path = os.path.join(directory, new_filename)

            counter = 1
            original_new_path = new_file_path
            while os.path.exists(new_file_path):
                name, ext = os.path.splitext(original_new_path)
                new_file_path = f"{name}_{counter}{ext}"
                counter += 1

            try:
                os.rename(file_path, new_file_path)
                print(f"重命名: {filename} -> {os.path.basename(new_file_path)}")
                renamed_count += 1
                renamed_files.append((filename, os.path.basename(new_file_path)))
            except Exception as e:
                print(f"重命名失败 {filename}: {e}")

    elapsed = time.perf_counter() - start_time
    print(f"⏱️  重命名文件耗时: {elapsed:.4f} 秒")
    return renamed_count, renamed_files


def process_folder(folder_path):
    """处理文件夹下所有 .txt 文件"""
    total_start = time.perf_counter()

    # 1. 先重命名文件
    print("第一步：重命名文件...")
    renamed_count, renamed_files = rename_files(folder_path)
    if renamed_count == 0:
        print("没有文件需要重命名")
    print(f"完成重命名，共处理 {renamed_count} 个文件\n")

    # 2. 再处理文件内容
    print("第二步：处理文件内容...")
    content_start = time.perf_counter()

    pattern = os.path.join(folder_path, "**/*.txt")
    txt_files = glob.glob(pattern, recursive=True)

    if not txt_files:
        print(f"在 {folder_path} 中没有找到 .txt 文件")
        return

    print(f"找到 {len(txt_files)} 个 .txt 文件")
    processed_count = 0
    modified_files = []  # 记录修改了内容的文件

    for file_path in txt_files:
        if replace_quotes_in_file(file_path):
            print(f"修改内容: {file_path}")
            processed_count += 1
            modified_files.append(file_path)

    content_elapsed = time.perf_counter() - content_start
    print(f"⏱️  处理文件内容耗时: {content_elapsed:.4f} 秒")

    total_elapsed = time.perf_counter() - total_start

    print("\n📊 ========== 修改汇总 ==========")
    if renamed_files:
        print("\n重命名的文件:")
        for old_name, new_name in renamed_files:
            print(f"  {old_name} -> {new_name}")
    else:
        print("\n重命名的文件: 无")

    if modified_files:
        print("\n修改了内容的文件:")
        for file_path in modified_files:
            print(f"  {file_path}")
    else:
        print("\n修改了内容的文件: 无")

    print("\n📈 ========== 统计信息 ==========")
    print(f"- 重命名文件: {renamed_count} 个")
    print(f"- 修改内容: {processed_count} 个文件")
    print(f"- 总耗时: {total_elapsed:.4f} 秒")
    print("================================\n")


if __name__ == "__main__":
    # 请将此处替换为你的文件夹路径
    folder_path = r"F:\备份\3_文档文件\小说"

    # 去除可能的引号
    folder_path = folder_path.strip('"').strip("'")

    if os.path.isdir(folder_path):
        print("注意：此操作会直接修改原文件和文件名，建议先备份！")
        print("开始执行...\n")
        program_start = time.perf_counter()
        process_folder(folder_path)
        program_elapsed = time.perf_counter() - program_start
        print(f"⏱️  程序总运行时间: {program_elapsed:.4f} 秒")
    else:
        print(f"错误：'{folder_path}' 不是一个有效的文件夹路径")
