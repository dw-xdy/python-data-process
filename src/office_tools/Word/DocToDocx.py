import os
import win32com.client as win32
from tkinter import filedialog, Tk, messagebox
from pathlib import Path  # 添加这一行


def batch_convert():
    # 1. 初始化并隐藏 Tk 窗口
    root = Tk()
    root.withdraw()

    # 2. 交互逻辑：询问用户是想选"文件"还是"文件夹"
    # 虽然可以通过一个窗口实现，但为了逻辑清晰，建议先弹个简单的询问框
    mode = messagebox.askyesnocancel(
        "选择模式", "点击 [是/Yes] 选择多个文件\n点击 [否/No] 选择整个文件夹"
    )

    file_paths = []

    if mode is True:  # 用户选了"文件"
        file_paths = filedialog.askopenfilenames(
            title="请选择 .doc 文件（支持多选）",
            filetypes=[("Word 97-2003 文档", "*.doc")],
        )
    elif mode is False:  # 用户选了"文件夹"
        folder_selected = filedialog.askdirectory(title="请选择包含 .doc 文件的文件夹")
        if folder_selected:
            folder_path = Path(folder_selected)  # 转换为 Path 对象
            # 遍历文件夹下所有 .doc 文件
            file_paths = [
                str(folder_path / f.name)  # 使用 Path 拼接，然后转回字符串
                for f in folder_path.iterdir()
                if f.suffix.lower() == ".doc" and not f.name.startswith("~$")
            ]
    else:  # 用户点了取消
        return

    if not file_paths:
        print("未发现有效文件。")
        return

    # 3. 开始转换逻辑
    print(f"准备转换 {len(file_paths)} 个文件...")

    try:
        # 确保只启动一次 Word 进程以节省开销
        word = win32.gencache.EnsureDispatch("Word.Application")
        word.Visible = False

        success_count = 0
        for doc_path in file_paths:
            # 将字符串路径转为 Path 对象方便操作
            doc_path_obj = Path(doc_path)
            abs_path = str(doc_path_obj.resolve())  # 获取绝对路径字符串
            # 兼容处理：确保不会出现 .docxx 的情况
            base_path = str(doc_path_obj.with_suffix(""))  # 去掉扩展名
            docx_path = base_path + ".docx"

            try:
                doc = word.Documents.Open(abs_path)
                doc.SaveAs2(docx_path, FileFormat=16)
                doc.Close()
                success_count += 1
                print(f"已转换: {doc_path_obj.name}")  # 使用 .name 获取文件名
            except Exception as e:
                print(f"转换出错 {doc_path_obj.name}: {e}")

        word.Quit()
        messagebox.showinfo("完成", f"成功转换 {success_count} 个文件！")

    except Exception as e:
        messagebox.showerror("运行错误", f"无法启动 Word 或处理文件: {e}")


if __name__ == "__main__":
    batch_convert()
