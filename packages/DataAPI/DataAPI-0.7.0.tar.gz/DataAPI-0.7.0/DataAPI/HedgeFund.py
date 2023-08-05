# -*- coding: utf-8 -*-
u"""
Created on 2016-1-4

@author: cheng.li
"""

import copy
import math
import scipy.optimize as opt
import pandas as pd
import numpy as np
import datetime as dt
import functools
from PyFin.Math.Accumulators import MovingSharp
from PyFin.Math.Accumulators import MovingSortino
from PyFin.Math.Accumulators import MovingMaxDrawdown
from DataAPI.Utilities import createEngine
from DataAPI.Utilities import NAMES_SETTINGS
from DataAPI.Utilities import list_to_str
from DataAPI.Utilities import enableCache
from DataAPI.Utilities import cleanColsForUnicode
from DataAPI.Utilities import _setTimeStamp
from DataAPI.Utilities import BAR_TYPE
from DataAPI.Utilities import ASSET_TYPE
from DataAPI.SqlExpressions import Condition


@enableCache
@cleanColsForUnicode
def GetHedgeFundInfo(instruments=None, instrumentName=None, field='*', firstInvestType=None, forceUpdate=True):
    u"""

    获取对冲基金基础信息

    :param instruments: 基金代码列表，例如：'XT1515141.XT'。默认为None，获取所有的基金信息
    :param field: 需要获取的字段类型，例如：['firstInvestType']，不填的话，默认获取所有字段；
                  可用的field包括：[instrumentID, fullName, firstInvestType, investScope,
                  maturityDate, advisory]
    :param firstInvestType: 需要获取的基金所属的投资类型列表，例如: [u'期货型']
    :param forceUpdate: 当为True时强制刷新数据，不使用缓存。默认为True
    :return: pandas.DataFrame
    """

    table_name = 'HEDGEFUND_DESC'

    engine = createEngine('hedge_funds')
    names_mapping = NAMES_SETTINGS[table_name]

    field = list_to_str(field, sep=u'', default_names=names_mapping)

    ins_condition = None
    if instruments:
        instruments_str = list_to_str(instruments)
        ins_condition = Condition(names_mapping[u"instrumentID"], instruments_str, u"in")

    first_invest_condition = None
    if firstInvestType:
        first_invest_srt = list_to_str(firstInvestType)
        first_invest_condition = Condition(names_mapping[u"firstInvestType"], first_invest_srt, u"in")

    name_condition = None
    if instrumentName:
        name_condition = Condition(names_mapping[u"fullName"], "'%" + instrumentName + "%'", u"like")

    sql = u"select {0} from {1}".format(field, table_name)

    whole_condition = None
    if ins_condition:
        whole_condition = ins_condition & first_invest_condition & name_condition
    elif first_invest_condition:
        whole_condition = first_invest_condition & name_condition
    elif name_condition:
        whole_condition = name_condition

    if whole_condition:
        sql += u" where " + whole_condition.__str__()
    data = pd.read_sql(sql, engine)

    if 'instrumentID' in data:
        return data.sort_values('instrumentID').reset_index(drop=True)
    else:
        return data


