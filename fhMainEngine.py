# coding=utf-8

"""
Time : 2017/1/23 11:34
Author : Jia Jielin
Company:
File : fhMainEngine.py
Description:

"""


from collections import OrderedDict
from fhDb import DbUtils
from fhGateway import *
import pandas as pd
import datetime
import json


# =================================
class MainEngine:
    """主引擎，负责调度"""

    # -------------------------------------
    def __init__(self):
        # 创建事件驱动引擎
        self.eventEngine = EventEngine2()
        self.eventEngine.start()  # 启动引擎

        # 创建数据引擎
        self.dataEngine = DataEngine(self.eventEngine)

        # 数据库相关
        self.dbUtils = None  # MySQL数据库对象

        # 调用初始化函数，目前只接Wind
        self.initGateway()
        self.strategyList = []

    # -----------------------------
    def initGateway(self):
        """初始化接口对象，目前只有CTP"""
        self.gatewayDict = OrderedDict()
        # # Choice接口初始化
        # try:
        #     from choiceGateway.choiceGateway import ChoiceGateway
        #     self.addGateway(ChoiceGateway, 'Choice')
        # except Exception, e:
        #     print e  # 随后需改为日志输出 todo
        # Wind接口初始化
        try:
            from windGateway.windGateway import WindGateway
            self.addGateway(WindGateway, 'Wind')
        except Exception, e:
            print e  # 随后需改为日志输出 todo

        try:
            from ctpGateway.ctpGateway import CtpGateway
            self.addGateway(CtpGateway, 'CTP')
            self.gatewayDict['CTP'].setQryEnabled(True)
        except Exception, e:
            print e  # 随后需改为日志输出 todo

        # 设计SimuGateway是为了模拟查询数据库交易
        # try:
        #     from simuGateway.simuGateway import SimuGateway
        #     self.addGateway(SimuGateway, 'Simu')
        # except Exception, e:
        #     print e

    # ------------------------------------
    def addGateway(self, gateway, gatewayName=None):
        self.gatewayDict[gatewayName] = gateway(self.eventEngine, gatewayName, self.dataEngine)

    # -------------------------------------------
    def addStrategy(self, strategy):
        if strategy not in self.strategyList:
            self.strategyList.append(strategy)
            return True
        return False

    # --------------------------------------------
    def deleteStrategy(self, strategy):
        if strategy in self.strategyList:
            self.strategyList.remove(strategy)
            return True
        return False

    # ---------------------------------------------
    def connect(self, gatewayName, cache=None):  # gatewayName不是接口名，是'Wind','CTP'等
        """连接特定名称的接口"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            if cache:
                gateway.connect(cache)
            else:
                gateway.connect()
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # ---------------------------------------
    def login(self, gatewayName, user, encPwd):
        """注册特定名称的接口"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.login(user, encPwd)

    # ----------------------------------
    def logout(self, gatewayName, user, encPwd):
        """注册特定名称的接口"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.logout(user, encPwd)
    # -----------------------------
    def disconnect(self, gatewayName):
        """注册特定名称的接口"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.disconnect()

    # -----------------------------------------
    def isConnected(self, gatewayName):
        """确认连接状态"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            return gateway.isConnected()
        else:
            return False
            self.writeLog(u'接口不存在：%s' % gatewayName)

    def subscribe(self, subscribeReq, gatewayName):
        """订阅特定接口的行情"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]

            gateway.subscribe(subscribeReq)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # ------------------------------------------------
    def stopSubscribe(self, reqId, gatewayName):
        """订阅特定接口的行情"""
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Wind':
                gateway = self.gatewayDict[gatewayName]
                gateway.stopSubscribe(reqId)
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # -------------------------------------------------
    # def onAccount(self, product, gatewayName):
    #     """订阅特定接口的行情"""
    #     if gatewayName in self.gatewayDict:
    #         if gatewayName == 'Simu':
    #             gateway = self.gatewayDict[gatewayName]
    #             gateway.onAccount(product)
    #         else:
    #             self.writeLog(u'接口不存在：%s' % gatewayName)
    #     else:
    #         self.writeLog(u'接口不存在：%s' % gatewayName)

    # ---------------------------------------------------
    def offAccount(self, gatewayName, product=None):
        """订阅特定接口的行情"""
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Simu':
                gateway = self.gatewayDict[gatewayName]
                gateway.offAccount(product)
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # ---------------------------------------------------
    # def onPosition(self, product, gatewayName):
    #     """订阅特定接口的行情"""
    #     if gatewayName in self.gatewayDict:
    #         if gatewayName == 'Simu':
    #             gateway = self.gatewayDict[gatewayName]
    #             gateway.onPosition(product)
    #         else:
    #             self.writeLog(u'接口不存在：%s' % gatewayName)
    #     else:
    #         self.writeLog(u'接口不存在：%s' % gatewayName)

    # ---------------------------------------------------
    # def offPosition(self, gatewayName, product=None):
    #     """订阅特定接口的行情"""
    #     if gatewayName in self.gatewayDict:
    #         if gatewayName == 'Simu':
    #             gateway = self.gatewayDict[gatewayName]
    #             gateway.offPosition(product)
    #         else:
    #             self.writeLog(u'接口不存在：%s' % gatewayName)
    #     else:
    #         self.writeLog(u'接口不存在：%s' % gatewayName)
    #
    # # ---------------------------------------------------
    def getHigh5(self, objectList, gatewayName):
        """"""
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Wind':
                gateway = self.gatewayDict[gatewayName]
                return gateway.getHigh5(objectList)
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
                return {}
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)
            return {}

    # ------------------------------------------------
    def halt(self, haltReq, gatewayName):
        """挂起态，simuGateway中用于交易员不再接收任务"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]

            gateway.halt(haltReq)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # -----------------------------------------
    def getPrice(self, subscribeReq, gatewayName):
        """获取一次数据行情"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            return gateway.getPrice(subscribeReq)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)
            return 0

    # ---------------------------------------------------
    def immediateQueryPosition(self, gatewayName):
        # 做即时查询，为了保证撤单后数据不出现问题，目前只CTP接口有
        if gatewayName in self.gatewayDict:
            if gatewayName == 'CTP':
                gateway = self.gatewayDict[gatewayName]
                return gateway.immediateQueryPosition()
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
                return 0
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)
            return 0

    # ------------------------------------------------
    def sendOrder(self, orderReq, gatewayName):
        """对特定接口发单"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            return gateway.sendOrder(orderReq)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)  # todo 需返回标志，用于上层处理

    # ----------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq, gatewayName):
        """对特定接口撤单"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.cancelOrder(cancelOrderReq)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)
            # todo 需返回标志，用于上层处理

    # -----------------------------------------
    def qryAccont(self, gatewayName):
        """查询特定接口的账户"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.getAccount()
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # ------------------------------------------------
    def onAccount(self, account, gatewayName):
        """查询特定接口的账户"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.onAccount(account)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # ------------------------------------------------
    def onPosition(self, account, gatewayName):
        """查询特定接口的账户"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.onPosition(account)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # ------------------------------------------------
    def close(self, gatewayName):
        """对特定接口发单"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            return gateway.close()
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # ------------------------------------------------
    def exit(self):
        """退出程序前调用，保证正常退出"""
        # 安全关闭所有接口
        for gateway in self.gatewayDict.values():
            gateway.close()

        for strategy in self.strategyList:
            try:
                strategy.stop()
            except:
                pass

        # 停止事件引擎
        self.eventEngine.stop()

        # 保存数据引擎里的合约数据到硬盘
        # self.dataEngine.saveData()     # todo

    # -------------------------------------------------
    def writeLog(self, content):
        log = FhLogData()
        log.logContent = content
        event = Event(type_=EVENT_LOG)
        event.dict_['data'] = log
        self.eventEngine.put(event)

    # ----------------------------------------------
    def addDb(self, dbUtils):
        if not self.dbUtils:
            self.dbUtils = dbUtils

    # ------------------------------------------------
    def dbConnect(self):
        """连接MySQL数据库"""
        if not self.dbUtils:
            self.dbUtils = DbUtils()
        if self.dbUtils.isConnected():
            self.writeLog(u'数据库连接成功')
        else:
            self.writeLog(u'数据库连接失败')

    # ------------------------------------------------
    def dbConnected(self):
        return self.dbUtils.isConnected()

    # ----------------------------------------------
    def getSecPrice(self):
        pass

    # -------------------------
    def getAllTask(self, gatewayName):
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Simu':
                gateway = self.gatewayDict[gatewayName]
                gateway.getAllTask()
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # -----------------------------------
    def sendOption(self, option, data, gatewayName):
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.sendOption(option, data)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # -----------------------------------
    def addRemark(self, text, taskNo, subNo, gatewayName):
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Simu':
                gateway = self.gatewayDict[gatewayName]
                gateway.addRemark(text, taskNo, subNo)
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # ---------------------------------------
    def saveSecValue(self, product, totalValue, gatewayName):
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Simu':
                gateway = self.gatewayDict[gatewayName]
                gateway.saveSecValue(product, totalValue)
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)
    # ---------------------------------------
    def saveFuturesTodayInfo(self, product, margin, todayProfit, gatewayName):
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Simu':
                gateway = self.gatewayDict[gatewayName]
                gateway.saveFuturesTodayInfo(product, margin, todayProfit)
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)

    # ----------------------------
    def haveDaysData(self, code, exchange, start, end, gatewayName):
        # 只针对Wind
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Wind':
                gateway = self.gatewayDict[gatewayName]
                code = '.'.join([code, exchange])
                return gateway.haveDaysData(code, start, end)
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
                return -1
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)
            return -1

    # --------------------------------------------------------
    def getDayData(self, code, exchange, start, end, gatewayName):
        # 只针对Wind
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Wind':
                gateway = self.gatewayDict[gatewayName]
                code = '.'.join([code, exchange])
                return gateway.getDayData(code, start, end)
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
                return {}
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)
            return {}

    # --------------------------------------------------------
    def haveTickData(self, code, exchange, start, end, gatewayName, barSize=15):
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Wind':
                gateway = self.gatewayDict[gatewayName]
                code = '.'.join([code, exchange])
                return gateway.haveTickData(code, start, end, barSize)
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
                return -1
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)
            return -1

    # ----------------------------------------------------------------------
    def getTickData(self, code, exchange, start, end, gatewayName, barSize=15):
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Wind':
                gateway = self.gatewayDict[gatewayName]
                code = '.'.join([code, exchange])
                return gateway.getTickData(code, start, end, barSize)
            else:
                self.writeLog(u'接口不存在：%s' % gatewayName)
                return {}
        else:
            self.writeLog(u'接口不存在：%s' % gatewayName)
            return {}

    # ----------------------------------------------------------------------
    def getPriceOnce(self, fhSymbol):
        """查询合约"""
        return self.dataEngine.getPrice(fhSymbol)

    # ----------------------------------------------------------------------
    def getOrder(self, fhOrderID):
        """查询委托"""
        return self.dataEngine.getOrder(fhOrderID)

    # ----------------------------------------------------------------------
    def getAllWorkingOrders(self):
        """查询所有的活跃的委托（返回列表）"""
        return self.dataEngine.getAllWorkingOrders()

    # ----------------------------------------------------------------------
    def putSignalMap(self, fhOrderID, strategyName):
        self.dataEngine.putSignalMap(fhOrderID, strategyName)

    # -------------------------------------------------------------------
    def getOrderByStrategy(self, strategyName):
        return self.dataEngine.getOrderByStrategy(strategyName)

    # -----------------------------------------------
    def getDayOpen(self, code, exchange, gatewayName):
        """仅期货所用"""
        if gatewayName in self.gatewayDict:
            if gatewayName == 'Wind':
                gateway = self.gatewayDict[gatewayName]
                code = '.'.join([code, exchange])
                return gateway.getDayOpen(code)
        return 0

    # ------------------------------------------------
    def getPosition(self, code):
        return self.dataEngine.getPosition(code)


