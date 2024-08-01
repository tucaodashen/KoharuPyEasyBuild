import json
import os
import ast
import subprocess
import sys
import glob
import shutil


if sys.stdin.isatty():
    print("使用终端运行中，使用彩色进度条")
    from tqdm.rich import tqdm
else:
    print("非终端环境，彩色进度条已禁用!")
    from tqdm import tqdm

error_list = []




from rich import print

NuPluginFilter = { #nuitka的插件映射表
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


def get_site_packages_info():
    # 获取site-packages目录路径
    site_packages_dirs = [site_package for site_package in sys.path if 'site-packages' in site_package]

    package_info = {}

    # 遍历所有site-packages目录
    for site_packages_dir in site_packages_dirs:
        for entry in os.listdir(site_packages_dir):
            entry_path = os.path.join(site_packages_dir, entry)
            if os.path.isdir(entry_path) and os.path.isfile(os.path.join(entry_path, '__init__.py')):
                # 这是一个包
                package_info[entry] = entry_path
            elif os.path.isfile(entry_path) and entry.endswith('.py') and entry != '__init__.py':
                # 这是一个模块
                module_name = entry[:-3]  # 去掉 .py 后缀
                package_info[module_name] = entry_path

    return package_info

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

def console_multiple_select(selection): #终端内多选
    while True:
        selected=[]
        for i in range(1,len(selection)):
            print("("+str(i)+")"+selection[i-1])
        print("请输入你的选择，可多选，选项之间用半角逗号（英文逗号）隔开,q退出")
        selecnu = str(input("->"))
        if selecnu == "q":
            sys.exit()
        try:
            for i in selecnu.split(","):
                selected.append(selection[int(i)-1])
            break
        except Exception as e:
            print("输入格式错误!"+str(e))
    return selected


def list_folders_and_py_files(path):
    # 获取所有文件夹
    folders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    # 获取所有 .py 文件
    py_files = glob.glob(os.path.join(path, '*.py'))
    py_files = [os.path.basename(f) for f in py_files]

    return folders + py_files

def is_package(path): #根据文件夹内有无python文件判断是否为python包
    is_pac=False
    files = os.listdir(path)
    for i in files:
        if i.endswith('.py'):
            is_pac = True
            break
    return is_pac

def get_py_package(path): #获取指定路径下的有效python包
    pack_list=[]
    for i in list_folders_and_py_files(path):
        if ".py" not in i:
            if is_package(path+"/"+str(i)):
                pack_list.append(i)
    return pack_list

def get_lib_files():
    # 获取Python解释器的内置库路径
    lib_path = sys.base_prefix  # 使用base_prefix以避免虚拟环境的影响
    # 根据操作系统适配路径
    if sys.platform == 'win32':
        lib_path = os.path.join(lib_path, 'Lib')
    else:
        lib_path = os.path.join(lib_path, 'lib', 'python' + sys.version[:3])

    # 创建字典来存储文件名和路径
    lib_files = {}

    # 列出Lib文件夹中的一级目录文件和文件夹
    try:
        with os.scandir(lib_path) as entries:
            for entry in entries:
                if entry.is_file() or entry.is_dir():
                    # 将文件名和路径添加到字典中
                    lib_files[get_filename_without_extension(entry.name)] = os.path.join(lib_path, entry.name)
    except FileNotFoundError:
        # 如果Lib目录不存在，则返回空字典
        print(f"The directory {lib_path} does not exist.")
        return {}

    return lib_files

def find_py_files(directory):#获取文件夹内所有py文件的路径
    py_files = {}
    # 遍历指定目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名是否为.py
            if file.endswith('.py'):
                # 构造完整的文件路径
                full_path = os.path.join(root, file)
                # 将文件名和路径添加到字典中
                py_files[file] = full_path
    return py_files

def find_folders_with_py_files(directory): #获取所有含py文件的文件夹
    folders_with_py = {}
    # 遍历指定目录及其子目录
    for root, dirs, files in os.walk(directory):
        # 如果当前目录中有.py文件
        if any(file.endswith('.py') for file in files):
            # 构造文件夹的完整路径
            folder_path = os.path.join(directory, root[len(directory)+1:])  # 去掉路径前缀
            # 将文件夹名和路径添加到字典中
            folders_with_py[os.path.basename(root)] = folder_path
    return folders_with_py

def get_filename_without_extension(filename):
    # 分割文件名和扩展名
    return os.path.splitext(filename)[0]

def extract_3rd_part_package_imports_from_dictionary(path):
    third_part_package = []
    print("正在遍历文件，请稍等.....")
    flo = find_folders_with_py_files(path) #获取所有含有py文件的文件夹
    for floder in tqdm(flo.keys(),desc="正在分析导入项....."):
        curr_import = extract_imports_from_folder_top(flo[floder]) #获取当前文件夹中的导入信息
        curr_module = find_top_level_python_modules(flo[floder]) #获取当前目录的可导入项
        for i in curr_import:
            if i not in curr_module:
                try:
                    third_part_package.append(i)
                except Exception as e:
                    print(e)
    return list(set(third_part_package))



def extract_imports_from_folder(folder_path):
    imports_list = []

    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = parse_imports_in_file(file_path)
                imports_list.extend(imports)

    return list(set(imports_list))
def extract_imports_from_folder_top(folder_path):
    imports_list = []

    # 获取当前层文件夹中的所有文件和目录
    entries = os.listdir(folder_path)

    for entry in entries:
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path) and entry.endswith('.py'):
            # 如果是Python文件，解析导入的模块
            imports = parse_imports_in_file(full_path)
            imports_list.extend(imports)

    # 使用set去除重复的导入项，然后转换回列表
    return list(set(imports_list))

