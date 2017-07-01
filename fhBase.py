# coding=utf-8

"""
Time : 2017/1/23 10:44
Author : Jia Jielin
Company:
File : fhBase.py
Description:

"""


import json
from PyQt4 import QtGui, QtCore
import decimal
from eventEngine import *
from collections import OrderedDict


def loadFont():
    """载入字体设置"""
    try:
        f = file('setting.json')
        setting = json.load(f)
        f.close()
        family = setting['fontFamily']
        size = setting['fontSize']
        font = QtGui.QFont(family, size)
    except:
        font = QtGui.QFont(u'微软雅黑', 12)
    return font

# -------------------------
BASIC_FONT = loadFont()

# ---------------------
MAX_NUMBER = 10000000000000
MAX_DECIMAL = 4


def safeUnicode(value):
    """检查接口数据潜在的错误，保证转化为的字符串正确"""
    if value == None:
        return unicode('')

    # 检查是数字接近0时会出现的浮点数上限
    if type(value) is int or type(value) is float:
        if value > MAX_NUMBER:
            value = 0

    # 检查防止小数点位过多
    if type(value) is float:
        d = decimal.Decimal(str(value))
        if abs(d.as_tuple().exponent) > MAX_DECIMAL:
            value = round(value, ndigits=MAX_DECIMAL)

    return unicode(value)


# -------------------------------



