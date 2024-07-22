import os
import platform
import ast
import subprocess

NuPluginFilter = {
    "anti-bloat": [],
    "data-files": [],
    "delvewheel": [],
    "dill-compat": ["dill"],
    "dll-files": ["os"],
    "enum-compat": ["enum"],
    "eventlet": ["eventlet", "dns"],
    "gevent": ["gevent"],
    "gi": ["typelib"],
    "glfw": ["pyopengl", "glfw"],
    "implicit-imports": [],
    "kivy": ["kivy"],
    "matplotlib": ["matplotlib"],
    "multiprocessing": ["multiprocessing"],
    "no-qt": [],
    "options-nanny": [],
    "pbr-compat":["pbr"],
    "pkg-resources":["pkg_resources"],
    "pmw-freezer":["Pmw"],
    "pylint-warnings":[],
    "pyqt5":["PyQt5"],
    "pyqt6":["PyQt6"],
    "pyside2":["PySide2"],
    "pyside6":["PySide6"],
    "pywebview":["pywebview"],
    "tk-inter":["tkinter"],
    "transformers":["transformers"],
    "upx":[]
}


def extract_imports_from_file(file_path):
    """从文件中提取所有导入的模块名"""
    imports = set()
    ire = []
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
    if imports != []:
        for i in imports:
            curr = i.split(".")
            ire += curr
    return list(set(ire))


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
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout


def nuitka_plugin_filter(package_info):
    adding_list=[]
    for add in NuPluginFilter.keys():
        for sub in NuPluginFilter[add]:
            for i in package_info:
                if i == sub:
                    adding_list.append(add)


    return adding_list


def setupwindows() -> None:
    state = os.system("pip install pillow")
    print(state)

def console_multiple_select(selection):
    while True:
        selected=[]
        for i in range(1,len(selection)):
            print("("+str(i)+")"+selection[i-1])
        print("请输入你的选择，可多选，选项之间用半角逗号（英文逗号）隔开,q退出")
        selecnu = str(input("->"))
        if selecnu == "q":
            raise Exception("用户退出")
        try:
            for i in selecnu.split(","):
                selected.append(selection[int(i)-1])
            break
        except Exception as e:
            print("输入格式错误!"+str(e))
    return selected


if __name__ == "__main__":
    imports = extract_imports_from_directory("D:\invisible_video_watermark")
    print(nuitka_plugin_filter(imports))
    print(console_multiple_select(imports))

