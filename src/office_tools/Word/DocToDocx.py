# import os
# import win32com.client as win32
# import tkinter as tk
# from tkinter import filedialog, messagebox
#
#
# def convert_selected_files():
#     # 1. 初始化 Tkinter 并隐藏主窗口
#     root = tk.Tk()
#     root.withdraw()
#
#     # 2. 弹出 Windows 资源管理器选择文件
#     # title: 对话框标题
#     # filetypes: 限制只能选择 .doc 文件
#     file_paths = filedialog.askopenfilenames(
#         title="请选择要转换的 .doc 文件",
#         filetypes=[("Word 97-2003 文档", "*.doc")]
#     )
#
#     if not file_paths:
#         print("未选择任何文件。")
#         return
#
#     print(f"已选择 {len(file_paths)} 个文件，准备开始转换...")
#
#     # 3. 启动 Word 进程
#     word = win32.gencache.EnsureDispatch('Word.Application')
#     word.Visible = False
#
#     success_count = 0
#     for doc_path in file_paths:
#         # 将路径转换为 Windows 绝对路径
#         doc_path = os.path.abspath(doc_path)
#         docx_path = doc_path + "x"
#
#         try:
#             doc = word.Documents.Open(doc_path)
#             doc.SaveAs2(docx_path, FileFormat=16)  # 16 代表 docx
#             doc.Close()
#             success_count += 1
#             print(f"成功: {os.path.basename(doc_path)}")
#         except Exception as e:
#             print(f"失败 {os.path.basename(doc_path)}: {e}")
#
#     word.Quit()
#
#     print("转换成功")
#
# if __name__ == "__main__":
#     convert_selected_files()
#
#


# 关于这个代码, 这个算是一个优化行为吧, 这个代码将来再看. 现在并不是非常着急.
import os
import win32com.client as win32
from tkinter import filedialog, Tk, messagebox


def batch_convert():
    # 1. 初始化并隐藏 Tk 窗口
    root = Tk()
    root.withdraw()

    # 2. 交互逻辑：询问用户是想选“文件”还是“文件夹”
    # 虽然可以通过一个窗口实现，但为了逻辑清晰，建议先弹个简单的询问框
    mode = messagebox.askyesnocancel(
        "选择模式", "点击 [是/Yes] 选择多个文件\n点击 [否/No] 选择整个文件夹"
    )

    file_paths = []

    if mode is True:  # 用户选了“文件”
        file_paths = filedialog.askopenfilenames(
            title="请选择 .doc 文件（支持多选）",
            filetypes=[("Word 97-2003 文档", "*.doc")],
        )
    elif mode is False:  # 用户选了“文件夹”
        folder_selected = filedialog.askdirectory(title="请选择包含 .doc 文件的文件夹")
        if folder_selected:
            # 遍历文件夹下所有 .doc 文件
            file_paths = [
                os.path.join(folder_selected, f)
                for f in os.listdir(folder_selected)
                if f.lower().endswith(".doc") and not f.startswith("~$")
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
            abs_path = os.path.abspath(doc_path)
            # 兼容处理：确保不会出现 .docxx 的情况
            base_path = os.path.splitext(abs_path)[0]
            docx_path = base_path + ".docx"

            try:
                doc = word.Documents.Open(abs_path)
                doc.SaveAs2(docx_path, FileFormat=16)
                doc.Close()
                success_count += 1
                print(f"已转换: {os.path.basename(docx_path)}")
            except Exception as e:
                print(f"转换出错 {os.path.basename(abs_path)}: {e}")

        word.Quit()
        messagebox.showinfo("完成", f"成功转换 {success_count} 个文件！")

    except Exception as e:
        messagebox.showerror("运行错误", f"无法启动 Word 或处理文件: {e}")


if __name__ == "__main__":
    batch_convert()
