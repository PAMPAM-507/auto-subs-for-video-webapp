import os
from typing import NoReturn

class RemoveAllHelpingFiles:
    
    @staticmethod
    def remove(path: str, base_filename: str) -> NoReturn:
        """
        Deletes all files with a specific base name at the specified path.
        
        :param path: The path to the directory where you want to delete files.
        :param base_filename: The base name of the files to delete (without extension).
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