@enableCache
@cleanColsForUnicode
def GetHedgeFundBarWeek(instruments=None,
                        startDate='2003-01-01',
                        endDate='2015-12-31',
                        field='*',
                        forceUpdate=True,
                        instrumentIDasCol=False):
    u"""

    获取对冲基金历史表现信息(周）

    :param instruments: 基金代码列表，例如：'XT1515141.XT'。默认为None，获取所有基金历史表现
    :param field: 需要获取的字段类型，例如：['logRetAcc']，不填的话，默认获取所有字段；
                  可用的field包括：[tradingDate, instrumentID, navUnit, navAcc,
                  logRetUnit, logRetAcc]
    :param forceUpdate: 当为True时强制刷新数据，不使用缓存。默认为True
    :param instrumentIDasCol: 联合使用field以及instrumentIDs作为column的名字
    :return: pandas.DataFrame
    """
    engine = createEngine('hedge_funds')

    table_name = 'HEDGEFUND_PEF_WEEK'
    names_mapping = NAMES_SETTINGS[table_name]

    field = list_to_str(field, sep=u'', default_names=names_mapping, forced_names=['tradingDate'])
    sql = u"select {0} from {1}".format(field, table_name)

    ins_condition = None
    if instruments:
        instruments_str = list_to_str(instruments)
        ins_condition = Condition(names_mapping[u"instrumentID"], instruments_str, u"in")

    left_td_condition = Condition(names_mapping[u'tradingDate'], startDate.replace('-', ''), '>=')
    right_td_condition = Condition(names_mapping[u'tradingDate'], endDate.replace('-', ''), '<=')

    whole_condition = left_td_condition & right_td_condition & ins_condition

    if whole_condition:
        sql += u" where " + whole_condition.__str__()

    data = pd.read_sql(sql, engine)
    data['tradingDate'] = data['tradingDate'] .apply(lambda x: x[:4] + '-' + x[4:6] + '-' + x[6:8])
    data = _setTimeStamp(data, ASSET_TYPE.HEDGE_FUND, BAR_TYPE.EOD, instrumentIDasCol)
    if instrumentIDasCol:
        data = data[['navAcc', 'navUnit', 'logRetAcc', 'logRetUnit']]
    return data


@enableCache
@cleanColsForUnicode
def GetHedgeFundBarMonth(instruments=None,
                         startDate='2003-01-01',
                         endDate='2015-12-31',
                         field='*',
                         forceUpdate=True,
                         instrumentIDasCol=False):
    u"""

    获取对冲基金历史表现信息(月）

    :param instruments: 基金代码列表，例如：'XT1515141.XT'。默认为None，获取所有基金历史表现
    :param field: 需要获取的字段类型，例如：['logRetAcc']，不填的话，默认获取所有字段；
                  可用的field包括：[tradingDate, instrumentID, navUnit, navAcc,
                  logRetUnit, logRetAcc]
    :param forceUpdate: 当为True时强制刷新数据，不使用缓存。默认为True
    :param instrumentIDasCol: 联合使用field以及instrumentIDs作为column的名字
    :return: pandas.DataFrame
    """
    engine = createEngine('hedge_funds')

    table_name = 'HEDGEFUND_PEF_MONTH'
    names_mapping = NAMES_SETTINGS[table_name]

    field = list_to_str(field, sep=u'', default_names=names_mapping, forced_names=['tradingDate'])
    sql = u"select {0} from {1}".format(field, table_name)

    ins_condition = None
    if instruments:
        instruments_str = list_to_str(instruments)
        ins_condition = Condition(names_mapping[u"instrumentID"], instruments_str, u"in")

    left_td_condition = Condition(names_mapping[u'tradingDate'], startDate.replace('-', ''), '>=')
    right_td_condition = Condition(names_mapping[u'tradingDate'], endDate.replace('-', ''), '<=')

    whole_condition = left_td_condition & right_td_condition & ins_condition

    if whole_condition:
        sql += u" where " + whole_condition.__str__()

    data = pd.read_sql(sql, engine)
    data['tradingDate'] = data['tradingDate'] .apply(lambda x: x[:4] + '-' + x[4:6] + '-' + x[6:8])
    data = _setTimeStamp(data, ASSET_TYPE.HEDGE_FUND, BAR_TYPE.EOD, instrumentIDasCol)
    return data


