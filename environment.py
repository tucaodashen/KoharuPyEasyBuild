import platform
import subprocess
import psutil

import gettext

_ = gettext.gettext


def is_executable(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode

def compile_estimate():
    outputlines = []
    arch = platform.machine()
    outputlines.append(_("当前系统架构：")+arch)
    if arch.lower() != "amd64":
        outputlines.append(_(" - [red]架构可能不适合编译[/red]"))
    pythonversion = platform.python_version().split(".")
    allmem = psutil.virtual_memory().total / (1024 ** 3)
    if int(allmem) <= 2:
        outputlines.append(_("[red]内存可能不足以完成编译[/red]"))


    outputlines.append(_("你的python解释器版本为：")+str(pythonversion[0])+str(pythonversion[1]))
    if int(pythonversion[1]) < 8:
        outputlines.append(_(" - [red]python版本过低[/red]"))

    if is_executable("cl.exe") == 1:
        outputlines.append(_("未安装MSVC或未添加到环境变量"))
    if is_executable("gcc") == 1:
        outputlines.append(_("未安装MinGW或者GCC，无法使用Nuitka的GCC模式"))

    outputlines.append(_("更详细的分析报告将在编译前生成"))

    return outputlines


