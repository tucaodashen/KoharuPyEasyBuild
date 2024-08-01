"""
Nuitka的自动处理类
꒰ঌ(🎀 ᗜ`v´ᗜ 🌸)໒꒱💈✅
"""
# ToDo:完善Nuika的操作
# ToDo:写TUI
# ToDo:有关文件的复制
# ToDo:Pyinstaller的支持
# ToDo:环境的自动搭建
# ToDo:多语言化
# ToDo:错误处理
# ToDo:冗余代码清理


import AutoDep
import get_dep
import analysis_NDEP
import dependence_analysis
import os
import shutil

import gettext
from rich import print
from rich.console import Console
from rich.table import Column, Table


class AutoNuitka():
    def __init__(self, project_path):
        self.analist_list = None
        self.path = project_path

        self._setup_error_table()
        self.console = Console()
        self.pypi_package = None
        self._1pass_pypi_package = None
        self.import_list = None
        self.buildin_package = None
        self.non_custom_package = None
        self.stdlib = None
        self.plugin_list = []
        self.error_list = []
        self.installed_pypi_dic = AutoDep.get_site_packages_info()
        self.ns_pypi_mapping_list = []
        self.site_dir = analysis_NDEP.get_site_packages_path()
        self.path_list = []
        self.target_path = "D:\copytest"


        self.analyse_te_dic = {
            "name":"",
            "path":"",
            "associated":[],
            "cost_rate":0
        }

    def _setup_error_table(self):
        self.error_table = Table(show_header=True, header_style="bold magenta",show_lines=True)
        self.error_table.add_column("错误类型")
        self.error_table.add_column("报错内容")
        self.error_table.add_column("错误优先级", justify="right")

    def get_import(self):  # 这里获取的导入信息是包括自己写的模块的
        self.import_list = AutoDep.extract_imports_from_folder(self.path)

    def get_3rdp_package(self):  # 包括内置包和pypi包
        self.non_custom_package = AutoDep.extract_3rd_part_package_imports_from_dictionary(self.path)

    def get_pypi_package(self):
        self._1pass_pypi_package = []
        self.pypi_package = []
        self._stdlib = AutoDep.get_lib_files().keys()
        for i in self.non_custom_package:
            if i not in self.buildin_package:
                self._1pass_pypi_package.append(i)
        for i in self._1pass_pypi_package:
            if i not in self._stdlib:
                self.pypi_package.append(i)


    def get_buildin_package(self):
        if self.non_custom_package is not None:
            self.buildin_package = AutoDep.get_std_lib(self.non_custom_package)
        else:
            self.get_3rdp_package()
            self.buildin_package = AutoDep.get_std_lib(self.non_custom_package)

    def get_essential_nuitka_plugin(self):
        if self.non_custom_package != None:
            # print(self.import_list)
            self.plugin_list = AutoDep.nuitka_plugin_filter(self.non_custom_package)
        else:
            self.get_3rdp_package()

    def print_error_table(self):
        self.error_list = AutoDep.error_list
        for i in self.error_list:
            currrow = list()
            if i["type"] == "ParseError":
                currrow.append("[green]ParseError[/green]")
            else:
                currrow.append("")
            currrow.append("[yellow]"+str(i["context"])+"/yellow")
            if i["type"] == "ParseError":
                currrow.append("[green]一般无需处理[/green]")
            else:
                currrow.append("")
            self.error_table.add_row(currrow[0],currrow[1],currrow[2])
        self.console.print(self.error_table)

    def get_copy_list(self):
        need_copy_list = []
        analysis_list = []
        trans_list = [] #需要映射的列表
        normal_list = [] #不需要映射的列表
        json_data = dependence_analysis.get_full_dependence()
        self.ns_pypi_mapping_list = analysis_NDEP.get_non_standard_package()
        dec = []
        for i in self.ns_pypi_mapping_list:
            dec += list(i.values())
        decision_list = analysis_NDEP.flatten_list(dec) #获取判断包名是否需要映射的决定列表
        # print(decision_list)

        for i in self.pypi_package:
            if i in decision_list:
                #print(i)
                trans_list.append(i) #将需要转换的加入列表
            else:
                normal_list.append(i) #其余的加入不需要转换的列表
        for i in trans_list:
            for di in self.ns_pypi_mapping_list:
                if i in analysis_NDEP.flatten_list(list(di.values())):
                    #print("a")
                    #print(i)
                    #print(str(list(di.keys())[0]))
                    analysis_list.append(str(list(di.keys())[0]).lower())
        #analysis_list += normal_list #合并
        for i in analysis_list:
            need_copy_list += get_dep.find_dependencies(json_data,i)
        # 获得完整依赖列表
        need_copy_list = list(set(need_copy_list))

        print(need_copy_list)

        # 转回对应文件夹
        nonspack = []
        for i in need_copy_list:
            for dicc in self.ns_pypi_mapping_list:
                if i == str(list(dicc.keys())[0]).lower():
                    print(str(i)+str(dicc))
                    nonspack.append(i)

                    for fi in list(list(dicc.values())[0]):
                        print(self.site_dir+"/"+str(fi))
                        if os.path.exists(self.site_dir+"/"+str(fi)):
                            print("exit")
                            self.path_list.append(self.site_dir+"/"+str(fi))
                        else:
                            print(self.site_dir+"/"+str(list(dicc.keys())[0]).replace("-","_"))
                            if os.path.exists(self.site_dir+"/"+str(list(dicc.keys())[0]).replace("-","_")):
                                print("name_exist")
                                self.path_list.append(self.site_dir+"/"+str(list(dicc.keys())[0]).replace("-","_"))
                            # 获取所有非标准包路径



        print(nonspack)
        for i in nonspack:
            need_copy_list.remove(i)
        print(need_copy_list)
        need_copy_list += normal_list # 合并规范包
        print(need_copy_list)
        for spack in need_copy_list:
            if os.path.exists(self.site_dir+"/"+str(spack)):
                self.path_list.append(self.site_dir+"/"+str(spack))
            else:
                if os.path.exists(self.site_dir+"/"+str(spack).replace("-","_")):
                    self.path_list.append(self.site_dir+"/"+str(spack).replace("-","_"))


        self.path_list = list(set(self.path_list))


        print(self.path_list)

        self.ana_result = self.analysis_std() #所有需要的库
        self.req_std = []
        for i in self.ana_result:
            if i in self._stdlib:
                self.req_std.append(i)



        self.copy_std()
        self.copy_pypi()
    def esay_STD(self):
        self.all_std_lib_dir = AutoDep.get_lib_files().values()
        for i in self.all_std_lib_dir:
            if os.path.splitext(i)[1] != ".py" and os.path.basename(i) != "site-packages":
                AutoDep.copy_folder(i, self.target_path + "/" + os.path.basename(i))
            if os.path.splitext(i)[1] == ".py" and os.path.basename(i) != "site-packages":
                shutil.copy(i,self.target_path)

    def analysis_std(self):
        all = []
        for i in self.path_list:
            all += AutoDep.extract_3rd_part_package_imports_from_dictionary(i)
        return list(set(all))

    def copy_std(self):
        copy_list = []
        for i in self.req_std:
            if os.path.exists(AutoDep.std_lib_path()+"/"+i):
                print(i)
                copy_list.append(AutoDep.std_lib_path()+"/"+i)
            else:
                if os.path.exists(AutoDep.std_lib_path()+"/"+i+".py"):
                    print(i+".py")
                    copy_list.append(AutoDep.std_lib_path()+"/"+i+".py")
        for na in copy_list:
            if os.path.splitext(na)[1] != ".py":
                AutoDep.copy_folder(na, self.target_path + "/" + os.path.basename(na))
            if os.path.splitext(na)[1] == ".py":
                shutil.copy(na,self.target_path)
    def copy_pypi(self):
        for path in self.path_list:
            AutoDep.copy_folder(path,self.target_path+"/"+os.path.basename(path))













if __name__ == "__main__":
    pass
    path = r"D:\KoharuPyEasyBuild\build_test"
    bigpath = r"F:\solidworks\sd-webui-aki-v4.8"
    build_instance = AutoNuitka(path)
    build_instance.get_buildin_package()
    build_instance.get_pypi_package()
    build_instance.get_essential_nuitka_plugin()
    print(build_instance.buildin_package)
    print(build_instance.pypi_package)
    print(build_instance.plugin_list)
    build_instance.print_error_table()
    build_instance.get_copy_list()
    #build_instance.analysis_compile_cost()
    #build_instance.esay_STD()
    # bild_instance.analysis_std()



