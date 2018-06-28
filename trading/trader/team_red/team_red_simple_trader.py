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

        best_stock = self.__get_best_stock(stock_market_data, self.stock_a_predictor, self.stock_b_predictor)
        if best_stock is not None:
            result.buy(best_stock, self.get_buyable_amount(current_portfolio_value, stock_market_data, best_stock))

        return result

    @staticmethod
    def get_buyable_amount(current_portfolio_value, stock_market_data, companyEnum: CompanyEnum) -> int:
        return int(current_portfolio_value / stock_market_data.get_most_recent_price(companyEnum))
    
    @staticmethod
    def __get_best_stock(stock_market_data: StockMarketData, stock_a_predictor: IPredictor, stock_b_predictor: IPredictor) -> CompanyEnum:
        deltaA = stock_a_predictor.doPredict(stock_market_data[CompanyEnum.COMPANY_A]) - stock_market_data.get_most_recent_price(CompanyEnum.COMPANY_A)
        deltaB = stock_b_predictor.doPredict(stock_market_data[CompanyEnum.COMPANY_B]) - stock_market_data.get_most_recent_price(CompanyEnum.COMPANY_B)
        if deltaA <= 0 and deltaB <= 0:
            return None
        if deltaA >= deltaB:
            return CompanyEnum.COMPANY_A
        else:
            return CompanyEnum.COMPANY_B
