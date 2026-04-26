import os
import glob


def remove_specific_text(content):
    """删除文件中的特定文本块"""
    # 要删除的文本模式
    text_to_remove = """-----------------------------------
本文件来自尚香书苑。
发布页：sxsy.org
-----------------------------------"""

    # 直接替换为空字符串
    new_content = content.replace(text_to_remove, "")

    return new_content


def replace_quotes_in_file(file_path):
    """替换单个文件中的双引号为直角引号，并删除特定文本"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        original_content = content

        # 1. 删除特定文本
        content = remove_specific_text(content)

        # 2. 替换左双引号和右双引号为直角引号
        content = content.replace("“", "「").replace("”", "」")

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
    # 构建搜索模式（包括子文件夹）
    pattern = os.path.join(folder_path, "**/*.txt")
    txt_files = glob.glob(pattern, recursive=True)

    renamed_count = 0

    for file_path in txt_files:
        # 获取文件名和目录路径
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        # 删除文件名中的 [sxsy.org]
        new_filename = filename.replace("[sxsy.org]", "")
        new_filename = new_filename.replace("soushu2025.com@", "")

        # 如果文件名有变化
        if new_filename != filename:
            new_file_path = os.path.join(directory, new_filename)

            # 确保新文件名不会重复
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
            except Exception as e:
                print(f"重命名失败 {filename}: {e}")

    return renamed_count


def process_folder(folder_path):
    """处理文件夹下所有 .txt 文件"""
    # 1. 先重命名文件
    print("第一步：重命名文件...")
    renamed_count = rename_files(folder_path)
    print(f"完成重命名，共处理 {renamed_count} 个文件\n")

    # 2. 再处理文件内容
    print("第二步：处理文件内容...")
    pattern = os.path.join(folder_path, "**/*.txt")
    txt_files = glob.glob(pattern, recursive=True)

    if not txt_files:
        print(f"在 {folder_path} 中没有找到 .txt 文件")
        return

    print(f"找到 {len(txt_files)} 个 .txt 文件")
    processed_count = 0

    for file_path in txt_files:
        if replace_quotes_in_file(file_path):
            print(f"已处理内容: {file_path}")
            processed_count += 1
        else:
            print(f"无变化: {file_path}")

    print(f"\n完成！")
    print(f"- 重命名文件: {renamed_count} 个")
    print(f"- 修改内容: {processed_count} 个文件")


if __name__ == "__main__":
    # 请将此处替换为你的文件夹路径
    folder_path = input("请输入文件夹路径: ").strip()

    # 去除可能的引号
    folder_path = folder_path.strip('"').strip("'")

    if os.path.isdir(folder_path):
        print("注意：此操作会直接修改原文件和文件名，建议先备份！")
        confirm = input("是否继续？(y/n): ").strip().lower()
        if confirm == "y":
            process_folder(folder_path)
        else:
            print("操作已取消")
    else:
        print(f"错误：'{folder_path}' 不是一个有效的文件夹路径")
