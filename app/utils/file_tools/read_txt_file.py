from app.utils.file_tools.read_file import FileReader


class TXTReader(FileReader):
    def __init__(self, file_path: str):
        super().__init__(file_path, "txt")

    def read(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return  content
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {str(e)}")
