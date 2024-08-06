import gettext
import os

os.environ['LANG'] = 'zh_CN.UTF-8'

# 设置 gettext 的目录和语言
localedir = 'locales'
languages = ['zh_CN']
gettext.bindtextdomain('i18n.py', localedir)
gettext.textdomain('i18n.py')
_ = gettext.gettext

print(_("I Love You!"))