from pathlib import Path
from pdf2docx import Converter


def batch_convert_pdfs_to_word(source_dir: Path, output_dir: Path):
    """批量将文件夹中的所有 PDF 转换为 Word"""
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(source_dir.glob("*.pdf"))
    print(f"找到 {len(pdf_files)} 个 PDF 文件")

    for pdf_path in pdf_files:
        output_path = output_dir / f"{pdf_path.stem}.docx"
        print(f"转换中: {pdf_path.name}")

        cv = Converter(str(pdf_path))
        cv.convert(str(output_path))
        cv.close()

    print(f"完成！文件保存在: {output_dir}")


if __name__ == "__main__":
    PDF_INPUT = r"F:\备份\3_文档文件\小说\enough"
    WORD_OUTPUT = r"F:\备份\3_文档文件\小说\enough"

    batch_convert_pdfs_to_word(Path(PDF_INPUT), Path(WORD_OUTPUT))
