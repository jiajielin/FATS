# coding=utf-8

"""
Time : 2017/1/23 11:08
Author : Jia Jielin
Company:
File : fhGateway.py
Description:

"""

from eventEngine import *
from fhConstant import *
import time


class FhGateway(object):
    """交易接口，用于其他接口来继承"""

    # ------------------------
    def __init__(self, eventEngine, gatewayName, dataEngine=None):
        self.eventEngine = eventEngine
        self.gatewayName = gatewayName
        self.dataEngine = dataEngine

    # -------------------------
    def onTick(self, tick):
        """行情推送"""
        event1 = Event(type_=EVENT_TICK)
        event1.dict_['data'] = tick
        self.eventEngine.put(event1)

        # 特定合约代码事件
        # event2 = Event(type_=EVENT_TICK + tick.fhSymbol)
        # event2.dict_['data'] = tick
        # self.eventEngine.put(event2)

    # ----------------------------
    def onTrade(self, trade):
        """成交信息推送，目前不需要"""
        # todo
        pass

    # ---------------------------
    def onOrder(self, order):
        """订单变化推送"""
        # 通用事件
        event1 = Event(type_=EVENT_ORDER)
        event1.dict_['data'] = order
        self.eventEngine.put(event1)

        # # 特定订单编号的事件
        # event2 = Event(type_=EVENT_ORDER+order.vtOrderID)
        # event2.dict_['data'] = order
        # self.eventEngine.put(event2)

    # ------------------------
    def onPosition(self, position):
        """持仓信息推送"""
        # 通用事件
        event1 = Event(type_=EVENT_POSITION)
        event1.dict_['data'] = position
        self.eventEngine.put(event1)

        # # 特定合约代码的事件
        # event2 = Event(type_=EVENT_POSITION+position.vtSymbol)
        # event2.dict_['data'] = position
        # self.eventEngine.put(event2)

    # -----------------------
    def onAccount(self, account):
        """账户信息推送，目前不需要"""
        # 通用事件
        event1 = Event(type_=EVENT_ACCOUNT)
        event1.dict_['data'] = account
        self.eventEngine.put(event1)

        # # 特定合约代码的事件
        # event2 = Event(type_=EVENT_ACCOUNT+account.fhAccountID)
        # event2.dict_['data'] = account
        # self.eventEngine.put(event2)

    # -------------------
    def onError(self, error):
        """错误信息推送"""
        # 通用事件
        # event1 = Event(type_=EVENT_ERROR)
        # event1.dict_['data'] = error
        log = FhLogData()
        log.gatewayName = error.gatewayName
        log.logContent = error.errorMsg +error.additionalInfo + unicode('-ErrorID:') + unicode(error.errorID)
        event1 = Event(type_=EVENT_LOG)
        event1.dict_['data'] = log

        self.eventEngine.put(event1)

    # -------------------------
    def onLog(self, log):
        """日志推送"""
        event1 = Event(type_=EVENT_LOG)
        event1.dict_['data'] = log
        self.eventEngine.put(event1)

    # -----------------------------
    def onContract(self, contract):
        """合约基础信息推送"""
        # 通用事件
        event1 = Event(type_=EVENT_CONTRACT)
        event1.dict_['data'] = contract
        self.eventEngine.put(event1)

    # ----------------------------
    def isConnected(self):
        """判断连接状态"""
        pass

    # ----------------------------
    def connect(self):
        """连接"""
        pass

    # ---------------------------------
    def subscribe(self, subscribeReq):
        """订阅行情"""
        pass

    # ---------------------------------
    def stopSubscribe(self, reqId=None):
        """订阅行情"""
        pass

    # ---------------------------------
    def getPrice(self, subscribeReq):
        """获取一次"""
        pass

    # ---------------------------------
    def sendOrder(self, orderReq):
        """发单"""
        pass

    # -------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """撤单"""
        pass

    # -----------------------------------
    def qryAccount(self):
        """查询账户资金"""
        pass

    # ------------------------
    def qryPosition(self):
        """查询持仓"""
        pass

    # -----------------------------------
    def close(self):
        """关闭"""
        pass

    # ---------------------------------
    def sendOption(self, option):
        # 目前只Simu需要
        pass


# ================================================
class FhBaseData(object):
    """基础数据类"""

    def __init__(self):
        self.gatewayName = EMPTY_STRING  # Gateway名称
        self.rawData = None  # 原始数据