class BasicMonitor(QtGui.QTableWidget):
    """
    基础监控
    """
    signal = QtCore.pyqtSignal(type(Event()))

    # -----------------------------------
    def __init__(self, mainEngine=None, eventEngine=None, parent=None):
        super(BasicMonitor, self).__init__(parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # 保存表头标签用
        self.headerDict = OrderedDict()  # 有序字典，key是英文名，value是对应的配置字典
        self.headerList = []  # 对应self.headerDict.keys()

        # 设置表头筛选项，用于相同内容的分别显示，主要是针对各个产品
        self.headerFilterDict = []
        self.headerFilter = {}
        self.filterFlag = False

        # 保存相关数据用
        self.dataDict = {}  # 字典，key是字段对应的数据，value是保存相关单元格的字典
        self.dataKey = ''  # 字典键对应的数据字段

        # 监控事件类型
        self.eventType = ''

        # 字体
        self.font = None

        # 保存数据对象到单元格
        self.saveData = False

        # 默认不允许根据表头进行排序，需要的组件可以开启
        self.sorting = False

        # 初始化右键菜单
        self.initMenu()

    # -----------------------------
    def setHeaderDict(self, headerDict):
        """设置表头有序字典"""
        self.headerDict = headerDict
        self.headerList = headerDict.keys()

    # ------------------------------
    def addHeaderFilterDict(self, header, filter):
        self.headerFilterDict.append(header)
        self.headerFilter[header] = filter
        self.filterFlag = True

    # ------------------------------
    def setDataKey(self, dataKey):
        """设置数据字典的键"""
        self.dataKey = dataKey

    # -----------------------------
    def setEventType(self, eventType):
        """设置监控的事件类型"""
        self.eventType = eventType

    # --------------------------------
    def setFont(self, font):
        """设置字体"""
        self.font = font

    # ---------------------------------
    def initTable(self):
        # 设置表格列数
        col = len(self.headerDict)
        self.setColumnCount(col)

        # 设置列表头
        labels = [d['chinese'] for d in self.headerDict.values()]
        self.setHorizontalHeaderLabels(labels)

        # 关闭左边垂直表头
        self.verticalHeader().setVisible(False)

        # 设置为不可编辑
        self.setEditTriggers(self.NoEditTriggers)

        # 设置为行交替颜色
        self.setAlternatingRowColors(True)

        # 设置允许排列
        self.setSortingEnabled(self.sorting)

    # -----------------------------
    def registerEvent(self):
        self.signal.connect(self.updateEvent)
        self.eventEngine.register(self.eventType, self.signal.emit)

    # ------------------------------------
    def updateEvent(self, event):
        data = event.dict_['data']
        self.updateData(data)

    # ------------------------------------
    def updateData(self, data):
        """数据更新至表格中"""
        inFilterFlag = True
        if self.filterFlag:
            for i in range(0, len(self.headerFilterDict)):
                if self.headerFilterDict[i] in data:
                    if data[self.headerFilterDict[i]] not in self.headerFilter[self.headerFilterDict[i]]:
                        inFilterFlag = False
                        break
                else:
                    inFilterFlag = False
                    break

        if inFilterFlag:
            # 如果允许排序，则插入数据前需关闭，否则插入新的数据会变乱
            if self.sorting:
                self.setSortingEnabled(False)

            # 如果设置了dataKey，则采用存量更新模式
            if self.dataKey:
                key = data.__getattribute__(self.dataKey)
                # 如果键在数据字典中不存在，则先插入新的一行，并创建对应单元格
                if key not in self.dataDict:
                    self.insertRow(0)
                    d = {}
                    for n, header in enumerate(self.headerList):
                        content = safeUnicode(data.__getattribute__(header))
                        cellType = self.headerDict[header]['cellType']
                        cell = cellType(content, self.mainEngine)

                        if self.font:
                            cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置

                        if self.saveData:  # 如果设置了保存数据对象，则进行对象保存
                            cell.data = data

                        self.setItem(0, n, cell)
                        d[header] = cell
                    self.dataDict[key] = d
                # 否则如果已经存在，则直接更新相关单元格
                else:
                    d = self.dataDict[key]
                    for header in self.headerList:
                        if header in dir(data):
                            content = safeUnicode(data.__getattribute__(header))
                            cell = d[header]
                            cell.setContent(content)

                            if self.saveData:  # 如果设置了保存数据对象，则进行对象保存
                                cell.data = data

            # 否则采用增量更新模式
            else:
                self.insertRow(0)
                for n, header in enumerate(self.headerList):
                    content = safeUnicode(data.__getattribute__(header))
                    cellType = self.headerDict[header]['cellType']
                    cell = cellType(content, self.mainEngine)

                    if self.font:
                        cell.setFont(self.font)

                    if self.saveData:
                        cell.data = data

                    self.setItem(0, n, cell)

            # 调整列宽
            # self.resizeColumns()
            self.resizeColumnsToContents()

            # 重新打开排序
            if self.sorting:
                self.setSortingEnabled(True)

    # ----------------------------------
    def resizeColumns(self):
        self.horizontalHeader().resizeSections(QtGui.QHeaderView.ResizeToContents)

    # ----------------------------
    def setSorting(self, sorting):
        self.sorting = sorting

    # --------------------------------
    def initMenu(self):
        """初始化右键菜单"""
        self.menu = QtGui.QMenu(self)
        saveAction = QtGui.QAction(u'保存内容', self)

        self.menu.addAction(saveAction)

    # -----------------------------
    def contextMenuEvent(self, event):
        """右键点击事件"""
        self.menu.popup(QtGui.QCursor.pos())


# ================================================
class BasicTreeCell(QtGui.QTreeWidgetItem):
    """基础的单元格"""

    # ------------------------------------------------------
    def __init__(self, text=None, mainEngine=None):
        """Constructor"""
        super(BasicTreeCell, self).__init__()
        self.data = None
        if text:
            self.setContent(text)

    # --------------------------------------------
    def setContent(self, text):
        """设置内容"""
        if text == '0' or text == '0.0':
            self.setText('')
        else:
            self.setText(text)


# ===============================================
class BasicCell(QtGui.QTableWidgetItem):
    """基础的单元格"""

    # ------------------------------------------------------
    def __init__(self, text=None, mainEngine=None):
        """Constructor"""
        super(BasicCell, self).__init__()
        self.data = None
        if text:
            self.setContent(text)

    # --------------------------------------------
    def setContent(self, text):
        """设置内容"""
        # if text == '0' or text == '0.0':
        #     self.setText('')
        # else:
        #     self.setText(text)
        self.setText(text)


# ==============================================
class NameCell(QtGui.QTableWidgetItem):
    """用来显示中文的单元格"""

    # --------------------------------------------
    def __init__(self, text=None, mainEngine=None):
        """Constructor"""
        super(NameCell, self).__init__()

        self.mainEngine = mainEngine
        self.data = None

        if text:
            self.setContent(text)

    # -----------------------------------------------
    def setContent(self, text):
        """设置内容"""
        if self.mainEngine:
            # 首先尝试正常获取合约对象
            contract = self.mainEngine.getContract(text)

            # 如果能读取合约信息
            if contract:
                self.setText(contract.name)


# ====================================================