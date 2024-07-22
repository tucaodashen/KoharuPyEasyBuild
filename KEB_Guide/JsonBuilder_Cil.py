import platform
class Guider():
    def __init__(self):
        print(self.get_system_info())
    def intro(self):
        print("欢迎使用KEB_python构建器编译文件创建向导~")
        print()
    def generate_json(self):
        pass
    def get_system_info(self):
        info={
            "System":str(platform.system())+str(platform.version()),
            "Machine":platform.machine()+"  "+platform.processor(),
            "Python":platform.python_implementation()+str(platform.python_version())
        }
        return info

test = Guider()