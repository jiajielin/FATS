# coding=utf-8

"""
Time : 2017/1/23 10:52
Author : Jia Jielin
Company:
File : fhUiMain.py
Description:

"""

# system module
from __future__ import division
import psutil


# own module
from fhDb import DbUtils
from fhBase import *

from fhUtils import *
from fhMainEngine import MainEngine
from strategyTemplate import *
from PyQt4 import QtGui, QtCore


# ===============================
class LoginWidget(QtGui.QDialog):
    """登录界面，用于登录本公司系统，进入主页面前验证"""
    settingList = [SETTING_DEFAUlT,
                   SETTING_MYSELF]

    def __init__(self, cache, parent=None):
        super(LoginWidget, self).__init__()
        self.cache = cache
        self.initUi()

    # -----------------------
    def initUi(self):
        self.setWindowTitle(u'登录')
        # 设置组件
        labelUserID = QtGui.QLabel(u'用户')
        labelPassword = QtGui.QLabel(u'密码')
        # labelSetting = QtGui.QLabel(u'界面')

        self.editUserID = QtGui.QLineEdit()
        self.editPassword = QtGui.QLineEdit()
        self.editPassword.setEchoMode(QtGui.QLineEdit.Password)
        # self.comboSetting = QtGui.QComboBox()
        # self.comboSetting.addItems(self.settingList)

        self.editUserID.setMinimumWidth(220)

        buttonLogin = QtGui.QPushButton(u'登录')
        buttonCancel = QtGui.QPushButton(u'退出')
        buttonLogin.clicked.connect(self.login)
        buttonCancel.clicked.connect(self.close)

        # 设置布局
        buttonHBox = QtGui.QHBoxLayout()
        buttonHBox.addStretch()
        buttonHBox.addWidget(buttonLogin)
        buttonHBox.addWidget(buttonCancel)

        grid = QtGui.QGridLayout()
        grid.addWidget(labelUserID, 0, 0)
        grid.addWidget(labelPassword, 1, 0)
        # grid.addWidget(labelSetting, 2, 0)
        grid.addWidget(self.editUserID, 0, 1)
        grid.addWidget(self.editPassword, 1, 1)
        # grid.addWidget(self.comboSetting, 2, 1)

        grid.addLayout(buttonHBox, 3, 0, 1, 2)

        self.setLayout(grid)

        # self.login()

    # --------------------------------
    def login(self):
        """登录操作"""
        loginName = str(self.editUserID.text())
        password = str(self.editPassword.text())
        # setting = self.comboSetting.currentIndex()
        # if setting == 0:
        #     isDefaultSetting = True
        # else:
        #     isDefaultSetting = False
        isDefaultSetting = True

        # verifyFlag = self.userVerify(loginName, password)

        # 调试代码，调试完成后需注释掉 todo
        loginName = 'admin'
        verifyFlag = VERIFY_FUNDMANAGER

        if verifyFlag == VERIFY_ADMIN or verifyFlag == VERIFY_FUNDMANAGER or verifyFlag == VERIFY_TRADER or verifyFlag == VERIFY_DATAMANAGER or verifyFlag == VERIFY_INVESTMANAGER:
            self.cache['loginName'] = loginName
            self.cache['verifyFlag'] = verifyFlag
            inc = CipherUtils(password, FhKey)
            encPwd = inc.encrypt()
            self.cache['encPwd'] = encPwd
            self.cache['isDefaultSetting'] = isDefaultSetting
            self.openMainWindow()
            self.close()
        elif verifyFlag == VERIFY_NOUSER:
            QtGui.QMessageBox.warning(self, u'信息提示', u'用户名或密码错误')
        elif verifyFlag == DB_DISCONNECT:
            QtGui.QMessageBox.warning(self, u'信息提示', u'数据库连接失败')
        else:
            QtGui.QMessageBox.warning(self, u'信息提示', u'未知错误')

    # ---------------------------------
    def userVerify(self, loginName, password):
        inc = CipherUtils(password, FhKey)
        encPwd = inc.encrypt()
        dbUtils = DbUtils()
        if dbUtils.isConnected():
            return dbUtils.getUserVerify(loginName, encPwd)
        else:
            QtGui.QMessageBox.warning(self, u'信息提示', u'数据库连接失败')

    # -------------------------------------
    def openMainWindow(self):
        # print 'login secc'
        mainEngine = MainEngine()
        self.mw = MainWindow(mainEngine, mainEngine.eventEngine, self.cache)
        if self.cache['isDefaultSetting'] == False:
            import qdarkstyle
            self.mw.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

        self.mw.showMaximized()


