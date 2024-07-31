"""
Nuitka的自动处理类
꒰ঌ(🎀 ᗜ`v´ᗜ 🌸)໒꒱💈✅
"""
import AutoDep
import get_dep
import analysis_NDEP
import dependence_analysis

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
        self._stdlib = AutoDep.get_standard_library_names()
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
        for i in need_copy_list:
            for dicc in self.ns_pypi_mapping_list:
                if i == str(list(dicc.keys())[0]).lower():
                    print(str(i)+str(dicc))
        print(need_copy_list)

        #待修复：会将所有依赖项均视为非标准包，需要重新判断










if __name__ == "__main__":
    pass
    path = r"D:\invisible_video_watermark"
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



