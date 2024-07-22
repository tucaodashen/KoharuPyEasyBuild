import os
import platform
import ast
import subprocess


def extract_imports_from_file(file_path):
    """从文件中提取所有导入的模块名"""
    imports = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
    return imports


def get_all_py_files(directory):
    """获取指定目录下所有的.py文件路径"""
    py_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files


def extract_imports_from_directory(directory):
    """从指定目录下所有的.py文件中提取导入的模块名"""
    all_imports = set()
    py_files = get_all_py_files(directory)
    for file in py_files:
        file_imports = extract_imports_from_file(file)
        all_imports.update(file_imports)
    return list(set(all_imports))

def execute_cmd(cmd):
    # 使用subprocess.run来执行命令
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # 输出命令的返回结果
    return result.stdout

def nuitka_plugin_filter():
    supportlist = execute_cmd("nuitka --plugin-list")


def setupwindows() -> None:
    state = os.system("pip install pillow")
    print(state)


if __name__ == "__main__":
    imports = extract_imports_from_directory("D:\invisible_video_watermark")
    print(imports)