# =====================================
class MainWindow(QtGui.QMainWindow):
    def __init__(self, mainEngine, eventEngine, cache):
        super(MainWindow, self).__init__()

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine
        self.cache = cache
        self.dbUtils = DbUtils(self.eventEngine, isLog=True)
        self.cache['dbUtils'] = self.dbUtils

        productInfo = self.dbUtils.getProducts()
        self.productList = [productInfo[i][0] for i in range(0, len(productInfo))]

        self.widgetDict = {}

        self.getAccountFile()
        self.initUi()

    # --------------------------------
    def initUi(self):

        self.initSize()
        self.setWindowTitle(u'欢迎使用福慧自动交易系统')
        self.initCentral()
        self.initMenu()

    # ------------------------
    def getAccountFile(self):
        try:
            f = file('accountSetting.json')
            accountSetting = json.load(f)
            f.close()
        except:
            accountSetting = {}

        if accountSetting:
            try:
                self.brokerID = accountSetting['brokerID']
                self.userID = accountSetting['userID']
                self.password = accountSetting['password']
                self.tdAddress = accountSetting['tdAddress']
                self.mdAddress = accountSetting['mdAddress']
                if 'product' in accountSetting:
                    self.product = accountSetting['product']
                else:
                    self.product = 'Unknown'
                if 'strategyFile' in accountSetting:
                    self.strategyFile = accountSetting['strategyFile']
                else:
                    self.strategyFile = ''
                if 'strategyClass' in accountSetting:
                    self.strategyClass = accountSetting['strategyClass']
                else:
                    self.strategyClass = ''
            except:
                self.brokerID = ''
                self.userID = ''
                self.password = ''
                self.tdAddress = ''
                self.mdAddress = ''
                self.product = 'None'
                self.strategyFile = ''
                self.strategyClass = ''
        else:
            self.brokerID = ''
            self.userID = ''
            self.password = ''
            self.tdAddress = ''
            self.mdAddress = ''
            self.product = 'None'
            self.strategyFile = ''
            self.strategyClass = ''

        self.cache['accountSetting'] = accountSetting
        self.cache['brokerID'] = self.brokerID
        self.cache['userID'] = self.userID
        self.cache['password'] = self.password
        self.cache['tdAddress'] = self.tdAddress
        self.cache['mdAddress'] = self.mdAddress
        self.cache['product'] = self.product
        self.cache['strategyFile'] = self.strategyFile
        self.cache['strategyClass'] = self.strategyClass

    # --------------------------
    def initSize(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(screen.width() / 8, screen.height() / 8, 3 * screen.width() / 4, 3 * screen.height() / 4)

    # ---------------------------
    def initCentral(self):
        widgetAlgoW, dockAlogW = self.createDock(AlgoWidget, u'产品', QtCore.Qt.LeftDockWidgetArea)
        widgetLogM, dockLogM = self.createDock(LogMonitor, u'日志', QtCore.Qt.LeftDockWidgetArea)
        widgetSignalM, dockSignalM = self.createDock(SignalMonitor, u'信号及成交情况', QtCore.Qt.RightDockWidgetArea)
        widgetPositionM, dockPositionM = self.createDock(PositionMonitor, u'持仓', QtCore.Qt.RightDockWidgetArea)
        widgetAccountM, dockAccountM = self.createDock(AccountMonitor, u'资金', QtCore.Qt.RightDockWidgetArea)

        self.tabifyDockWidget(dockPositionM, dockAccountM)

        dockPositionM.raise_()

    # -------------------------------
    def initMenu(self):
        actionWind = QtGui.QAction(u'连接Wind', self)
        actionWind.triggered.connect(self.connectWind)
        actionCTP = QtGui.QAction(u'连接CTP', self)
        actionCTP.triggered.connect(self.connectCTP)
        actionExit = QtGui.QAction(u'退出', self)
        actionExit.triggered.connect(self.close)
        # actionStrategy = QtGui.QAction(u'运行策略', self)
        # actionAbout = QtGui.QAction(u'关于', self)
        # actionAbout.triggered.connect(self.openAboutWidget)

        menubar = self.menuBar()

        sysMenu = menubar.addMenu(u'系统')
        if 'Wind' in self.mainEngine.gatewayDict:
            sysMenu.addAction(actionWind)
            self.connectWind()
        if 'CTP' in self.mainEngine.gatewayDict:
            sysMenu.addAction(actionCTP)
            self.connectCTP()
        sysMenu.addSeparator()
        sysMenu.addAction(actionExit)

        # strategyMenu = menubar.addMenu(u'策略')
        # helpMenu = menubar.addMenu(u'帮助')
        # helpMenu.addAction(actionAbout)

    # ------------------------------------------
    def connectCTP(self):
        """连接CTP接口"""
        # 赋值期货数据接口
        if self.cache['futuresGateway']:
            if self.cache['futuresGateway'] != 'CTP':
                self.mainEngine.close(self.cache['futuresGateway'])
                if 'accountSetting' in self.cache:
                    self.mainEngine.connect('CTP', self.cache['accountSetting'])
                else:
                    self.mainEngine.connect('CTP')
                self.cache['futuresGateway'] = 'CTP'
            else:
                if self.mainEngine.isConnected('CTP'):
                    pass
                else:
                    if 'accountSetting' in self.cache:
                        self.mainEngine.connect('CTP', self.cache['accountSetting'])
                    else:
                        self.mainEngine.connect('CTP')
        else:
            if 'accountSetting' in self.cache:
                self.mainEngine.connect('CTP', self.cache['accountSetting'])
            else:
                self.mainEngine.connect('CTP')
            self.cache['futuresGateway'] = 'CTP'

    # -------------------------------------------
    def createDock(self, widgetClass, widgetName, widgetArea):
        widget = widgetClass(self.mainEngine, self.eventEngine, self.cache, self)
        dock = QtGui.QDockWidget(widgetName)
        dock.setObjectName(widgetName)
        dock.setWidget(widget)
        dock.setFeatures(dock.DockWidgetFloatable)
        self.addDockWidget(widgetArea, dock)
        return widget, dock

    # -----------------------------------
    def connectWind(self):
        """连接Wind接口"""
        # 赋值期货数据接口
        if self.cache['futuresDataGateway']:
            if self.cache['futuresDataGateway'] != 'Wind':
                self.mainEngine.close(self.cache['futuresDataGateway'])
                self.mainEngine.connect('Wind')
                self.cache['futuresDataGateway'] = 'Wind'
            else:
                if self.mainEngine.isConnected('Wind'):
                    pass
                else:
                    self.mainEngine.connect('Wind')
        else:
            self.mainEngine.connect('Wind')
            self.cache['futuresDataGateway'] = 'Wind'

    # ------------------------------------------
    def openAboutWidget(self):
        """"""
        try:
            self.widgetDict['aboutW'].show()
        except KeyError:
            self.widgetDict['aboutW'] = AboutWidget(self)
            self.widgetDict['aboutW'].show()

    # ------------------------------
    def closeEvent(self, event):
        """关闭事件"""
        reply = QtGui.QMessageBox.question(self, u'退出',
                                           u'确认退出?', QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            for widget in self.widgetDict.values():
                widget.close()
            # self.saveWindowSettings()

            self.mainEngine.exit()
            event.accept()
        else:
            event.ignore()


# =====================================
class AboutWidget(QtGui.QDialog):
    """显示关于信息"""

    def __init__(self, parent):
        """Constructor"""
        super(AboutWidget, self).__init__(parent)
        self.parent = parent
        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """"""
        self.setWindowTitle(u'关于')

        text = u"""DEMO
            """ % self.parent.cache['version']

        label = QtGui.QLabel()
        label.setText(text)
        label.setMinimumWidth(450)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(label)

        self.setLayout(vbox)


# ========================================
class LogMonitor(BasicMonitor):
    """日志监控"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine, cache, parent=None):
        """Constructor"""
        super(LogMonitor, self).__init__(mainEngine, eventEngine, parent)

        d = OrderedDict()
        d['logTime'] = {'chinese': u'时间', 'cellType': BasicCell}
        d['logContent'] = {'chinese': u'内容', 'cellType': BasicCell}
        d['gatewayName'] = {'chinese': u'接口', 'cellType': BasicCell}
        self.setHeaderDict(d)

        self.setEventType(EVENT_LOG)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.registerEvent()
        self.setMaximumWidth(TRADE_LEFT_MAX)
        self.setMinimumWidth(TRADE_LEFT_MIN)


# ===============================
class AlgoWidget(QtGui.QFrame):
    """算法（策略）信息界面"""
    def __init__(self, mainEngine, eventEngine, cache, parent=None):
        super(AlgoWidget, self).__init__()
        self.gatewayName = u'策略模块'
        self.mainEngine = mainEngine
        self.eventEngine = eventEngine
        self.cache = cache
        self.product = self.cache['product']
        self.brokerID = self.cache['brokerID']
        self.userID = self.cache['userID']
        self.strategyFile = self.cache['strategyFile']

        self.strategyClass = None

        # 载入策略文件标记Flag，加载策略文件并实例化策略类成功，方为True
        self.loadFlag = False
        # # 策略执行状态标记
        # self.isStarted = False
        # 策略实例，目前是一个策略，若为多个策略，需修改程序，改为list或dict
        self.strategy = None

        self.initUi()

    # --------------------
    def initUi(self):

        self.setFrameShape(self.Box)
        self.setMaximumHeight(280)

        # 左边字段
        labelProduct = QtGui.QLabel(u'产品：')
        labelBrokerID = QtGui.QLabel(u'经纪商：')
        labelUserID = QtGui.QLabel(u'账户：')
        labelStrategy = QtGui.QLabel(u'策略文件：')
        # labelProduct.setFrameStyle(1)
        # 右边控件
        # self.lineProduct = QtGui.QLineEdit()
        self.lineProduct = QtGui.QLabel()
        self.lineProduct.setFrameStyle(2)
        # self.lineProduct.setEnabled(False)
        # self.lineBrokerID = QtGui.QLineEdi/t()
        self.lineBrokerID = QtGui.QLabel()
        self.lineBrokerID.setFrameStyle(1)
        # self.lineBrokerID.setEnabled(False)
        # self.lineUserID = QtGui.QLineEdit()
        self.lineUserID = QtGui.QLabel()
        self.lineUserID.setFrameStyle(1)
        # self.lineUserID.setEnabled(False)
        # self.lineStrategy = QtGui.QLineEdit()
        self.lineStrategy = QtGui.QLabel()
        self.lineStrategy.setFrameStyle(1)
        # self.lineStrategy.setEnabled(False)

        # 下面控件
        buttonAccount = QtGui.QPushButton(u'重载配置文件')
        buttonLoadStrategy = QtGui.QPushButton(u'加载策略')
        buttonStartStrategy = QtGui.QPushButton(u'启动策略')
        buttonStopStrategy = QtGui.QPushButton(u'停止策略')

        buttonAccount.clicked.connect(self.reloadAccountSetting)
        buttonLoadStrategy.clicked.connect(self.loadStrategy)
        buttonStartStrategy.clicked.connect(self.startStrategy)
        buttonStopStrategy.clicked.connect(self.stopStrategy)

        grid = QtGui.QGridLayout()
        grid.addWidget(labelProduct, 0, 0)
        grid.addWidget(labelBrokerID, 1, 0)
        grid.addWidget(labelUserID, 2, 0)
        grid.addWidget(labelStrategy, 3, 0)

        grid.addWidget(self.lineProduct, 0, 1)
        grid.addWidget(self.lineBrokerID, 1, 1)
        grid.addWidget(self.lineUserID, 2, 1)
        grid.addWidget(self.lineStrategy, 3, 1)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(buttonAccount)
        vbox.addWidget(buttonLoadStrategy)
        vbox.addWidget(buttonStartStrategy)
        vbox.addWidget(buttonStopStrategy)

        vbox.addStretch()

        self.setLayout(vbox)
        self.showInfo()

    # --------------------------
    def reloadAccountSetting(self):
        ret = 0
        if self.strategy:
            self.onLog(u'策略运行中，请先停止策略')
            return ret

        try:
            f = file('accountSetting.json')
            accountSetting = json.load(f)
            f.close()
        except:
            accountSetting = {}

        if accountSetting:
            try:
                self.brokerID = accountSetting['brokerID']
                self.userID = accountSetting['userID']
                self.password = accountSetting['password']
                self.tdAddress = accountSetting['tdAddress']
                self.mdAddress = accountSetting['mdAddress']
                if 'product' in accountSetting:
                    self.product = accountSetting['product']
                else:
                    self.product = 'Unknown'
                if 'strategyFile' in accountSetting:
                    self.strategyFile = accountSetting['strategyFile']
                else:
                    self.strategyFile = ''
                if 'strategyClass' in accountSetting:
                    self.strategyClass = accountSetting['strategyClass']
                else:
                    self.strategyClass = ''
            except:
                self.brokerID = ''
                self.userID = ''
                self.password = ''
                self.tdAddress = ''
                self.mdAddress = ''
                self.product = 'None'
                self.strategyFile = ''
                self.strategyClass = ''
                ret = 1
        else:
            self.brokerID = ''
            self.userID = ''
            self.password = ''
            self.tdAddress = ''
            self.mdAddress = ''
            self.product = 'None'
            self.strategyFile = ''
            self.strategyClass = ''
            ret = 1

        self.cache['accountSetting'] = accountSetting
        self.cache['brokerID'] = self.brokerID
        self.cache['userID'] = self.userID
        self.cache['password'] = self.password
        self.cache['tdAddress'] = self.tdAddress
        self.cache['mdAddress'] = self.mdAddress
        self.cache['product'] = self.product
        self.cache['strategyFile'] = self.strategyFile
        self.cache['strategyClass'] = self.strategyClass

        self.lineProduct.setText(unicode(self.product))
        self.lineBrokerID.setText(unicode(self.brokerID))
        self.lineUserID.setText(unicode(self.userID))
        self.lineStrategy.setText(unicode(self.strategyFile))
        # print accountSetting

        self.showInfo()

        return ret

    # -------------------------------
    def loadStrategy(self):
        self.strategyFile = self.cache['strategyFile']
        strategyClass = self.cache['strategyClass']

        if strategyClass == self.strategyClass and self.loadFlag:
            self.onLog(u'重复操作：策略已加载，加载算法相同，')
            return

        self.strategyClass = strategyClass

        try:
            stat = 'from ' + self.strategyFile + ' import ' + self.strategyClass
            exec(stat)
            # from kaufmanMA_1d import KaufmanMA_1d
            self.loadFlag = True
        except:
            self.onLog(u'加载策略失败')

        if self.loadFlag:
            if self.strategyClass in STRATEGY_CLASS:
                # STRATEGY大写为类，小写为实例
                try:
                    self.STRATEGY = STRATEGY_CLASS[self.strategyClass]
                    self.strategy = self.STRATEGY(self.mainEngine, self.eventEngine, self.cache)
                    self.onLog(u'加载策略成功')
                except:
                    self.onLog(u'实例化策略失败，请查看策略调用代码代码，调用类： ' + self.strategyClass)
                    self.loadFlag = False
            else:
                self.onLog(u'未找到对应策略类，请查看策略文件')
                self.loadFlag = False

    # ----------------------------------------------
    def startStrategy(self):
        if self.loadFlag and self.strategy:
            self.strategy.start()
            # self.isStarted = True
            if self.mainEngine.addStrategy(self.strategy):
                self.onLog(u'策略启动成功')
            else:
                self.onLog(u'策略已在运行列表中')
        else:
            self.onLog(u'策略启动失败，请查看是否已加载策略文件')

    # ----------------------------------------
    def stopStrategy(self):
        if self.strategy:
            self.strategy.stop()
            self.loadFlag = False
            self.onLog(u'策略停止成功')
            self.mainEngine.deleteStrategy(self.strategy)
            self.strategy = None
        else:
            self.loadFlag = False
            self.onLog(u'未检测到执行策略，停止操作无效')

    # ---------------------------------------------
    def onLog(self, logContent):
        """日志推送"""
        log = FhLogData()
        log.gatewayName = self.gatewayName
        log.logContent = logContent
        event1 = Event(type_=EVENT_LOG)
        event1.dict_['data'] = log
        self.eventEngine.put(event1)

    # --------------------------------------------
    def showInfo(self):
        self.lineProduct.setText(self.cache['product'])
        # print self.cache['product']
        self.lineBrokerID.setText(self.cache['brokerID'])
        self.lineUserID.setText(self.cache['userID'])
        self.lineStrategy.setText(self.cache['strategyFile'])


# =============================
class accountWidget(QtGui.QGroupBox):
    """账户信息"""
    def __init__(self, name, cache):
        super(accountWidget, self).__init__(name)
        self.cache = cache
        self.initUi()

    # ------------------
    def initUi(self):
        # 左边字段
        labelProduct = QtGui.QLabel(u'产品：')
        labelBrokerID = QtGui.QLabel(u'经纪商：')
        labelUserID = QtGui.QLabel(u'账户：')
        labelStrategy = QtGui.QLabel(u'策略文件：')

        # 右边控件
        self.lineProduct = QtGui.QLineEdit()
        self.lineBrokerID = QtGui.QLineEdit()
        self.lineUserID = QtGui.QLineEdit()
        self.lineStrategy = QtGui.QLineEdit()


        grid = QtGui.QGridLayout()
        grid.addWidget(labelProduct, 0, 0)
        grid.addWidget(labelBrokerID, 1, 0)
        grid.addWidget(labelUserID, 2, 0)
        grid.addWidget(labelStrategy, 3, 0)

        self.setAccountText()
        self.setLayout(grid)

    # ---------------------------
    def setAccountText(self):
        verifyFlag = True
        if 'product' in self.cache:
            self.lineProduct.setText(self.cache['product'])
        else:
            verifyFlag = False
        if 'brokerID' in self.cache:
            self.lineBrokerID.setText(self.cache['brokerID'])
        else:
            verifyFlag = False
        if 'userID' in self.cache:
            self.lineUserID.setText(self.cache['userID'])
        else:
            verifyFlag = False
        if 'strategyFile' in self.cache:
            self.lineStrategy.setText(self.cache['strategyFile'])
        else:
            verifyFlag = False
        if not verifyFlag:
            self.parent().onLog()

# ====================================
class SignalMonitor(BasicMonitor):
    """信号及下单监控"""
    def __init__(self, mainEngine, eventEngine, cache, parent=None):
        super(SignalMonitor, self).__init__(mainEngine, eventEngine, parent)

        d = OrderedDict()
        d['orderID'] = {'chinese': u'委托编号', 'cellType': BasicCell}
        d['strategyName'] = {'chinese': u'策略', 'cellType': BasicCell}
        d['symbol'] = {'chinese': u'代码', 'cellType': BasicCell}
        d['direction'] = {'chinese': u'信号方向', 'cellType': BasicCell}
        d['offset'] = {'chinese': u'开平仓', 'cellType': BasicCell}
        d['sessionID'] = {'chinese': u'会话编号', 'cellType': BasicCell}
        d['orderTime'] = {'chinese': u'委托时间', 'cellType': BasicCell}
        # d['finishTime'] = {'chinese': u'成交时间', 'cellType': BasicCell}
        # d['cancelTime'] = {'chinese': u'撤销时间', 'cellType': BasicCell}
        d['orderState'] = {'chinese': u'订单状态', 'cellType': BasicCell}
        d['price'] = {'chinese': u'价格', 'cellType': BasicCell}
        d['totalVolume'] = {'chinese': u'委托数量', 'cellType': BasicCell}
        d['tradedVolume'] = {'chinese': u'成交数量', 'cellType': BasicCell}
        # d['amt'] = {'chinese': u'金额', 'cellType': BasicCell}

        self.setHeaderDict(d)

        self.setDataKey('orderID')

        self.setFont(BASIC_FONT)
        self.initTable()

        self.setEventType(EVENT_SIGNAL)
        self.registerEvent()
        self.setSorting(True)


# ====================================
class PositionMonitor(BasicMonitor):
    """持仓监控"""
    def __init__(self, mainEngine, eventEngine, cache, parent=None):
        super(PositionMonitor, self).__init__(mainEngine, eventEngine, parent)

        d = OrderedDict()
        d['symbol'] = {'chinese':u'代码', 'cellType':BasicCell}
        d['fhSymbol'] = {'chinese':u'名称', 'cellType':BasicCell}
        d['direction'] = {'chinese':u'方向', 'cellType':BasicCell}
        d['position'] = {'chinese':u'持仓量', 'cellType':BasicCell}
        d['ydPosition'] = {'chinese':u'昨持仓', 'cellType':BasicCell}
        d['frozen'] = {'chinese':u'冻结量', 'cellType':BasicCell}
        d['price'] = {'chinese':u'成本', 'cellType':BasicCell}
        d['nowPrice'] = {'chinese':u'现价', 'cellType':BasicCell}
        # d['gatewayName'] = {'chinese':u'接口', 'cellType':BasicCell}

        self.setHeaderDict(d)

        self.setDataKey('fhPositionName')

        self.setFont(BASIC_FONT)
        self.initTable()

        self.setEventType(EVENT_POSITION)
        self.registerEvent()
        self.setSorting(True)


# ====================================
class AccountMonitor(BasicMonitor):
    """账户资金监控"""
    def __init__(self, mainEngine, eventEngine, cache, parent=None):
        super(AccountMonitor, self).__init__(mainEngine, eventEngine, parent)

        d = OrderedDict()
        d['accountID'] = {'chinese':u'账户', 'cellType':BasicCell}
        d['preBalance'] = {'chinese':u'昨结', 'cellType':BasicCell}
        d['balance'] = {'chinese':u'净值', 'cellType':BasicCell}
        d['available'] = {'chinese':u'可用', 'cellType':BasicCell}
        d['commission'] = {'chinese':u'手续费', 'cellType':BasicCell}
        d['margin'] = {'chinese':u'保证金', 'cellType':BasicCell}
        d['closeProfit'] = {'chinese':u'平仓盈亏', 'cellType':BasicCell}
        d['positionProfit'] = {'chinese':u'持仓盈亏', 'cellType':BasicCell}
        # d['gatewayName'] = {'chinese':u'接口', 'cellType':BasicCell}

        self.setHeaderDict(d)

        self.setDataKey('accountID')

        self.setFont(BASIC_FONT)
        self.initTable()

        self.setEventType(EVENT_ACCOUNT)
        self.registerEvent()
        self.setSorting(True)

