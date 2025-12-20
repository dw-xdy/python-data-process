import os
import shutil


"""
这个代码的意义在于: 需要将一个文件夹中的很多个零散的文件复制到另一个文件夹中.
"""


def copy_specified_files():
    # 定义文件列表
    file_list = []

    # 定义路径  这里'r' 表示: 按照字符串原始的方式处理. (而不是转义字符).
    source_dir = r"C:\Users\asus\Desktop\学校作业\water"
    target_dir = r"C:\Users\asus\Desktop\学校作业\kaishi"

    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"创建目标目录: {target_dir}")

    # 复制文件
    copied_count = 0
    missing_files = []

    for filename in file_list:
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)

        if os.path.exists(source_path):
            try:
                shutil.copy2(source_path, target_path)
                print(f"已复制: {filename}")
                copied_count += 1
            except Exception as e:
                print(f"复制失败 {filename}: {e}")
        else:
            missing_files.append(filename)
            print(f"文件不存在: {filename}, 请检查文件!!!")

    # 输出结果摘要
    print(f"\n=== 复制完成 ===")
    print(f"成功复制文件: {copied_count} 个")
    print(f"缺失文件: {len(missing_files)} 个")

    if missing_files:
        print("缺失的文件列表:")
        for file in missing_files:
            print(f"  - {file}")


# 运行程序
if __name__ == "__main__":
    copy_specified_files()
