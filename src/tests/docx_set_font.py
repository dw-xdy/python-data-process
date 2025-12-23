from docx import Document
from docx.shared import Pt  # 用于设置字号
from docx.oxml.ns import qn  # 用于处理底层 XML 命名空间

doc = Document(r"C:\Users\asus\Desktop\学校作业\kaishi\信息论复习手册.docx")

for para in doc.paragraphs:
    for run in para.runs:
        # 1. 设置西文字体 (如 Arial, Times New Roman)
        run.font.name = '微软雅黑'

        # 2. 设置中文字体 (必须步骤)
        # 这一步是直接修改 Word 底层的 XML 标签，强制指定东亚字体
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '霞鹜文楷')

        # 3. 设置字号 (例如 12磅，相当于小四)
        run.font.size = Pt(12)

        # 4. 设置加粗 (可选)
        run.font.bold = True

doc.save(r"C:\Users\asus\Desktop\学校作业\kaishi\信息论复习手册.docx")