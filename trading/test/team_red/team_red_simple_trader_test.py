"""
Created on 19.11.2017

Module for testing the SimpleTrader.

@author: rmueller
"""
import unittest

from definitions import PERIOD_1
from model.Order import CompanyEnum
from model.Portfolio import Portfolio
from predicting.predictor.reference.perfect_predictor import PerfectPredictor
from trading.trader.team_red.team_red_simple_trader import TeamRedSimpleTrader
from utils import read_stock_market_data


class TeamBlueSimpleTraderWithPerfectPredictorTest(unittest.TestCase):

    def setUp(self):
        self.trader = TeamRedSimpleTrader(PerfectPredictor(CompanyEnum.COMPANY_A),
                                          PerfectPredictor(CompanyEnum.COMPANY_B))
        pass

    def tearDown(self):
        pass

    def testDataCanBeRead(self):
        self.assertIsNotNone(self.trader)
        stock_market_data = read_stock_market_data([CompanyEnum.COMPANY_A], [PERIOD_1])
        self.assertIsNotNone(stock_market_data)
        portfolio = Portfolio(10000, [])
        self.assertIsNotNone(portfolio)

        order_list: OrderList = self.trader.doTrade(portfolio, 0.0, stock_market_data)
        self.assertIsNotNone(order_list)


