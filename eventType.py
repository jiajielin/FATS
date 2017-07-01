# coding=utf-8

"""
Time : 2017/1/23 11:03
Author : Jia Jielin
Company:
File : eventType.py
Description:

"""

# 系统相关
EVENT_TIMER = 'eTimer'                  # 计时器事件，每隔1秒发送一次
EVENT_LOG = 'eLog'                      # 日志事件，通常使用某个监听函数直接显示

EVENT_TASK = 'eTask'                    # 任务事件，用于界面向后端传递任务更新信息
EVENT_TASK_LOGIN = 'eTaskLogin'         # 服务器登录事件
EVENT_TASK_REQ = 'eTaskReq'             # 任务请求，用于向服务器发送请求交易，增量请求，仅返回变动量
EVENT_TASK_ALL = 'eTaskAll'             # 任务全量请求，用于向服务器发送全量任务请求交易
EVENT_TASK_LOGOUT = 'eTaskLogout'       # 服务器登出事件
EVENT_TASK_HALT_ON = 'eTaskHaltOn'      # 服务器挂起事件
EVENT_TASK_HALT_OFF = 'eTaskHaltOff'    # 服务器解挂起事件

# Gateway相关
EVENT_TICK = 'eTick.'                   # TICK行情事件，可后接具体的vtSymbol
EVENT_ERROR = 'eError.'                 # 错误回报事件
EVENT_CONTRACT = 'eContract.'           # 合约基础信息回报事件

# EVENT_TICK_SEC = 'eTickSec'             # TICK股票行情，包含所有

EVENT_TDLOGIN = 'eTdLogin'                  # 交易服务器登录成功事件

EVENT_MARKETDATA = 'eMarketData'            # 行情推送事件
EVENT_MARKETDATA_CONTRACT = 'eMarketData.'  # 特定合约的行情事件

EVENT_TRADE = 'eTrade'                      # 成交推送事件
EVENT_TRADE_CONTRACT = 'eTrade.'            # 特定合约的成交事件

EVENT_ORDER = 'eOrder'                      # 报单推送事件
EVENT_ORDER_ORDERREF = 'eOrder.'            # 特定报单号的报单事件

EVENT_POSITION_REQ = 'ePositionReq'         # 持仓查询请求事件
EVENT_POSITION = 'ePosition'                # 持仓查询回报事件
EVENT_POSITION_ALL = 'ePositionAll'         # 持仓查询更新事件

EVENT_INSTRUMENT = 'eInstrument'            # 合约查询回报事件
EVENT_INVESTOR = 'eInvestor'                # 投资者查询回报事件

EVENT_ACCOUNT_REQ = 'eAccountReq'           # 账户查询请求事件
EVENT_ACCOUNT = 'eAccount'                  # 账户查询回报事件
EVENT_ACCOUNT_ALL = 'eAccountAll'           # 账户查询更新事件
EVENT_ACCOUNT_SHOW = 'eAccountShow'         # 账户前端显示统计信息

# Wind接口相关
EVENT_WIND_CONNECTREQ = 'eWindConnectReq'   # Wind接口请求连接事件

# 策略相关
EVENT_SIGNAL = 'eSignal'        # 信号返回接口


# -------------------------------------
def test():
    """检查是否存在内容重复的常量定义"""
    check_dict = {}

    global_dict = globals()
    # print global_dict

    for key, value in global_dict.items():
        if '__' not in key:                       # 不检查python内置对象
            if value in check_dict:
                check_dict[value].append(key)
            else:
                check_dict[value] = [key]

    for key, value in check_dict.items():
        if len(value) > 1:
            print u'存在重复的常量定义:' + str(key)
            for name in value:
                print name
            print ''

    print u'测试完毕'


# 直接运行脚本可以进行测试
if __name__ == '__main__':
    test()