from pathlib import Path
from pdf2docx import Converter

# 1. 设置文件夹路径
pdf_folder = Path(r"F:\备份\3_文档文件\小说\enough")
output_folder = pdf_folder / "word"  # 更简洁的方式

# 2. 创建输出文件夹（parents=True 可创建多级目录，exist_ok=True 避免异常）
output_folder.mkdir(parents=True, exist_ok=True)

# 3. 获取所有PDF文件（使用 glob 更直观）
pdf_files = list(pdf_folder.glob("*.pdf")) + list(pdf_folder.glob("*.PDF"))

print(f"找到 {len(pdf_files)} 个PDF文件")

# 4. 批量转换
for pdf_path in pdf_files:  # pdf_path 已经是 Path 对象了
    # 直接使用 stem 属性获取文件名（不含扩展名）
    word_path = output_folder / f"{pdf_path.stem}.docx"

    try:
        cv = Converter(str(pdf_path))
        cv.convert(str(word_path), start=0)
        cv.close()
        print(f"✓ 已转换: {pdf_path.name} -> {word_path.name}")
    except Exception as e:
        print(f"✗ 转换失败 {pdf_path.name}: {str(e)}")

print("批量转换完成！")
