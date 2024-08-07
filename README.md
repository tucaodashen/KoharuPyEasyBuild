
# KoharuEasyBuild  
  
下江小春都会用的Python静态可执行文件构建器  
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/edHeadI.jpg?raw=true "Ai画的")  
[中文](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/README.md)|[English](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme_EN.md)  
![Alt](https://repobeats.axiom.co/api/embed/d4224f09be08f0118383269fca5d909676a69c0e.svg "Repobeats analytics image")  
![Alt](https://moe-counter.glitch.me/get/@:tucaodashen_Koharu?theme=rule34 "Repobeats analytics image")  
### 为什么要使用KoharuEasyBuild(KEB)？  
1，KEB可以轻松的嵌入到你的任何GitHub项目中来实现自动化的云端构建与分发  
2，KEB简化了Nuitka这类复杂Python构建器的参数设置，可以快速帮助新手构建出兼具效率与空间利用率的可执行文件，也可以帮助熟练使用者减少时间占用。  
3，KEB可以自动分析Pypi包的相互关系，并自动化准备所需文件，无需人工干预。这大大加快了Nuitka的构建速度。在极端情况下时间利用率超过500%。  
4，KEB的自动化分析在部分情况下可以使构建出可执行文件的大小较常规情况减少25%左右，极端情况下可以减少一半以上。  
  
### KoharuEsayBuild目前的不足  
1，运行不稳定，有待质量验证  
2，大型项目的分析时间与构建时间都过长  
3，自动环境准备存在冗余文件问题  
  
  
### KoharuEasyBuild的推荐使用项目  
1，纯Python标准库项目(最稳定，空间最小)  
2，使用少量第三方包的项目(相对稳定，构建速度最快)  
3，大量使用第三方包，但项目结构并不复杂(分析速度慢，构建速度快)  
  
### 不推荐使用的情况  
1，使用Transformrs与PyTorch的项目(编译器本身支持不完善)  
2，有大量Dll绑定的项目(自动数据文件分析可能无法进行正确复制)  
3，非Windows构建(Linux与Mac适用性尚未验证)  
  
## 如何使用？  
### 设备环境准备  
设备要求：  
amd64架构   
2G以上内存   
10G以上储存  
终端支持彩色显示  
  
Python项目应该符合以下要求：  
1，能够正常运行  
2，不含有与你所使用第三方包同名(不区分大小写)的自定义模块  
3，所需外部文件在根目录，所需外部文件夹中无.py文件，这会导致无法自动识别，当然，你可以手动指定  
4，在项目根目录中存在requirements.txt  
  
之后，克隆此仓库，尽量将其与项目文件夹分离，以免对依赖分析产生影响。  
  
  
### C后端准备  
若你只打算使用Pyinstaller，则无需进行任何准备，但若是要使用Nuitka，则需要MSVC(2017以上)或MinGW64(不同版本不同)。对于MinGW，即GCC的Windows移植版，可以由Nuitka自动下载并配置，而MSVC则需要使用VisualStudio等进行安装。  
  
若你想自动化配置GCC的C后端，可以在配置好Python环境后，在激活Python环境的前提下在终端中运行auto_env.bat自动配置GCC(确保网络通畅)  
### Python环境配置  
创建虚拟环境或使用Conda环境，Python版本必须大于3.8，推荐使用3.10。  
要确保KoharuEB的运行环境与你的项目的运行环境相同  
```  
conda create -n KoharuEasyBuild python=3.10 -y  
```  
然后安装KoharuEB的依赖  
```  
pip install -r selfreq.txt  
```  
你也可以使用Conda  
```  
conda install -r selfreq.txt  
```  
  
安装完成后，打开你的终端软件(推荐使用Windows终端，而不是命令行主机)并全屏，防止信息显示不全。  
使用`python CIL.py`启动编译向导  
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/pic1.png?raw=true "Pic1")  
输入1进入编译向导，根据自身情况选择始于你的项目的编译器  
由于Pyinstaller使用过于简单，此处以Nuitka为例。  
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/pic2.png?raw=true "Pic2")  
按照指引输入项目路径与项目入口文件路径  
随后，会让你选择预处理模式  
无预处理即为编译 ***所有*** 的第三方库  
而引导预处理则是会让你选择一部分不编译的第三方库  
无第三方库的项目选择哪一种都是可以的，此处以自动引导预处理为例  
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/pic3.png?raw=true "Pic3")  
选择后会进行依赖分析，并让你选择不编译的库。对于占用空间小于50m的库，不编译可以显著加快速度并在一定程度上减少空间占用。而对大于50m的库进行编译可以显著减少空间占用。  
这需要各位以自身经验为准  
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/pic4.png?raw=true "Pic4")  
然后为选择插件，一般而言输入 ***D***保持默认即可，但若是发现自己未使用相应库插件却启用(如你并未使用PyQt，Pyqt5的颜色却变绿),可输入相应序号关闭。  
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/pic5.png?raw=true "Pic5")  
随后为附加数据文件，一般而言自动检测以足够使用，若未完全检测到位。可以使用Zip文件附加，附加逻辑为直接将Zip解压并覆盖根目录。  
之后进入附加选项，根据自身需要填写即可，但我建议保留控制台，Nuitka关闭控制台有可能出现无法运行的问题。  
编译器也根据自身情况选择即可  
最后填写输出路径与输出类型  
若选择可执行文件，输出为文件夹。若选择嵌入包，输出则为压缩包。  
  
### GithubAction嵌入包的使用  
如果你选择使用GitHubAction嵌入包，那你会得到一个名为GA_Pack的压缩包，里面有两个文件夹(K_make与.github)，你只需要把他放在项目的根目录下，然后提交并推送至Github，即可实现云端的自动化编译。

## ToDo
 - [ ] 添加对Linux的支持
 - [ ] 冗余代码的优化
 - [ ] 添加对英语的支持
 - [ ] 优化CIL工具的操作

## Credit
感谢下列开源项目，没有它们也不会有今天的各种编译器与KoharuEB
```
https://github.com/Nuitka/Nuitka
https://github.com/pyinstaller/pyinstaller
https://github.com/Textualize/rich
https://github.com/microsoft/STL
https://github.com/gcc-mirror/gcc
```
还有你