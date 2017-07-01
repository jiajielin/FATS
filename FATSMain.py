# coding=utf-8

"""
Name：福慧自动交易系统（FATS）
Time : 2017/1/23 10:10
Author : Jia Jielin
Company:
File : FATSMain.py
Description:实现自动下单功能
Version: v0.1   2016/7/12-2016/12/18
"""

# system module
import sys
from fhUiMain import *
# sys.setrecursionlimit(10000000)

# ------------------------
def main():
    """主程序入口"""
    # 重载sys模块，设置默认字符串编码方式为utf-8
    reload(sys)
    sys.setdefaultencoding('utf8')
    # sys.setrecursionlimit(100000)

    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('fhIcon.ico'))
    app.setFont(BASIC_FONT)

    # cache缓存类
    cache = dict()
    version = 'V0.1'
    cache['version'] = version
    cache['futuresDataGateway'] = ''    # 期货数据获取接口（历史数据）
    cache['secDataGateway'] = ''        # 证券数据获取接口（历史数据）
    cache['futuresGateway'] = ''        # 期货交易及行情数据接口
    cache['secGateway'] = ''            # 期货交易及行情数据接口

    lw = LoginWidget(cache)

    lw.show()
    sys.exit(app.exec_())

# --------------------

if __name__ == '__main__':
    main()


