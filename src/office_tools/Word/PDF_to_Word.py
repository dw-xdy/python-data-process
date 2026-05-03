import os
from pdf2docx import Converter

# 1. 设置文件夹路径（手动修改这两个路径）
pdf_folder = r"F:\备份\3_文档文件\小说\enough"  # PDF文件夹路径
output_folder = r"F:\备份\3_文档文件\小说\enough\word"  # 输出文件夹路径

# 2. 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 3. 获取所有PDF文件
pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

print(f"找到 {len(pdf_files)} 个PDF文件")

# 4. 批量转换
for pdf_file in pdf_files:
    # 构建完整路径
    pdf_path = os.path.join(pdf_folder, pdf_file)

    # 生成输出Word文件名（保持原名，只改扩展名）
    word_file = pdf_file.replace(".pdf", ".docx").replace(".PDF", ".docx")
    word_path = os.path.join(output_folder, word_file)

    try:
        # 创建转换器并转换
        cv = Converter(pdf_path)
        cv.convert(word_path, start=0, end=None)
        cv.close()

        print(f"✓ 已转换: {pdf_file} -> {word_file}")
    except Exception as e:
        print(f"✗ 转换失败 {pdf_file}: {str(e)}")

print("批量转换完成！")