@enableCache
@cleanColsForUnicode
def GetHedgeFundPool(field='*', refDate=None, forceUpdate=True):
    u"""

    获取指定日期下，基金备选池的信息

    :param field: 需要获取的字段类型，例如：['logRetAcc']，不填的话，默认获取所有字段；
                  可用的field包括：[tradingDate, instrumentID, navUnit, navAcc,
                  logRetUnit, logRetAcc]
    :param refDate: 指定日期，将查询范围限制于当日在基金备选池中的基金，格式为：YYYY-MM-DD；
                    不填的话，默认查询最新的备选池信息
    :param forceUpdate: 当为True时强制刷新数据，不使用缓存。默认为True
    :return: pandas.DataFrame
    """
    engine = createEngine('hedge_funds')
    table_name = 'HEDGEFUND_POOL'
    names_mapping = NAMES_SETTINGS[table_name]

    ref_condition = None
    if refDate:
        ref_condition = Condition(names_mapping[u'eventDate'], refDate.replace(u'-', u''), u"<=")

    sql = u'select * from {0}'.format(table_name)
    if ref_condition:
        sql += u" where " + ref_condition.__str__()

    data = pd.read_sql(sql, engine)
    data = data.groupby(names_mapping['instrumentID']).last()
    data = data[data.eventType == 'A'][['eventDate']]

    # get the detail info of the instruments
    if field != '*':
        if isinstance(field, str):
            field = [field]
        if 'instrumentID' not in field:
            field.append('instrumentID')

    info_data = GetHedgeFundInfo(list(data.index.values), field=field)
    data = pd.merge(data, info_data, left_index=True, right_on='instrumentID')
    return data.sort_values('instrumentID')


@enableCache
@cleanColsForUnicode
def GetHedgeFundStylePerf(styleName=None, startDate='2012-01-01', endDate='2015-12-31', instrumentIDasCol=False, forceUpdate=True):
    u"""

    获取特定风格的基金类型的历史表现

    :param styleName: 基金风格类型，可选的风格有：[u'债券型', u'多空仓型', u'宏观策略', u'市场中性', u'管理期货', u'股票型', u'货币型']
    :param startDate: 历史表现起始日期
    :param endDate: 历史表现结束日期
    :param instrumentIDasCol: 联合使用field以及instrumentIDs作为column的名字
    :param forceUpdate: 当为True时强制刷新数据，不使用缓存。默认为True
    :return: pandas.DataFrame
    """
    engine = createEngine('hedge_funds')
    table_name = 'HOWBUY_STYLE_RET'
    names_mapping = NAMES_SETTINGS[table_name]

    ins_condition = None
    if styleName:
        index_str = list_to_str(styleName, sep=u"'")
        ins_condition = Condition(names_mapping[u'howbuyStrategy'], index_str, u"in")

    left_td_condition = Condition(names_mapping[u'tradingDate'], "'" + startDate + "'", '>=')
    right_td_condition = Condition(names_mapping[u'tradingDate'], "'" + endDate + "'", '<=')

    sql = u'select * from {0}'.format(table_name)

    whole_condition = left_td_condition & right_td_condition & ins_condition

    sql += u" where " + whole_condition.__str__()
    data = pd.read_sql(sql, engine)
    data = data.rename(columns={'howbuyStrategy': 'instrumentID'})
    data = _setTimeStamp(data, ASSET_TYPE.HEDGE_FUND, BAR_TYPE.EOD, instrumentIDasCol)
    data.sort_index(inplace=True)
    return data


