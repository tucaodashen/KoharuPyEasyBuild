import json
import subprocess
import sys


def get_full_dependence():
    # 使用subprocess.run来执行命令
    result = subprocess.run(sys.executable + " -m pipdeptree -j", shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    # 输出命令的返回值
    data = result.stdout
    with open("dependence.json", "w", encoding='utf-8') as file:
        file.write(data)

    with open('dependence.json') as json_file:
        json_data = json.load(json_file)
    return json_data



if __name__ == "__main__":
    pass
