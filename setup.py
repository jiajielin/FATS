# coding=utf-8

"""
Time : 2017/4/21 9:28
Author : Jia Jielin
Company:
File : setup.py
Description:

"""

# system module
from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')

options = {"py2exe": {"includes": ["sip"],
                      "compressed": 1,
                      "optimize": 2,
                      "ascii": 0,
                      "excludes": ["Tkinter"],
                      "dll_excludes": ["MSVCP90.dll"]
                      }
           }

windows = [{'script': 'FATSMain.py', 'icon_resources':[(1, 'fhIcon.ico')]}]

setup(windows=windows,
      options=options,
      # data_files=[]
      )

