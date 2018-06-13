from os import listdir, remove
import os.path
import Constants

def delete_aux_files(path):
    files = listdir(path)
    for file in files:
        if file.endswith('.aux'):
            remove(path + '/' + file)

def delete_everything_but_tex_and_pdf(path):
    files = listdir(path)
    for file in files:
        if not(file.endswith('.tex') or file.endswith('.pdf') or file.endswith('.txt') or os.path.isdir(path + '/' + file)):
            remove(path + '/' + file)

def delete_files_by_extensions(path: str, extensions: []):
    files = listdir(path)
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                remove(path + '/' + file)

delete_files_by_extensions(Constants.study_docs_path + '/Praca magisterska', Constants.latex_output)