# ============================
class DataEngine(object):
    """数据引擎"""
    billFileName = 'BillData.fh'

    def __init__(self, eventEngine):
        self.eventEngine = eventEngine
        # 订单/任务详细信息字典
        self.billDict = {}
        # 订单数据字典,key:orderID, value:......
        self.orderDict = {}
        # 活动订单/任务字典（即可撤销）
        self.workingOrderDict = {}
        # 读取任务信息 todo 需从Mysql中读取
        self.loadBills()
        # 注册事件监听
        self.registerEvent()
        # MySQL数据库类型
        self.dbUtils = None
        # 账户信息字典
        self.accountDict = {}
        # 订阅信息字典，key:code, value:price
        self.codeDict = {}
        # 仓位信息字典
        self.positionDict = {}
        # 订单信号信息, key:fhOrderID or sessionID, value:dict -> strategyName, orderTime,......用于更新信号订单信息
        self.signalDict = {}
        # 已交易订单信息
        self.tradedOrderList = []
        self.costPriceDict = {}
        self.readSignalMap()

    # ---------------------------------------------
    def getPrice(self, code):
        if code in self.codeDict:
            return self.codeDict[code].lastPrice
        return 0

    # ------------------------------------
    def getOrder(self, fhOrderID):
        """查询下单委托"""
        if fhOrderID in self.orderDict:
            return self.orderDict[fhOrderID]
        return None

    # ----------------------------------------------
    def updateOrder(self, event):
        order = event.dict_['data']
        sig = FhSignalData()
        # d = {}
        # d['code'] = order.symbol
        # d['orderID'] = order.orderID
        # d['fhOrderID'] = order.fhOrderID
        # d['sessionID'] = order.sessionID
        # d['offset'] = order.offset
        # d['orderTime'] = order.orderTime
        # d['cancelTime'] = order.cancelTime
        # d['orderState'] = order.status
        # d['totalVolume'] = order.totalVolume
        # d['tradeVolume'] = order.tradedVolume
        # d['price'] = order.price
        # if order.orderID in self.signalDict:
        #     d['strategyName'] = self.signalDict[order.orderID]['strategyName']

        sig.symbol = order.symbol
        sig.exchange = order.exchange
        sig.orderID = order.orderID
        sig.fhOrderID = order.fhOrderID
        sig.frontID = order.frontID
        sig.sessionID = order.sessionID
        sig.direction = order.direction
        sig.offset = order.offset
        sig.orderTime = order.orderTime
        sig.orderState = order.status
        sig.totalVolume = order.totalVolume
        sig.tradedVolume = order.tradedVolume
        sig.price = order.price
        sig.gatewayName = order.gatewayName
        if order.fhOrderID in self.signalDict:
            sig.strategyName = self.signalDict[order.fhOrderID]['strategyName']
        else:
            sig.strategyName = EMPTY_STRING

        # 放入已交易列表
        if sig.orderID in self.orderDict:
            if (self.orderDict[sig.orderID].orderState == STATUS_NOTTRADED or
                        self.orderDict[sig.orderID].orderState == STATUS_PARTTRADED) and \
                            sig.orderTime == STATUS_ALLTRADED:
                inFlag = False

                if inFlag:
                    self.tradedOrderList.append(sig)
        else:
            if sig.orderState == STATUS_ALLTRADED:
                inFlag = False
                if inFlag:
                    self.tradedOrderList.append(sig)

        self.orderDict[order.orderID] = sig
        self.onSignalOrder()

        # self.saveTraded()   # todo

    # ---------------------------------------------
    def getAllWorkingOrders(self):
        """查询目前活动委托"""
        return self.signalDict.values()

    # --------------------------------------------------
    def registerEvent(self):
        """注册事件监听"""
        self.eventEngine.register(EVENT_ORDER, self.updateOrder)
        # self.eventEngine.register(EVENT_TRADE, self.updateTrade)
        self.eventEngine.register(EVENT_ACCOUNT, self.updateAccount)
        self.eventEngine.register(EVENT_POSITION, self.updatePosition)
        self.eventEngine.register(EVENT_TICK, self.updateTick)

    # ---------------------------------------------------
    def updateAccount(self, event):
        account = event.dict_['data']   # account为FhAccountData
        accountID = account.accountID
        self.accountDict[accountID] = account
        # print self.accountDict

    # -----------------------------------------------------
    def updatePosition(self, event):
        fhPositon = event.dict_['data']   # positon为FhPositionData
        position = {}
        code = fhPositon.symbol
        position['code'] = code
        position['exchange'] = fhPositon.exchange
        position['direction'] = fhPositon.direction
        position['position'] = fhPositon.position
        position['frozen'] = fhPositon.frozen
        position['price'] = fhPositon.price
        position['ydPosition'] = fhPositon.ydPosition

        # 未在持仓字典中，则添加
        if code not in self.positionDict:
            self.positionDict[code] = []
            self.positionDict[code].append(position)
        else:
            # 判断code是多还是空
            lenPosCode = len(self.positionDict[code])
            # 如果为空，需增加
            if lenPosCode == 0:
                self.positionDict[code] = []
                self.positionDict[code].append(position)
            # 如果为1，需判断
            elif lenPosCode == 1:
                if self.positionDict[code][0]['direction'] != position['direction']:
                    self.positionDict[code].append(position)
                else:
                    self.positionDict[code][0]['code'] = code
                    self.positionDict[code][0]['exchange'] = fhPositon.exchange
                    self.positionDict[code][0]['direction'] = fhPositon.direction
                    self.positionDict[code][0]['position'] = fhPositon.position
                    self.positionDict[code][0]['frozen'] = fhPositon.frozen
                    self.positionDict[code][0]['price'] = fhPositon.price
                    self.positionDict[code][0]['ydPosition'] = fhPositon.ydPosition
            elif lenPosCode == 2:
                for item in self.positionDict[code]:
                    if item['direction'] == position['direction']:
                        item['code'] = code
                        item['exchange'] = fhPositon.exchange
                        item['direction'] = fhPositon.direction
                        item['position'] = fhPositon.position
                        item['frozen'] = fhPositon.frozen
                        item['price'] = fhPositon.price
                        item['ydPosition'] = fhPositon.ydPosition
        # print self.positionDict

    # ------------------------------------------------------
    def updateTick(self, event):
        tick = event.dict_['data']
        code = tick.symbol
        if code:
            self.codeDict[code] = tick

        return 0

    # ---------------------------------
    def putSignalMap(self, orderID, strategyName):
        if orderID not in self.signalDict:
            self.signalDict[orderID] = {}
            self.signalDict[orderID]['strategyName'] = strategyName
            self.signalDict[orderID]['fhOrderID'] = orderID
        else:
            self.signalDict[orderID]['strategyName'] = strategyName
            self.signalDict[orderID]['fhOrderID'] = orderID
        self.saveSignalMap()

    # ------------------------------------------------------
    # def changeSignalMap(self, fhOrderID, sessionID):
    #     if fhOrderID in self.signalDict:
    #         d = self.signalDict[fhOrderID]
    #         self.saveSignalMap()

    # ---------------------------------------------------------
    def saveSignalMap(self):
        saveDate = datetime.datetime.now().strftime('%Y%m%d')
        self.signalDict['time'] = saveDate
        with open('signalMap.json', 'w') as f:
            f.write(json.dumps(self.signalDict, ensure_ascii=False, indent=2))

    # -------------------------------------------------
    def readSignalMap(self):
        now = datetime.datetime.now().strftime('%Y%m%d')
        setNull = False
        with open('signalMap.json') as f:
            signalMap = json.load(f)
            if 'time' in signalMap:
                if signalMap['time'] == now:
                    self.signalDict = signalMap
                else:
                    self.signalDict = {}
                    setNull = True
            else:
                self.signalDict = {}
                setNull = True

        if setNull:
            self.saveSignalMap()

    # ---------------------------------------------------
    def onSignalOrder(self):
        for item in self.orderDict.values():
            event1 = Event(type_=EVENT_SIGNAL)
            event1.dict_['data'] = item
            self.eventEngine.put(event1)

    # -----------------------------------------------------
    def getOrderByStrategy(self, strategyName):
        fhOrderIDList = []
        retList = []
        for fhOrderID in self.signalDict:
            if 'strategyName' in self.signalDict[fhOrderID]:
                if self.signalDict[fhOrderID]['strategyName'] == strategyName:
                    fhOrderIDList.append(fhOrderID)
        for orderID in self.orderDict:
            if self.orderDict[orderID].fhOrderID in fhOrderIDList:
                retList.append(self.orderDict[orderID])
        return retList

    # -----------------------------------------------------
    def getPosition(self, code):
        if code in self.positionDict:
            return self.positionDict[code]
        return []
    # -------------------------------------------------
    def saveData(self):
        """保存到数据库"""
        pass

    # ---------------------
    def loadBills(self):
        pass


# =====================================
def readCsv(fileName):
    """
    output: pd.DataFrame
    """
    try:
        frame = pd.read_csv(fileName)
    except:
        return pd.DataFrame([])
    try:
        del frame['Unnamed: 0']
    except:
        pass
    return frame

