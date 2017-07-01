# coding=utf-8

"""
Time : 2017/4/21 11:29
Author : Jia Jielin
Company:
File : setup2pyd.py
Description:
该文件将对应文件，一般为需要隐藏代码的文件，策略文件，转为pyd文件
"""

from distutils.core import setup
from Cython.Build import cythonize

# 确定编译文件
file = 'strategyTemplate.py'
setup(
    ext_modules=cythonize(file)
)

# setup2pyd.py build_ext --inplace
# ps:1.项目路径不能有中文，否则报编码错误，解决方式暂不了解
#    2.编译用到C++编译器，由于相关代码问题，经常取不到对应文件，实际需要更改distutils中toolskey，具体参考 http://bbs.fishc.com/thread-64098-1-1.html