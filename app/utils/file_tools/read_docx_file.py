from app.utils.file_tools.read_file import FileReader
import docx


class DocxReader(FileReader):

    def read(self, file_path):
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            print(f"读取DOCX文件 {file_path} 时出错: {str(e)}")