def parse_imports_in_file(file_path):
    global error_list
    error_table = {
        "type":"ParseError",
        "context":""
    }
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=file_path)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module.split('.')[0])
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        error_table["context"] = f"Error processing file {file_path}: {e}"
        error_list.append(error_table)
    return imports

def find_top_level_python_modules(folder_path):
    python_modules = []
    # 先获取一级目录中的所有文件夹
    directories = [entry.name for entry in os.scandir(folder_path) if entry.is_dir()]

    # 遍历每个文件夹，检查其下是否有Python文件
    for directory in directories:
        potential_package_path = os.path.join(folder_path, directory)
        # 检查目录中是否有Python文件
        if any(entry.name.endswith('.py') for entry in os.scandir(potential_package_path)):
            # 如果有Python文件，视为包
            package_name = directory
            python_modules.append(package_name)

    # 列出一级目录中的所有Python文件作为模块
    for entry in os.scandir(folder_path):
        if entry.is_file() and entry.name.endswith('.py'):
            module_name = entry.name[:-3]
            python_modules.append(module_name)

    return python_modules

def get_std_lib(import_list):
    std_lib = []
    libs = get_lib_files()
    for i in import_list:
        if i in libs:
            std_lib.append(i)
    return std_lib

def get_standard_library_names(): #获取当前版本的标准库
    # 获取所有模块的名称
    all_modules = sys.modules.keys()

    # 过滤出标准库模块
    std_libs = []
    for module in all_modules:
        if module in sys.builtin_module_names or module.startswith('win32'):
            std_libs.append(module)

    return std_libs

def get_pypi_package(non_custom_package,buildin_package,_stdlib):
    _1pass_pypi_package = []
    pypi_package = []
    stdlib = get_standard_library_names()
    for i in non_custom_package:
        if i not in buildin_package:
            _1pass_pypi_package.append(i)
    for i in _1pass_pypi_package:
        if i not in _stdlib:
            pypi_package.append(i)
    return pypi_package

def get_full_dependence():
    # 使用subprocess.run来执行命令
    result = subprocess.run(sys.executable+" -m pipdeptree -j", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # 输出命令的返回值
    data = result.stdout
    with open("dependence.json","w",encoding='utf-8') as file:
        file.write(data)

    with open('dependence.json') as json_file:
        json_data = json.load(json_file)
    for single in json_data:
        if single["package"]["key"] == "cv2":
            for i in single['dependencies']:
                print(i['key'])

def copy_folder(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_folder(s, d)
        else:
            shutil.copy2(s, d)
def std_lib_path():
    # 获取当前Python解释器的路径
    python_path = os.path.realpath(sys.executable)
    python_dir = os.path.dirname(python_path)
    stdlib_path = os.path.join(python_dir, 'Lib')

    return stdlib_path




if __name__ == "__main__":
    pass
    path="D:\invisible_video_watermark"
    #path1=r"D:\robot"
    #fpp = r"D:\invisible_video_watermark\algorithm\firekepper\GUI"
    #imports = extract_imports_from_directory(path1)
    #print(nuitka_plugin_filter(imports))
    #print(imports)
    #dict = get_installed_packages()
    #print(dict["PySide6"])
    #print(find_folders_with_py_files(path))
    #rdi = extract_3rd_part_package_imports_from_dictionary(path)
    #print(rdi)
    #print(get_std_lib(rdi))
    #print(find_top_level_python_modules(path))
    #print(extract_imports_from_folder(path1))
    #a=extract_imports_from_folder_top(fpp)
    #b=find_top_level_python_modules(fpp)
    #print(a)
    #print(b)
    #for i in a:
    #    if i not in b:
    #        print(i)
    #print(get_lib_files())
    #a = extract_3rd_part_package_imports_from_dictionary(path)
    #print(a)
    #print(get_full_dependence())
    #copy_folder("D:\python_ENV\ivw\Lib\site-packages\pydeps","D:\copytest\pydeps")
    #print(extract_3rd_part_package_imports_from_dictionary(r"D:\python_ENV\python\Lib\site-packages\tqdm"))
    #print(get_lib_files())
    print(std_lib_path())

