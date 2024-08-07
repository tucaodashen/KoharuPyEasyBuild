
# KoharuEasyBuild  
  
Everyone who is not as dumb as Koharu can use it to compile python files easily.
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/edHeadI.jpg?raw=true "Ai画的") 
中文|English  
![Alt](https://repobeats.axiom.co/api/embed/d4224f09be08f0118383269fca5d909676a69c0e.svg "Repobeats analytics image")  
![Alt](https://moe-counter.glitch.me/get/@:tucaodashen_Koharu?theme=rule34 "Repobeats analytics image")  
### What's the feature of KoharuEasyBuild(KEB)？  
1，You can implant it in your project easily to compile your python files on cloud.  
2，KEB simplifies the parameter settings of complex Python builders like Nuitka, enabling quick construction of executable files that are both efficient and space-efficient for beginners, and also helps experienced users save time.  
3，KEB can automatically analyze the interrelationships of PyPI packages and prepare the necessary files without human intervention. This significantly speeds up the build process of Nuitka. In extreme cases, the time efficiency can exceed 500%.  
4，KEB's automated analysis can, in some cases, reduce the size of the executable file by about 25% compared to the standard scenario, and in extreme cases, it can be reduced by more than half.  
  
### The current shortcomings of KoharuEsayBuild  
1.  It has unstable operation and requires quality verification.
2.  The analysis time and build time for large projects are both excessively long.
3.  There is an issue with redundant file generation in the automatic environment preparation.
  
  
### In which situation you should use KoharuEB
1.  Pure Python standard library projects (the most stable, minimal space usage).
2.  Projects that use a small number of third-party packages (relatively stable, fastest build speed).
3.  Projects that extensively use third-party packages but have a simple project structure (slow analysis speed, fast build speed).
  
### Situations not recommended for use. 
1.  Projects that use Transformers and PyTorch (the compiler's support is not fully developed).
2.  Projects with a large number of DLL bindings (automatic data file analysis may not be able to perform the correct copying).
3.  Builds that are not on Windows (Linux and Mac compatibility has not yet been verified).
  
## QuickSetup
### DevicSetup 
DeviceRequirements：  
-   Architecture: AMD64
-   Memory: More than 2GB
-   Storage: More than 10GB
-   Terminal supports color display
  
Your python project should：  
1.  It should be able to run normally.
2.  It should not contain any custom modules with the same name as the third-party packages you are using (case-insensitive).
3.  The required external files should be in the root directory, and there should be no `.py` files in the required external folders, as this may lead to failure in automatic recognition. Of course, you can manually specify them.
4.  There should be a `requirements.txt` file in the project's root directory.  

  
### C Backend  

If you only plan to use Pyinstaller, no preparation is needed. However, if you intend to use Nuitka, you will require MSVC (version 2017 or above) or MinGW64 (different versions may vary). For MinGW, which is a port of GCC for Windows, Nuitka can automatically download and configure it. In contrast, MSVC requires installation through Visual Studio or similar.

If you wish to automate the configuration of the GCC C backend, after setting up the Python environment, activate the Python environment and run `auto_env.bat` in the terminal to automatically configure GCC (ensure you have a stable internet connection).
### Python environment prepare
Create a virtual environment or use a Conda environment, ensuring that the Python version is greater than 3.8, with a recommendation to use version 3.10. 
Make sure that the runtime environment for KoharuEB is the same as the runtime environment for your project. 
```  
conda create -n KoharuEasyBuild python=3.10 -y  
```  
Then, install the dependencies for KoharuEB.
```  
pip install -r selfreq.txt  
```  
You can also use Conda  
```  
conda install -r selfreq.txt  
```  
  
After the installation is complete, open your terminal software (the Windows Terminal is recommended instead of the Command Prompt) and go full screen to prevent incomplete display of information. 
Use the command `python CIL.py` to start the compilation wizard.
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/pic1.png?raw=true "Pic1")  
Enter '1' to access the compilation wizard, and choose the compiler that suits your project based on your specific situation. 
Since Pyinstaller is too simple to use, this example will focus on Nuitka.
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/pic2.png?raw=true "Pic2")  
Enter the project path and the entry file path of the project according to the guidance. 
Next, you will be asked to select a preprocessing mode. No preprocessing means compiling _**all**_ third-party libraries, while guided preprocessing will allow you to choose some third-party libraries not to compile. 
For projects without third-party libraries, either option is fine; this example will use automatic guided preprocessing.
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/pic3.png?raw=true "Pic3")  
After making your selection, a dependency analysis will be conducted, and you will be asked to choose which libraries not to compile. Not compiling libraries that occupy less than 50MB of space can significantly speed up the process and reduce space usage to some extent. Compiling libraries larger than 50MB can significantly reduce space usage.
This requires everyone to rely on their own experience to make the decision.
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/pic4.png?raw=true "Pic4")  
Next, you will be prompted to select plugins. Generally, you can simply enter _**D**_ to keep the default settings. However, if you find that a plugin for a library you are not using is enabled (for example, if you are not using PyQt but the color for PyQt5 turns green), you can enter the corresponding number to disable it.
![Alt](https://github.com/tucaodashen/KoharuPyEasyBuild/blob/main/readme/pic5.png?raw=true "Pic5")  
Next is the step for additional data files. Generally, the automatic detection is sufficient for use. If the automatic detection does not cover everything, you can attach files using a Zip file. The attachment logic is to directly extract the Zip and overwrite the contents in the root directory.
After that, you will enter the additional options step. You can fill in according to your own needs, but I recommend keeping the console. There might be issues with running the program if Nuitka closes the console.
Choose the compiler according to your own circumstances.

Finally, enter the output path and the type of output. 
If you choose the executable file, the output will be a folder. 
If you choose the embedded package, the output will be a compressed file.
  
### How to use GithubAction embedded package
If you choose to use a GitHub Action embedded package, you will obtain a compressed file named `GA_Pack`. Inside, there are two folders (`K_make` and `.github`). You simply need to place it in the root directory of your project, then commit and push to GitHub to achieve cloud-based automated compilation.

## ToDo
-  [ ] Add support for Linux
-  [ ] Optimize redundant code
-  [ ] Add support for English
-  [ ] Optimize the operation of the CIL tool

## Credit
We would like to express our gratitude to the following open-source projects; without them, there would be no variety of compilers and KoharuEB available today.
```
https://github.com/Nuitka/Nuitka
https://github.com/pyinstaller/pyinstaller
https://github.com/Textualize/rich
https://github.com/microsoft/STL
https://github.com/gcc-mirror/gcc
```
and you!