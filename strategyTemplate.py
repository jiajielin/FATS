# coding=utf-8

"""
Time : 2017/3/8 10:40
Author : Jia Jielin
Company:
File : strategyTemplate.py
Description:

"""

from fhGateway import *
import sched

import datetime


class StrategyTemplate(object):
    """策略模板"""
    def __init__(self, mainEngine, eventEngine, cache):
        # 引擎
        self.mainEngine = mainEngine
        self.eventEngine = eventEngine
        # 缓存
        self.cache = cache
        # 策略名
        self.strategyName = self.__class__.__name__
        # 策略所需订阅代码集
        self.strategyCodeList = []
        # 订阅代码标记
        self.isSubscribed = False
        # 策略运行标记
        self.isStarted = False
        # 策略运行线程
        self.strategyThread = None
        # 策略循环运行间隔
        self.interval = 2
        self.longInterval = 4 * self.interval
        self.startTime = '093000'   # 定义开始运行时间，若self.timingFlag为False，该属性未用到
        self.endTime = '150000'     # 定义结束运行时间，若self.timingFlag为False，该属性未用到
        self.midTime1 = '113100'    # 中午休息开始时间
        self.midTime2 = '130000'    # 中午休息结束时间

        # 是否数据及交易接口存在
        self.hasGateway = self.verifyGateway()

        # # 未成交订单取消时间间隔
        # self.cancelOrderInterval = self.interval - 0.5
        self.gateway = ''
        self.dataGateway = ''
        self.riskManageFlag = False
        self.timingFlag = True  # 定时启动algo标记，为True，则在onCondition中设置定时运行的条件，若为False，则始终轮询

    # -------------------------------------
    def setTimingFlag(self, timingFlag):
        self.timingFlag = timingFlag

    # -----------------------------------------
    def setStrategyName(self, name):
        self.strategyName = name

    # -------------------------------------
    def setSleepInterval(self, interval):
        self.interval = interval

    # --------------------------------------
    def setStarted(self, isStarted):
        self.isStarted = isStarted

    # ---------------------------------------
    def setStrategyCodeList(self, codeList):
        if type(codeList) == list:
            self.strategyCodeList = codeList
        else:
            self.onLog(u'设置代码集合有误，请重新输入')

    # ----------------------------------------
    def setRiskManage(self, flag):
        self.riskManageFlag = flag

    # ------------------------------------------
    def riskManage(self):
        return self.riskManageFlag

    # -----------------------------------------
    def verifyGateway(self):
        """核实类所需接口是否存在，在self.cache中查找，需子类重写"""
        return True

    # -----------------------------------------
    def subscribe(self):
        """开启订阅，CTP接口暂不需子类重写"""
        # print self.verifyGateway()
        if self.hasGateway:
            if self.gateway:
                for code in self.strategyCodeList:
                    req = FhSubscribeReq()
                    req.symbol = code
                    self.mainEngine.subscribe(req, self.gateway)
                self.isSubscribed = True
            else:
                self.isSubscribed = False
                self.onLog(u'未定义接口，请确认')
        else:
            self.isSubscribed = False
            self.onLog(u'接口连接有误，请连接后再操作')

    # -----------------------------------
    def stopSubscribe(self):
        """停止订阅，需子类重写,不重写亦无影响，CTP接口暂无"""
        self.isSubscribed = False

    # --------------------------------
    def algo(self):
        """策略主体，需子类重写"""
        self.onLog(u'未定义策略主体，只输出日志')

    # ------------------------------------
    def onAlog(self):
        while self.isStarted:
            self.algo()
            sleep(self.interval)

    # ---------------------------------------
    def onTiming(self):
        while self.isStarted:
            now = datetime.datetime.now().strftime('%H%M%S')
            if now < self.startTime:
                sleep(self.interval)
            elif now > self.midTime1 and now < self.midTime2:
                sleep(self.interval)
            elif now > self.endTime:
                self.setStarted(False)
                self.onLog(u'今日交易时间已过，结束策略')
            elif self.onCondition():
                self.algo()
                sleep(self.longInterval)
            else:
                sleep(self.interval)

    # ----------------------------------------
    def onCondition(self):
        """定时器条件设置，需子类重写"""
        return False

    # ---------------------------------------
    def start(self):
        # 测试用
        self.updatePosition()
        self.subscribe()
        if self.dataPrepare():
            if self.isSubscribed:
                self.isStarted = True
                if self.timingFlag:
                    self.strategyThread = Thread(target=self.onTiming)
                else:
                    self.strategyThread = Thread(target=self.onAlog)
                self.strategyThread.start()
                self.onLog(u'策略开始运行')
            else:
                self.onLog(u'尚未订阅行情，请订阅后运行策略')
        else:
            self.onLog(u'dataPrepare模块有误，请查看，策略启动失败')

    # --------------------------------------------
    def stop(self):
        if self.isStarted:
            self.isStarted = False
            self.strategyThread.join()
            # sleep(0.5)
            self.strategyThread = None
            self.onLog(u'策略停止')
        self.stopSubscribe()
    # ------------------------------------------
    def dataPrepare(self):
        return True

    # ----------------------------------------
    def onLog(self, logContent):
        """日志推送"""
        log = FhLogData()
        log.gatewayName = self.strategyName
        log.logContent = logContent
        event1 = Event(type_=EVENT_LOG)
        event1.dict_['data'] = log
        self.eventEngine.put(event1)

    # ---------------------------------------------
    def sendOrder(self, code, exchange, price, volume, priceType, direction, offset):
        """发单"""
        req = FhOrderReq()
        req.symbol = code
        req.exchange = exchange
        req.price = price
        req.priceType = priceType
        req.volume = volume
        req.direction = direction   # DIRECITON_LONG DIRECTION_SHORT
        req.offset = offset
        req.comment = self.strategyName

        fhOrderID = self.mainEngine.sendOrder(req, self.gateway)
        # now = datetime.datetime.now()
        self.mainEngine.putSignalMap(fhOrderID, self.strategyName)

    # ----------------------------------------------
    def cancelOrder(self):
        """取消当前策略对应订单"""
        orderList = self.mainEngine.getOrderByStrategy(self.strategyName)
        # print orderList
        for order in orderList:
            req = FhCancelOrderReq()
            req.symbol = order.symbol
            req.exchange = order.exchange
            req.frontID = order.frontID
            req.sessionID = order.sessionID
            req.orderID = order.orderID
            # print req.symbol
            # print req.exchange
            # print req.frontID
            # print req.sessionID
            # print req.orderID
            if order.orderState == STATUS_NOTTRADED or order.orderState == STATUS_PARTTRADED:
                self.mainEngine.cancelOrder(req, order.gatewayName)

    # ---------------------------------------------
    def getPrice(self, code):
        return self.mainEngine.getPriceOnce(code)   # 调用subscribe暂存dataEngine的数据

    # ---------------------------------------
    def getDayOpen(self, code, exchange):
        return self.mainEngine.getDayOpen(code, exchange, self.dataGateway)

    # --------------------------------------------
    def getPosition(self, code):
        return self.mainEngine.getPosition(code)

    # ----------------------------------------------
    def updatePosition(self):
        # print '--- updatePosition ----',datetime.datetime.now()
        self.mainEngine.immediateQueryPosition(self.gateway)
        # print '--- end ---:',datetime.datetime.now()

# ===============================================

STRATEGY_CLASS = {}
STRATEGY_CLASS['StrategyTemplate'] = StrategyTemplate


class SignalInfo(object):
    """信号传递信息"""
    def __init__(self):
        self.symbol = ''
        self.exchange = u''

        self.position = u'' # 买入；卖出
        self.strategyName = u''
        self.time = '2000-01-01 00:00:00'
        self.price = -1.0
        self.volume = 0


# =========================================







