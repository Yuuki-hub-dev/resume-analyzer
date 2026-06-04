"""
简历解析模块
支持 PDF 和 Word 格式的简历文本提取
"""

import re
from PyPDF2 import PdfReader
from docx import Document


def parse_pdf(file_path):
    """
    解析 PDF 文件，提取文本内容
    参数: file_path - PDF文件路径
    返回: 提取的文本内容
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        return f"PDF解析错误: {str(e)}"


def parse_docx(file_path):
    """
    解析 Word 文件，提取文本内容
    参数: file_path - Word文件路径
    返回: 提取的文本内容
    """
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Word解析错误: {str(e)}"


def clean_text(text):
    """
    清洗文本内容
    - 去除多余空行
    - 去除首尾空格
    - 合并多个空格为单个空格
    """
    if not text:
        return ""

    # 去除多余空行（将连续多个换行替换为单个换行）
    text = re.sub(r'\n\s*\n', '\n', text)

    # 去除首尾空格
    text = text.strip()

    # 合并多个空格为单个空格（但保留换行符）
    text = re.sub(r' +', ' ', text)

    return text


def parse_resume(file_path, file_type):
    """
    根据文件类型调用对应的解析函数
    参数:
        file_path - 文件路径
        file_type - 文件类型 ('pdf' 或 'docx')
    返回: 清洗后的文本内容
    """
    if file_type == 'pdf':
        raw_text = parse_pdf(file_path)
    elif file_type == 'docx':
        raw_text = parse_docx(file_path)
    else:
        return "不支持的文件格式"

    cleaned_text = clean_text(raw_text)
    return cleaned_text


# 测试代码（开发时使用）
if __name__ == "__main__":
    # 测试PDF解析
    # text = parse_resume("test.pdf", "pdf")
    # print(text[:500])
    pass