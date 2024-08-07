import gettext
import shutil
import json
import auto_pyinstaller
import auto_nuitka
import AutoDep
import sys
import os
import time

from rich import print
from rich.console import Console
import environment

_ = gettext.gettext

console = Console()





def assembly_github_action(project_path, iconpath, attached_data, target_path):
    if os.path.exists("GA_Pack/K_make"):
        shutil.rmtree("GA_Pack")
        os.mkdir("GA_Pack")
        os.mkdir("GA_Pack/K_make")
        os.mkdir("GA_Pack/.github")
        os.mkdir("GA_Pack/.github/workflows")
    else:
        os.mkdir("GA_Pack")
        os.mkdir("GA_Pack/K_make")
        os.mkdir("GA_Pack/.github")
        os.mkdir("GA_Pack/.github/workflows")
    if iconpath != "":
        shutil.copy(iconpath, "GA_Pack/K_make")
    if attached_data != "":
        shutil.copy(attached_data, "GA_Pack/K_make")
    if os.path.exists("make_config.json"):
        shutil.copy("make_config.json", "GA_Pack/K_make")

    for i in os.listdir("executer"):
        if not os.path.isdir(i):
            shutil.copy("executer/" + str(i), "GA_Pack/K_make")

    shutil.copy("selfreq.txt", "GA_Pack/K_make")
    shutil.copy(project_path + "/requirements.txt", "GA_Pack/K_make")

    shutil.copy("build_python.yml", "GA_Pack/.github/workflows")
    shutil.copy("auto_env.bat","GA_Pack/K_make")
    shutil.copy("auto.txt","GA_Pack/K_make")
    shutil.copy("helloworld.py","GA_Pack/K_make")

    AutoDep.zip_directory("GA_Pack", target_path + "/GA_Pack.zip")
    shutil.rmtree("GA_Pack")


def compile_guide():
    console.clear()
    single_choose(compile_guide_menu)


def compile_analysis():
    result = environment.compile_estimate()
    for i in result:
        console.print(i)


def goto_main():
    console.clear()
    console.print(_("欢迎使用KoharuEasyBuild"), style="bold #66ccff on white", justify="center")
    single_choose(main_menu)