# ===================================================
class FhTickData(FhBaseData):
    """Tick行情数据类"""

    # --------------------------------------
    def __init__(self):
        super(FhTickData, self).__init__()

        # 代码相关
        self.symbol = EMPTY_STRING  # 合约代码/股票代码
        self.exchange = EMPTY_STRING  # 交易所代码
        self.fhSymbol = EMPTY_STRING  # 合约在FHTrader中的唯一代码，通常是 合约代码.交易所代码，实际中，Wind代码即是该代码

        # 成交数据
        self.lastPrice = EMPTY_STRING  # 最新成交价
        self.lastVolume = EMPTY_INT  # 最新成交量
        self.volume = EMPTY_INT  # 今天总成交量
        self.openInterest = EMPTY_INT  # 持仓量
        self.time = EMPTY_STRING  # 时间
        self.date = EMPTY_STRING  # 日期

        self.upperLimit = EMPTY_STRING  # 涨停价
        self.lowerLimit = EMPTY_STRING  # 跌停价


# ===========================
class FhLogData(FhBaseData):
    """"""

    # --------------------------------
    def __init__(self):
        super(FhLogData, self).__init__()
        self.logTime = time.strftime('%X', time.localtime())  # 生成日志事件
        self.gatewayName = EMPTY_UNICODE
        self.logContent = EMPTY_UNICODE


# ===============================
class FhSubscribeReq(object):
    """订阅行情时传入的对象类"""

    def __init__(self):
        self.symbol = EMPTY_STRING  # 代码
        self.exchange = EMPTY_STRING  # 交易所
        self.objectClass = EMPTY_INT # 产品类型，一般就股票和期货，股票0，期货1
        self.fields = ''            # 请求字段，Wind需要


class FhOrderReq(object):
    """下单对象类，实际下单用，目前暂时不需要"""

    def __init__(self):
        self.symbol = EMPTY_STRING  # 代码
        self.exchange = EMPTY_STRING  # 交易所
        self.price = EMPTY_FLOAT  # 价格
        self.volume = EMPTY_INT  # 数量

        self.priceType = EMPTY_STRING  # 价格类型
        self.direction = EMPTY_STRING  # 买卖
        self.offset = EMPTY_STRING  # 开平
        # 备注信息
        self.comment = EMPTY_STRING

        # 以下为IB相关
        self.productClass = EMPTY_UNICODE  # 合约类型
        self.currency = EMPTY_STRING  # 合约货币
        self.expiry = EMPTY_STRING  # 到期日
        self.strikePrice = EMPTY_FLOAT  # 行权价
        self.optionType = EMPTY_UNICODE  # 期权类型


# =============================
class FhCancelOrderReq(object):
    """撤单传入对象类，实际下单用，目前暂时不需要"""

    def __init__(self):
        self.symbol = EMPTY_STRING  # 代码
        self.exchange = EMPTY_STRING  # 交易所

        # 以下字段主要和CTP、LTS类接口相关
        self.orderID = EMPTY_STRING  # 报单号
        self.frontID = EMPTY_STRING  # 前置机号
        self.sessionID = EMPTY_STRING  # 会话号


# ========================================
class FhTaskReq(object):
    """任务下单对象类"""

    def __init__(self):
        self.taskId = EMPTY_STRING
        self.subtaskId = EMPTY_STRING

        self.symbol = EMPTY_STRING
        self.exchange = EMPTY_STRING
        self.price = EMPTY_FLOAT
        self.volume = EMPTY_INT
        self.priceType = EMPTY_STRING
        self.direction = EMPTY_STRING

        self.fundManager = EMPTY_STRING
        self.trader = EMPTY_STRING


# ===========================================
class FhCancelTaskReq(object):
    """任务下单取消对象类"""

    def __init__(self):
        self.taskId = EMPTY_STRING
        self.subtaskId = EMPTY_STRING


# ============================================
class FhAccountData(FhBaseData):
    """账户数据类"""

    # ----------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(FhAccountData, self).__init__()

        # 账号代码相关
        self.accountID = EMPTY_STRING           # 账户代码
        self.fhAccountID = EMPTY_STRING         # 账户在系统中的唯一代码，通常是 Gateway名.账户代码

        # 数值相关
        self.preBalance = EMPTY_FLOAT           # 昨日账户结算净值
        self.balance = EMPTY_FLOAT              # 账户净值
        self.available = EMPTY_FLOAT            # 可用资金
        self.commission = EMPTY_FLOAT           # 今日手续费
        self.margin = EMPTY_FLOAT               # 保证金占用
        self.closeProfit = EMPTY_FLOAT          # 平仓盈亏
        self.positionProfit = EMPTY_FLOAT       # 持仓盈亏


# ================================================================
class FhErrorData(FhBaseData):
    """错误数据类"""

    # -----------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(FhErrorData, self).__init__()

        self.errorID = EMPTY_STRING             # 错误代码
        self.errorMsg = EMPTY_UNICODE           # 错误信息
        self.additionalInfo = EMPTY_UNICODE     # 补充信息


