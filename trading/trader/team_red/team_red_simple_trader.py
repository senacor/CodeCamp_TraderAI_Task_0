"""
Created on 08.11.2017

@author: jtymoszuk
"""
from model.CompanyEnum import CompanyEnum
from model.Portfolio import Portfolio
from model.StockMarketData import StockMarketData
from model.ITrader import ITrader
from model.Order import OrderList
from model.IPredictor import IPredictor

class TeamRedSimpleTrader(ITrader):
    """
    Simple Trader generates Order based on simple logic, input data and prediction from NN-Engine
    """

    def __init__(self, stock_a_predictor: IPredictor, stock_b_predictor: IPredictor):
        """
        Constructor
        """
        self.stock_a_predictor = stock_a_predictor
        self.stock_b_predictor = stock_b_predictor

    def doTrade(self, portfolio: Portfolio, current_portfolio_value: float,
                stock_market_data: StockMarketData) -> OrderList:
        """
        Generate action to be taken on the "stock market"
    
        Args:
          portfolio : current Portfolio of this trader
          current_portfolio_value : value of Portfolio at given Momemnt
          stock_market_data : StockMarketData for evaluation

        Returns:
          A OrderList instance, may be empty never None
        """

        result = OrderList()
        """
        Sell Everything
        """
        result.sell(CompanyEnum.COMPANY_A, portfolio.get_amount(CompanyEnum.COMPANY_A))
        result.sell(CompanyEnum.COMPANY_B, portfolio.get_amount(CompanyEnum.COMPANY_B))

        if (self.stock_a_predictor.doPredict(stock_market_data[CompanyEnum.COMPANY_A])
                >self.stock_b_predictor.doPredict(stock_market_data[CompanyEnum.COMPANY_B])):
            # TODO: Calculate Buyable Amount for A
          result.buy(CompanyEnum.COMPANY_A, 10)
        else:
            # TODO: Calculate Buyable Amount for B
          result.buy(CompanyEnum.COMPANY_B, 10)


        return result