def score_data(data):
    # 年化收益得分
    data[u'年化收益得分'] = 0.0

    def return_score(x):
        if x > 0.25:
            return 15.0
        elif x > 0.20:
            return 10.
        elif x > 0.10:
            return 8.
        elif x > 0.05:
            return 4.
        else:
            return 0.
    data[u'年化收益得分'] = data[u'年化收益'].apply(return_score)

    # 夏普比率得分
    data[u'sharp得分'] = 0.0

    def sharp_score(x):
        if x > 2.:
            return 20.0
        elif x > 1.5:
            return 16.
        elif x > 1.0:
            return 10.
        elif x > 0.7:
            return 4.
        else:
            return 0.
    data[u'sharp得分'] = data[u'sharp'].apply(sharp_score)

    # 最大回撤得分
    data[u'最大回撤得分'] = 0.0

    def max_drawdown_score(x):
        if x < 0.03 or np.isnan(x):
            return 10.0
        elif x < 0.05:
            return 8.
        elif x < 0.10:
            return 5.
        elif 0.10 < x < 0.15:
            return 2.
        else:
            return 0.
    data[u'最大回撤得分'] = data[u'最大回撤'].apply(max_drawdown_score)

    # sortino得分
    data[u'sortino得分'] = 0.0

    def sortino_score(x, median):
        if x > median or np.isnan(x):
            return 10.
        else:
            return 5.
    median = data[u'sortino'].median()
    data[u'sortino得分'] = data[u'sortino'].apply(functools.partial(sortino_score, median=median))

    # 收益回撤比得分
    data[u'收益回撤比得分'] = 0.0

    def return_to_max_drawdown_score(x):
        if x > 2.5 or np.isnan(x):
            return 10.0
        elif x > 2:
            return 8.
        elif x > 1.5:
            return 5.
        elif x > 1.0:
            return 2.
        else:
            return 0.
    data[u'收益回撤比得分'] = data[u'收益回撤比'].apply(return_to_max_drawdown_score)

    # 波动率得分
    data[u'波动率得分'] = 0.0

    def volatility_score(x, median):
        if x < median:
            return 5.
        else:
            return 2.
    median = data[u'波动率'].median()
    data[u'波动率得分'] = data[u'波动率'].apply(functools.partial(volatility_score, median=median))

    data[u'总分'] = data[u'年化收益得分'] + data[u'sharp得分'] + data[u'最大回撤得分'] + data[u'sortino得分'] + data[u'收益回撤比得分'] + data[u'波动率得分']
    data.sort_values('总分', ascending=False, inplace=True)
    data.reset_index(inplace=True, drop=True)


@enableCache
@cleanColsForUnicode
def GetHedgeFundPerfComparison(instruments=None, startDate='2015-01-01', endDate='2015-12-31', forceUpdate=True):
    u"""

    获取指定基金的历史表现风险收益指标以及打分结果。

    :param instruments: 基金wind代码列表，可以为空。若为空，则获取所有在池基金的结果。
    :param startDate: 历史表现起始日
    :param endDate: 历史表现结束日
    :param forceUpdate: 当为True时强制刷新数据，不使用缓存。默认为True
    :return: pandas.DataFrame
    """
    data = GetHedgeFundBarWeek(instruments, startDate, endDate)
    groups = data.groupby('instrumentID')

    values = []

    for gname, group in groups:
        if len(group) >= 2:
            returns = group.logRetAcc
            returns.dropna(inplace=True)
            start = returns.index[0]
            end = returns.index[-1]

            annualized_return = returns.mean() * 50
            stddev = returns.std() * math.sqrt(50)

            mdrawdown = MovingMaxDrawdown(len(returns))
            msharp = MovingSharp(len(returns))
            msortino = MovingSortino(len(returns))
            for ret in returns:
                mdrawdown.push({'ret': ret})
                msharp.push({'ret': ret, 'riskFree': 0.})
                msortino.push({'ret': ret, 'riskFree': 0.})
            max_drawdown = -mdrawdown.value[0]
            sharp = msharp.value * math.sqrt(50)
            try:
                sortino = msortino.value * math.sqrt(50)
            except ZeroDivisionError:
                sortino = np.nan
            ret_to_drawdown = annualized_return / max_drawdown
            values.append([])
            values[-1].extend([gname, start, end, annualized_return, stddev, max_drawdown, sharp, sortino, ret_to_drawdown])

    data = pd.DataFrame(data=values, columns=['instrumentID',
                                              'refBegin',
                                              'refEnd',
                                              'annualizedReturn',
                                              'annualizedVolatility',
                                              'maxDrawdown',
                                              'sharp',
                                              'sortino',
                                              'returnToMaxDrawdown'])
    data = data.rename(columns={'instrumentID': u'基金代码',
                                'refBegin': u'参考起始日',
                                'refEnd': u'参考结束日',
                                'annualizedReturn': u'年化收益',
                                'annualizedVolatility': u'波动率',
                                'maxDrawdown': u'最大回撤',
                                'returnToMaxDrawdown': u'收益回撤比'})

    # do the scoring
    score_data(data)

    return data


