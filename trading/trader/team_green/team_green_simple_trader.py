"""
Created on 08.11.2017

@author: jtymoszuk
"""
from model.CompanyEnum import CompanyEnum
from model.IPredictor import IPredictor
from model.ITrader import ITrader
from model.Order import OrderList
from model.Portfolio import Portfolio
from model.StockMarketData import StockMarketData


class TeamGreenSimpleTrader(ITrader):
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

        company_a_value = stock_market_data.get_most_recent_price(CompanyEnum.COMPANY_A)
        company_b_value = stock_market_data.get_most_recent_price(CompanyEnum.COMPANY_B)
        cash = portfolio.cash
        result = OrderList()

        result.sell(CompanyEnum.COMPANY_A, portfolio.get_amount(CompanyEnum.COMPANY_A))
        cash += portfolio.get_amount(CompanyEnum.COMPANY_A) * company_a_value
        result.sell(CompanyEnum.COMPANY_B, portfolio.get_amount(CompanyEnum.COMPANY_B))
        cash += portfolio.get_amount(CompanyEnum.COMPANY_B) * company_b_value

        company_a_prediction = self.stock_a_predictor.doPredict(stock_market_data.__getitem__(CompanyEnum.COMPANY_A))
        company_a_difference = company_a_prediction - company_a_value
        company_b_prediction = self.stock_b_predictor.doPredict(stock_market_data.__getitem__(CompanyEnum.COMPANY_B))
        company_b_difference = company_b_prediction - company_b_value

        if max(company_a_difference, company_b_difference) > 0:
                bought_a_shares = int(cash / company_a_value)
                company_a_gain = bought_a_shares * company_a_difference
                bought_b_shares = int(cash / company_b_value)
                company_b_gain = bought_b_shares * company_b_difference
                if company_a_gain > company_b_gain:
                    result.buy(CompanyEnum.COMPANY_A, bought_a_shares)
                    remainingCash = cash - bought_a_shares * company_a_value
                    result.buy(CompanyEnum.COMPANY_B, int(remainingCash / company_b_value))
                else:
                    result.buy(CompanyEnum.COMPANY_B, bought_b_shares)
                    remainingCash = cash - bought_b_shares * company_b_value
                    result.buy(CompanyEnum.COMPANY_A, int(remainingCash / company_a_value))

        return result
