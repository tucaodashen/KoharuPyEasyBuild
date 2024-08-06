import os
import sys
import uuid

import json
import auto_nuitka
import auto_pyinstaller
import AutoDep
import shutil


class execute():
    def __init__(self):
        self.config = self._load_config()
        self.build_instance = None
        self.project_path = None
        self.entrance = None

        self._load_config()
        self.get_path()

    def get_path(self):
        base_dir = os.getcwd()
        self.project_path = os.path.split(base_dir)[0]
        self.entrance = self.project_path + "/" + self.config['main_entrance']

        print(self.project_path)
        print(self.entrance)

    def _load_config(self):
        with open('make_config.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def run(self):
        if self.config['generator_type'] == 'pyinstaller':
            self.build_instance = auto_pyinstaller.auto_pyinstaller()
        else:
            self.build_instance = auto_nuitka.AutoNuitka(self.project_path,self.entrance,self.config['mode'])
            self.build_instance.get_buildin_package()
            self.build_instance.get_pypi_package()
            self.build_instance.compile_start("GCC",self.config['uac'],False,False,self.config['console'],os.path.basename(self.config['icon']),"A")
            AutoDep.copy_path(
                os.getcwd() + "/" + os.path.splitext(os.path.basename(self.build_instance.entrance))[0] + ".dist",
                self.build_instance.target_path)
            self.build_instance.copy_adding()
            shutil.rmtree(os.getcwd() + "/" + os.path.splitext(os.path.basename(self.build_instance.entrance))[0] + ".dist")
            shutil.rmtree(os.getcwd() + "/" + os.path.splitext(os.path.basename(self.build_instance.entrance))[0] + ".build")
            dtf = AutoDep.auto_data_files(self.project_path)
            for i in dtf:
                if os.path.isdir(i):
                    AutoDep.copy_path(i, "output_"+"/" + os.path.basename(i), mode="merge")
                else:
                    AutoDep.copy_path(i, 'output_', mode="overwrite")
            if self.config['attached_data'] != "":
                AutoDep.release_zip(os.path.basename(self.config['attached_data']), 'output_')


if __name__ == '__main__':
    bi = execute()
    bi.run()