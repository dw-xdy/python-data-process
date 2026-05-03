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
