import zipfile
import os

def unzip(directory):
    done = False
    to_unzip = [file for file in os.listdir(directory) if file.endswith('.zip')]
    for file in to_unzip:
        with zipfile.ZipFile(directory+'/'+file, 'r') as zip_ref:
            zip_ref.extractall(directory)
        try:
            directory1 = file.strip('.zip')
            to_unzip2 = [file for file in os.listdir() if file.endswith('.zip')]
            for file in to_unzip2:
                with zipfile.ZipFile(directory1+'/'+file, 'r') as zip_ref:
                    zip_ref.extractall(directory1)
                try:
                    directory2 = file.strip('.zip')
                    to_unzip3 = [file for file in os.listdir(directory) if file.endswith('.zip')]
                    for file in to_unzip3:
                        with zipfile.ZipFile(directory+'/'+file, 'r') as zip_ref:
                            zip_ref.extractall(directory)    
                except:
                    pass
        except:
            pass
