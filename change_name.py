import os

folder_path = 'D:/samples_luzhou/0326/Labels'

def rename_files(folder_path):
    files = os.listdir(folder_path)
    for index, file_name in enumerate(files):
        file_path = os.path.join(folder_path, file_name)
        _, file_extension = os.path.splitext(file_name)
        new_file_name = f"{index + 16651}_{file_extension}"
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(file_path, new_file_path)
        print(f"Renamed: '{file_path}' -> '{new_file_path}'")

rename_files(folder_path)