# =========================================
class FhContractData(FhBaseData):
    """合约详细信息类"""

    # ----------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(FhContractData, self).__init__()

        self.symbol = EMPTY_STRING              # 代码
        self.exchange = EMPTY_STRING            # 交易所代码
        self.fhSymbol = EMPTY_STRING            # 合约在系统中的唯一代码，通常是 合约代码.交易所代码
        self.name = EMPTY_UNICODE               # 合约中文名

        self.productClass = EMPTY_UNICODE       # 合约类型
        self.size = EMPTY_INT                   # 合约大小
        self.priceTick = EMPTY_FLOAT            # 合约最小价格TICK

        # 期权相关
        self.strikePrice = EMPTY_FLOAT          # 期权行权价
        self.underlyingSymbol = EMPTY_STRING    # 标的物合约代码
        self.optionType = EMPTY_UNICODE         # 期权类型


# =====================================
class FhOrderData(FhBaseData):
    """订单数据类"""

    # -----------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(FhOrderData, self).__init__()

        # 代码编号相关
        self.symbol = EMPTY_STRING              # 合约代码
        self.exchange = EMPTY_STRING            # 交易所代码
        self.fhSymbol = EMPTY_STRING            # 合约在系统中的唯一代码，通常是 合约代码.交易所代码

        self.orderID = EMPTY_STRING             # 订单编号
        self.fhOrderID = EMPTY_STRING           # 订单在系统中的唯一编号，通常是 Gateway名.订单编号

        # 报单相关
        self.direction = EMPTY_UNICODE          # 报单方向
        self.offset = EMPTY_UNICODE             # 报单开平仓
        self.price = EMPTY_FLOAT                # 报单价格
        self.totalVolume = EMPTY_INT            # 报单总数量
        self.tradedVolume = EMPTY_INT           # 报单成交数量
        self.status = EMPTY_UNICODE             # 报单状态

        self.orderTime = EMPTY_STRING           # 发单时间
        self.cancelTime = EMPTY_STRING          # 撤单时间

        # CTP/LTS相关
        self.frontID = EMPTY_INT                # 前置机编号
        self.sessionID = EMPTY_INT              # 连接编号


# =======================================
class FhTradeData(FhBaseData):
    """成交数据类"""

    # -----------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(FhTradeData, self).__init__()

        # 代码编号相关
        self.symbol = EMPTY_STRING              # 合约代码
        self.exchange = EMPTY_STRING            # 交易所代码
        self.fhSymbol = EMPTY_STRING            # 合约在系统中的唯一代码，通常是 合约代码.交易所代码

        self.tradeID = EMPTY_STRING             # 成交编号
        self.fhTradeID = EMPTY_STRING           # 成交在系统中的唯一编号，通常是 Gateway名.成交编号

        self.orderID = EMPTY_STRING             # 订单编号
        self.fhOrderID = EMPTY_STRING           # 订单在系统中的唯一编号，通常是 Gateway名.订单编号

        # 成交相关
        self.direction = EMPTY_UNICODE          # 成交方向
        self.offset = EMPTY_UNICODE             # 成交开平仓
        self.price = EMPTY_FLOAT                # 成交价格
        self.volume = EMPTY_INT                 # 成交数量
        self.tradeTime = EMPTY_STRING           # 成交时间


# ======================================================
class FhPositionData(FhBaseData):
    """持仓数据类"""

    # -----------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(FhPositionData, self).__init__()

        # 代码编号相关
        self.symbol = EMPTY_STRING              # 合约代码
        self.exchange = EMPTY_STRING            # 交易所代码
        self.fhSymbol = EMPTY_STRING            # 合约在fh系统中的唯一代码，合约代码.交易所代码

        # 持仓相关
        self.direction = EMPTY_STRING           # 持仓方向
        self.position = EMPTY_INT               # 持仓量
        self.frozen = EMPTY_INT                 # 冻结数量
        self.price = EMPTY_FLOAT                # 持仓均价
        self.nowPrice = EMPTY_FLOAT             # 现价
        self.fhPositionName = EMPTY_STRING      # 持仓在fh系统中的唯一代码，通常是fhSymbol.方向

        self.todayPosition = EMPTY_INT          # 今持仓
        self.ydPosition = EMPTY_INT             # 昨持仓


# ========================================================
class FhSignalData(FhBaseData):
    """信号类"""
    def __init__(self):
        super(FhSignalData, self).__init__()

        self.symbol = EMPTY_STRING
        self.exchange = EMPTY_STRING
        self.orderID = EMPTY_STRING
        self.fhOrderID = EMPTY_STRING
        self.sessionID = EMPTY_INT      # CTP
        self.frontID = EMPTY_INT
        self.direction = EMPTY_UNICODE
        self.offset = EMPTY_UNICODE
        self.orderTime = EMPTY_STRING
        self.cancelTime = EMPTY_STRING
        self.orderState = EMPTY_UNICODE
        self.totalVolume = EMPTY_INT
        self.tradedVolume = EMPTY_INT
        self.price = EMPTY_FLOAT
        self.strategyName = EMPTY_STRING