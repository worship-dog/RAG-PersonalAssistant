from app.utils.file_tools.read_file import FileReader
import PyPDF2


class PDFReader(FileReader):

    def read(self, file_path):
        """
        读取所有PDF文件并返回内容列表
        :return: 包含所有PDF文件内容的列表
        """
        try:
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"读取PDF文件 {file_path} 时出错: {str(e)}")