def nu_guide():
    path = console.input(_("请输入你的Python项目路径:"))
    m_path = console.input(_("请输入你的Python[red]主入口文件[/red]路径:"))
    build_instance = auto_nuitka.AutoNuitka(path, m_path)
    console.print(_("请选择预处理模式："))
    console.print(_("1)无预处理(速度最慢，生成文件可能最大，建议微型项目或者未使用Pypi库的项目使用)"))
    console.print(_("2)自动引导预处理(速度最快，生成文件大小不确定，若使用大量Pypi库可使用)"))
    cho = console.input()
    if int(cho) == 3:
        manual_command = console.input(_("请输入nuitka命令[red]参数[/red]:"))
        pre_process = False
    if int(cho) != 3:
        pre_process = True
        build_instance.mode = "auto_np"
        build_instance.get_buildin_package()
        build_instance.get_pypi_package()
        build_instance.get_essential_nuitka_plugin()
        if int(cho) == 2:
            build_instance.mode = "auto_p"
            console.clear()
            console.print(_("导入设置"), style="bold #66ccff on white", justify="center")

            packageount = len(build_instance.pypi_package)
            console.print(_(f"你使用了{packageount}个Pypi包"))
            console.print(_("请选择你不需要编译的Pypi包"))
            build_instance.disabled_pypi = muitiple_choose_P(build_instance.pypi_package, build_instance.site_dir)

        console.clear()
        console.print(_("插件设置"), style="bold #66ccff on white", justify="center")
        console.print(
            _("请选择需要启用的Nuitka插件，[green]绿色[/green]为自动启用的插件，若保持默认则输入D，希望启用或关闭请输入相应序号，用半角逗号隔开"))
        printlist = []
        plist = list(AutoDep.NuPluginFilter.keys())
        for i in plist:
            if i in build_instance.plugin_list:
                printlist.append(f"[green]{i}[/green]")
            else:
                printlist.append(i)
        ids = 0
        for li in printlist:
            ids += 1
            console.print(f"{ids}){li}")
        plugin_resu = console.input(_("请输入:"))
        if plugin_resu == "D":
            build_instance.enabled_plugin = build_instance.plugin_list
        else:
            build_instance.enabled_plugin = build_instance.plugin_list
            for i in plugin_resu.split(","):
                if plist[int(i) - 1] in build_instance.plugin_list:
                    build_instance.enabled_plugin.remove(plist[int(i) - 1])
                else:
                    build_instance.enabled_plugin.append(plist[int(i) - 1])

        console.clear()
        console.print(_("附加设置"), style="bold #66ccff on white", justify="center")
        console.print(_("附加数据文件，留空则会自动复制项目文件夹中的非Python包文件夹与文件"))
        dtf = AutoDep.auto_data_files(path)
        for i in dtf:
            console.print(str(i))
        console.print(_("或者，你可以手动输入数据文件(文件夹)的[red]Zip压缩文件绝对路径[/red]"))
        data_files = ''
        data_files = console.input(_("请输入:"))
        is_console = console.input(_("是否启用控制台(Y/N:)"))
        if is_console == "Y":
            console_IS = True
        else:
            console_IS = False
        icon_file = console.input(_("图标文件(留空不使用):"))
        uac_admin = console.input(_("请求管理员权限(只有Windows可用)(Y/N)?"))
        if uac_admin == "Y":
            uac = True
        else:
            uac = False
        is_debug = console.input(_("生成Debug模式的文件(Y/N)?"))
        if is_debug == "Y":
            debug = True
        else:
            debug = False

        console.clear()
        console.print(_("编译相关设置"), style="bold #66ccff on white", justify="center")
        console.print(_("编译器选择(只可在安装后选择)"))
        console.print("1)MSVC")
        console.print("2)GCC(MinGW)")
        compiler_sl = console.input("请选择:")
        if int(compiler_sl) == 2:
            compiler = "GCC"
        else:
            compiler = "MSVC"
        compiler_LTO = console.input(_("启用链接优化时间(Y/N/A(自动)):"))
        low_memory = console.print(_("低内存模式(Y/N):"))
        if low_memory == "Y":
            lm = True
        else:
            lm = False

    console.clear()
    console.print(_("输出设置"), style="bold #66ccff on white", justify="center")
    output_path = console.input(_("输出路径:"))
    build_instance.target_path = output_path
    console.print(_("输出为:"))
    console.print(_("1)GitHubAction嵌入包"))
    console.print(_("2)可执行文件"))
    output_categories = console.input(_("请输入:"))

    if int(output_categories) == 2:
        if pre_process:
            build_instance.detect_self()
            build_instance.compile_start(compiler, uac, debug, lm, console_IS, icon_file, compiler_LTO)
        AutoDep.copy_path(os.getcwd() + "/" + os.path.splitext(os.path.basename(build_instance.entrance))[0] + ".dist",
                          build_instance.target_path)
        build_instance.copy_adding()
        shutil.rmtree(os.getcwd() + "/" + os.path.splitext(os.path.basename(build_instance.entrance))[0] + ".dist")
        shutil.rmtree(os.getcwd() + "/" + os.path.splitext(os.path.basename(build_instance.entrance))[0] + ".build")
        for i in dtf:
            if os.path.isdir(i):
                AutoDep.copy_path(i, output_path + "/" + os.path.basename(i), mode="merge")
            else:
                shutil.copy(i, output_path)
        if data_files != "":
            AutoDep.release_zip(data_files, build_instance.target_path)
        console.print(_(f"编译完成！路径{output_path}"))
    else:
        output_dic = {
            'generator_type': "nuitka",
            'mode': build_instance.mode,
            'main_entrance': os.path.basename(build_instance.entrance),
            'disabled_pypi': build_instance.disabled_pypi,
            'enabled_plugin': build_instance.enabled_plugin,
            'uac': uac,
            'console': console_IS,
            'debug': debug,
            'icon': icon_file,
            'attached_data': data_files
        }
        with open("make_config" + ".json", "w", encoding='utf-8') as f:
            json.dump(output_dic, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行
        assembly_github_action(path,icon_file,data_files,output_path)
        console.print(_("构建完成"))


def pyinstaller_guide():
    path = console.input(_("请输入你的Python项目路径:"))
    pyproject_path = console.input(_("请输入你的python项目[red]入口文件[/red]的[red]绝对路径[/red]:"))
    console.clear()
    console.print(_("附加设置"), style="bold #66ccff on white", justify="center")
    console.print(_("附加数据文件，留空则会自动复制项目文件夹中的非Python包文件夹与文件"))
    dtf = AutoDep.auto_data_files(path)
    for i in dtf:
        console.print(str(i))
    console.print(_("或者，你可以手动输入数据文件(文件夹)的[red]Zip压缩文件绝对路径[/red]"))
    data_files = ''
    data_files = console.input(_("请输入:"))
    is_console = console.input(_("是否启用控制台(Y/N):"))
    if is_console == "Y":
        c_arg = True
    else:
        c_arg = False
    is_debug = console.input(_("生成Debug模式的文件(Y/N):"))
    if is_debug == "Y":
        d_arg = True
    else:
        d_arg = False
    icon_path = console.input(_("图标路径(留空不使用):"))
    console.clear()
    console.print(_("输出设置"), style="bold #66ccff on white", justify="center")
    output_path = console.input(_("输出路径:"))
    console.print(_("输出为:"))
    console.print(_("1)GitHubAction嵌入包"))
    console.print(_("2)可执行文件"))
    output_categories = console.input(_("请输入:"))
    if int(output_categories) == 2:
        build_instance = auto_pyinstaller.auto_pyinstaller(pyproject_path, c_arg, d_arg, output_path, icon_path)
        build_instance.compile_start()
        build_instance.after()
        for i in dtf:
            if os.path.isdir(i):
                AutoDep.copy_path(i, output_path + "/" + os.path.basename(i), mode="merge")
            else:
                shutil.copy(i, output_path)
        if data_files != "":
            AutoDep.release_zip(data_files, output_path)
        console.print(_(f"编译完成！路径{output_path}"))
    else:
        output_dic = {
            'generator_type': "pyinstaller",
            'main_entrance': os.path.basename(pyproject_path),
            'process_type': None,
            'disabled_pypi': None,
            'enabled_plugin': None,
            'uac': None,
            'console': c_arg,
            'debug': d_arg,
            'icon': icon_path,
            'attached_data': data_files
        }
        with open("make_config" + ".json", "w", encoding='utf-8') as f:
            json.dump(output_dic, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行
        assembly_github_action(pyproject_path,icon_path,data_files,output_path)


def quit():
    sys.exit()


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # 跳过链接文件
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def bytes_to_mb(size_in_bytes):
    # 1MB = 1024 * 1024 字节
    MB = 1024 * 1024
    size_in_mb = size_in_bytes / MB
    return round(size_in_mb, 2)


main_menu = [
    {
        'label': _("编译向导"),
        'callback': compile_guide,
        'arguements': None
    },
    # {
    #     'label': _("从已生成指导文件编译"),
    #     'callback': compile_guide,
    #     'arguements': None
    # },
    {
        'label': _("退出"),
        'callback': quit,
        'arguements': None
    },
]

compile_guide_menu = [
    {
        'label': _("编译环境检测"),
        'callback': compile_analysis
    },
    {
        'label': _("Pyinstaller向导(Win,Mac,Linux)"),
        'callback': pyinstaller_guide
    },
    {
        'label': _("Nuitka向导(Win,Linux)"),
        'callback': nu_guide
    },
    {
        'label': _("返回上一级"),
        'callback': goto_main
    },
]


def con_able(inputnum):
    res = False
    try:
        a = int(inputnum)
        res = True
    except:
        pass
    return res


def single_choose(list):
    id = 0
    for si in list:
        id += 1
        console.print(str(id) + ")" + si['label'])
    while True:

        selected = console.input(_("[green]请输入序号以进行操作:[/green]"))
        if con_able(selected):

            if int(selected) > id:
                console.print(_("输入序号超出范围！"), style="red bold")
            else:
                sel = list[int(selected) - 1]
                sel['callback']()
                break

        else:
            console.print(_("请输入数字！"), style="red bold")


def muitiple_choose(list):
    id = 0
    for i in list:
        id += 1
        console.print(str(id) + ")" + str(i))
    res = console.input(_("请输入序号以选择，多个序号见以半角逗号隔开"))
    al = res.split(",")
    result = []
    for ids in al:
        result.append(list[int(ids) - 1])
    return result


def muitiple_choose_P(list, path):
    analysiser = AutoDep.accudeps()
    id = 0
    for i in list:
        if os.path.exists(path + "/" + str(i)):
            space = bytes_to_mb(get_folder_size(path + "/" + str(i)))
        else:
            space = 0
        id += 1
        console.print(str(id) + ")" + str(i) + "      " + _(f"占用空间{space} MB"))
        reares = analysiser.accurate_dependence_and_space_analysis(str(i))
        console.print(_("  -  " + f"关联了{reares[0]}个包，总占用{round(reares[1] + float(space), 3)} MB"))
    res = console.input(_("请输入序号以选择，多个序号见以半角逗号隔开"))
    al = res.split(",")
    result = []
    for ids in al:
        result.append(list[int(ids) - 1])
    return result


while True:
    console.clear()
    console.print(_("欢迎使用KoharuEasyBuild"), style="bold #66ccff on white", justify="center")
    single_choose(main_menu)
    input()
