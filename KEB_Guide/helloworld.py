import zipfile

zip_path = 'data.zip'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    # 解压所有文件到当前目录
    zip_ref.extractall("exttest")