import os
from typing import NoReturn

class RemoveAllHelpingFiles:
    
    @staticmethod
    def remove(path: str, base_filename: str) -> NoReturn:
        """
        Удаляет все файлы с определённым базовым именем по указанному пути.
        
        :param path: Путь к директории, где необходимо удалить файлы.
        :param base_filename: Базовое имя файлов для удаления (без расширения).
        """
        if not os.path.exists(path):
            print(f"Путь {path} не существует.")
            return

        files = os.listdir(path)

        for file in files:
            if file.split('.')[0] == base_filename:
                file_path = os.path.join(path, file)
                try:
                    os.remove(file_path)
                    print(f"Файл {file_path} успешно удалён.")
                except Exception as e:
                    print(f"Ошибка при удалении файла {file_path}: {e}")