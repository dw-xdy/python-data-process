import os
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import glob
import sys
from loguru import logger as log
from datetime import datetime

"""
工具说明:
    将一个文件夹中的所有PDF转为PNG格式的图片.
    个人认为速度可以接受的, 测试结果: 1000页的PDF转图片(默认的200DPI)需要时间为58s
    后续应该还会继续优化的.  
"""


def pdf_to_images(pdf_path, output_folder, dpi=200):
    """
    将单个PDF文件转换为PNG图片

    参数:
        pdf_path: PDF文件路径
        output_folder: 输出文件夹
        dpi: 图片分辨率（默认200）
    """
    doc = None
    try:
        # 打开PDF文件
        doc = fitz.open(pdf_path)

        # 获取PDF文件名（不含扩展名）
        pdf_name = Path(pdf_path).stem

        # 遍历PDF每一页
        total_pages = len(doc)
        success_count = 0

        for page_num in range(total_pages):
            try:
                # 获取页面
                page = doc.load_page(page_num)

                # 设置缩放比例（根据DPI计算）
                zoom = dpi / 72
                mat = fitz.Matrix(zoom, zoom)

                # 渲染页面为图像
                pix = page.get_pixmap(matrix=mat, alpha=False)

                # 创建PIL Image对象
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

                # 构建输出文件名
                output_filename = f"{pdf_name}_page_{page_num + 1:03d}.png"
                output_path = os.path.join(output_folder, output_filename)

                # 保存图像
                img.save(output_path, "PNG", dpi=(dpi, dpi))
                success_count += 1
                print(
                    f"✓ 已保存第 {page_num + 1} / {total_pages} 页: {output_filename}"
                )

            except Exception as page_error:
                print(f"✗ 第 {page_num + 1} 页转换失败: {page_error}")
                continue

        # 安全地关闭文档
        if doc:
            doc.close()

        if success_count == total_pages:
            print(
                f"✅ 完成转换: {pdf_name}.pdf ({success_count} / {total_pages} 页全部成功)"
            )
        else:
            print(
                f"⚠️  部分完成: {pdf_name}.pdf ({success_count} / {total_pages} 页成功)"
            )

        return success_count, total_pages

    except Exception as e:
        print(f"✗ 文件打开失败 {pdf_path}: {e}")
        if doc:
            try:
                doc.close()
            except Exception as close_exception:
                print(f"文件关闭失败: {close_exception}")
        return 0, 0


def batch_pdf_to_png(input_folder, output_folder=None, dpi=200):
    """
    批量转换文件夹中的所有PDF文件

    参数:
        input_folder: 包含PDF的文件夹路径
        output_folder: 输出文件夹（默认为输入文件夹下的'png_output'）
        dpi: 图片分辨率d
    """
    # 设置输出文件夹
    if output_folder is None:
        output_folder = os.path.join(input_folder, "png_output")

    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    # 查找所有PDF文件
    pdf_files = glob.glob(os.path.join(input_folder, "*.pdf"))

    if not pdf_files:
        print(f"在文件夹 '{input_folder}' 中没有找到PDF文件")
        print("支持的文件格式: .pdf")
        return

    print(f"找到 {len(pdf_files)} 个PDF文件")
    print(f"输出文件夹: {output_folder}")
    print(f"分辨率: {dpi} DPI")
    print("-" * 50)

    total_success_pages = 0
    total_pages = 0
    total_success_files = 0

    # 处理每个PDF文件
    for pdf_file in pdf_files:
        print(f"\n正在处理: {os.path.basename(pdf_file)}")
        success, total = pdf_to_images(pdf_file, output_folder, dpi)

        total_success_pages += success
        total_pages += total
        if success > 0:
            total_success_files += 1

    print("\n" + "=" * 50)
    print("批量转换完成！")
    print(f"处理文件: {len(pdf_files)} 个")
    print(f"成功转换: {total_success_files} 个文件")
    print(f"页面统计: {total_success_pages}/{total_pages} 页成功")
    print(f"图片保存在: {output_folder}")

    # 显示输出文件夹内容
    png_files = glob.glob(os.path.join(output_folder, "*.png"))
    if png_files:
        print(f"生成PNG文件数量: {len(png_files)} 个")
    else:
        print("警告: 输出文件夹中没有找到PNG文件")


def main():
    """主函数：提供命令行交互界面"""
    print("=" * 50)
    print("PDF批量转换为PNG图片工具")
    print("=" * 50)

    # 获取输入文件夹
    input_folder = input("请输入包含PDF文件的文件夹路径: ").strip()

    # 检查文件夹是否存在
    if not os.path.exists(input_folder):
        print("错误：指定的文件夹不存在！")
        sys.exit(1)

    # 获取输出文件夹
    output_folder_input = input("请输入输出文件夹路径（直接回车使用默认）: ").strip()
    output_folder = output_folder_input if output_folder_input else None

    # 获取DPI设置
    dpi_input = input("请输入图片分辨率DPI（默认200，直接回车使用默认）: ").strip()
    try:
        dpi = int(dpi_input) if dpi_input else 200
    except ValueError:
        print("无效的DPI值，使用默认值200")
        dpi = 200

    print("\n开始转换...")
    print("-" * 50)

    start = int(datetime.now().timestamp())
    log.info(f"{start}s")

    # 执行批量转换
    batch_pdf_to_png(input_folder, output_folder, dpi)

    end = int(datetime.now().timestamp())
    log.info(f"{end}s")
    log.success(f"{end - start}s")

    input("\n按回车键退出...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
