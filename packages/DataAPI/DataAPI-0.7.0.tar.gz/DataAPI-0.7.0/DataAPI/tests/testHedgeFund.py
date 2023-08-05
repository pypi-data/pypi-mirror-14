# -*- coding: utf-8 -*-
u"""
Created on 2016-1-5

@author: cheng.li
"""

import unittest
from DataAPI import api


class TestHedgeFund(unittest.TestCase):

    def test_hedge_fund_info(self):
        data = api.GetHedgeFundInfo()
        self.assertTrue(len(data) > 1)

    def test_hedge_fund_info_with_specific_first_invest(self):
        data = api.GetHedgeFundInfo(firstInvestType=u'股票型')
        first_invest_types = data.firstInvestType.values
        for ftype in first_invest_types:
            self.assertEqual(ftype, u'股票型')

    def test_hedge_fund_info_with_wrong_field(self):
        with self.assertRaises(ValueError):
            _ = api.GetHedgeFundInfo(field='listDate')

    def test_hedge_fund_info_with_specific_field(self):
        data = api.GetHedgeFundInfo(field='fullName')
        self.assertTrue('fullName' in data)
        self.assertTrue('instrumentID' not in data)

    def test_hedge_fund_bar_week_with_specific_instrument(self):
        data = api.GetHedgeFundBarWeek('XT125853.XT')
        instruments = data.instrumentID.unique()
        self.assertEqual(len(instruments), 1)
        self.assertEqual(instruments[0], u'XT125853.XT')

    def test_hedge_fund_bar_week_with_wrong_field(self):
        with self.assertRaises(ValueError):
            _ = api.GetHedgeFundBarWeek(field='listDate')

    def test_hedge_fund_bar_week_with_specific_field(self):
        data = api.GetHedgeFundBarWeek(field='navUnit')
        self.assertTrue('navUnit' in data)
        self.assertTrue('navAcc' not in data)

    def test_hedge_fund_style_ret(self):
        data = api.GetHedgeFundStylePerf(styleName=u'债券型', startDate='2014-01-01', endDate='2016-02-01')
        self.assertEqual(len(data), 26)

    def test_hedge_fund_style_analysis(self):
        styles = [u'债券型', u'多空仓型', u'宏观策略', u'市场中性', u'管理期货', u'股票型', u'货币型']

        for style in styles:
            data = api.GetHedgeFundStylePerf(styleName=style, startDate='2014-01-01', endDate='2016-02-01')
            data['nav'] = (1. + data['median_ret'] / 100.).cumprod()
            specific_data = data[['nav']]
            res = api.GetHedgeFundStyleAnalysis(navTable=specific_data)
            self.assertAlmostEqual(res[style][0], 1.0)