@enableCache
@cleanColsForUnicode
def GetHedgeFundStyleAnalysis(instruments=None,
                              navTable=pd.DataFrame(),
                              startDate='2012-01-01',
                              endDate='2015-01-01',
                              forceUpdate=True):
    u"""

    获取根据基金历史表现得到的风格分析的结果

    :param instruments: 基金wind代码列表，可以为空。若为空，则使用用户输入的navTable
    :param navTable: N*（M+1）的pandas.DataFrame，表示M个基金历史上N个时间点的净值
    :param startDate: 历史表现起始日，在使用navTable时候会被忽略
    :param endDate:历史表现结束日，在使用navTable时候会被忽略
    :param forceUpdate: 当为True时强制刷新数据，不使用缓存。默认为True
    :return: pandas.DataFrame
    """
    is_ex = False
    if instruments and navTable.empty:
        fund_data = GetHedgeFundBarMonth(instruments=instruments,
                                         startDate=startDate,
                                         endDate=endDate,
                                         instrumentIDasCol=True)['logRetAcc']
    elif not navTable.empty:
        fund_data = navTable
        startDate = navTable.index[0].strftime('%Y-%m-%d')
        endDate = navTable.index[-1].strftime('%Y-%m-%d')
        is_ex = True

    data = GetHedgeFundStylePerf(startDate=startDate, endDate=endDate, instrumentIDasCol=True)
    style_data = data['median_ret'][[u'债券型', u'多空仓型', u'宏观策略', u'市场中性', u'管理期货', u'股票型', u'货币型']]
    style_data.dropna(inplace=True)

    def error_function(*args):
        data = args[1]
        orig = copy.deepcopy(data[:, 7])
        for i in range(7):
            orig -= args[0][i] * data[:, i]

        res = sum(orig * orig)
        return math.sqrt(res)

    def equal_condition(*args):
        return sum(args[0]) - 1.0

    def f_ieq_condition(*args):
        res = []
        for i in range(7):
            res.append(args[0][i])
            res.append(1.0 - args[0][i])
        return res

    all_res = []

    if is_ex:
        fund_data.sort_index(inplace=True)
        fund_data_end = fund_data.groupby(lambda x: dt.datetime(x.year, x.month, 1)).last()
        fund_data_previous = fund_data.groupby(lambda x: dt.datetime(x.year, x.month, 1)).first()
        fund_data = fund_data_end / fund_data_end.shift(1) - 1.0
        if fund_data_end.iloc[0].values != fund_data_previous.iloc[0].values:
            fund_data.iloc[0] = fund_data_end.iloc[0] / fund_data_previous.iloc[0] - 1.0
    else:
        fund_data.index = map(lambda x: dt.datetime(x.year, x.month, 1), fund_data.index)

    for name in fund_data.columns:
        one_fund_data = fund_data[name]
        style_data[name] = one_fund_data * 100.
        data = style_data.dropna()
        del style_data[name]
        data = (data - data.mean()) / data.std()
        data = data.values

        print("{0} style analysis with {1} data observations.".format(name, len(data)))

        res = opt.fmin_slsqp(error_function,
                             [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                             eqcons=(equal_condition,),
                             f_ieqcons=f_ieq_condition,
                             args=(data,),
                             iprint=-1)
        all_res.append(res)

    return pd.DataFrame(all_res, index=fund_data.columns.values, columns=style_data.columns.values)


if __name__ == '__main__':
    perf_data = GetHedgeFundPerfComparison(startDate='2012-03-01',
                                          endDate='2016-03-11')
    print(perf_data)