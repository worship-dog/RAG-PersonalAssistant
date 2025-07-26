from app.utils.file_tools.read_docx_file import DocxReader
from app.utils.file_tools.read_md_file import MDReader
from app.utils.file_tools.read_pdf_file import PDFReader
from app.utils.file_tools.read_txt_file import TXTReader


def read_file(file_path: str, file_type: str):
    file_reader_map = {
        "docx": DocxReader,
        "pdf": PDFReader,
        "md": MDReader,
        "txt": TXTReader,
    }
    file_reader = file_reader_map.get(file_type)
    if file_reader:
        return file_reader().read(file_path)
    else:
        raise ValueError(f"不支持的文件类型: {file_type}")
