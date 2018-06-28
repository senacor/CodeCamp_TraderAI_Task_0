"""
Created on 08.11.2017

@author: jtymoszuk
"""
from model.Portfolio import Portfolio
from model.StockMarketData import StockMarketData
from model.ITrader import ITrader
from model.Order import OrderList
from model.IPredictor import IPredictor

from model.CompanyEnum import CompanyEnum

import math


class TeamBlueSimpleTrader(ITrader):
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

        # TODO: implement trading logic
        target_price_company_a = self.stock_a_predictor.doPredict(stock_market_data[CompanyEnum.COMPANY_A])
        current_price_company_a = stock_market_data.get_most_recent_price(CompanyEnum.COMPANY_A)

        target_price_company_b = self.stock_b_predictor.doPredict(stock_market_data[CompanyEnum.COMPANY_B])
        current_price_company_b = stock_market_data.get_most_recent_price(CompanyEnum.COMPANY_B)


        future_factor_company_a = target_price_company_a/current_price_company_a
        future_factor_company_b = target_price_company_b/current_price_company_b

        if future_factor_company_a<=1 and future_factor_company_b<=1:
            #beide gehen runter oder bleiben gleich
            result.sell(CompanyEnum.COMPANY_A, portfolio.get_amount(CompanyEnum.COMPANY_A))
            result.sell(CompanyEnum.COMPANY_B, portfolio.get_amount(CompanyEnum.COMPANY_B))

        else:

            if future_factor_company_a > future_factor_company_b:
                buy_company = CompanyEnum.COMPANY_A
                sell_company = CompanyEnum.COMPANY_B
                sell_factor = future_factor_company_b
            else:
                buy_company = CompanyEnum.COMPANY_B
                sell_company = CompanyEnum.COMPANY_A
                sell_factor = future_factor_company_a

            # Verkaufe Stock mit geringerer Performance
            amout_sell = portfolio.get_amount(sell_company)
            result.sell(sell_company, amout_sell)

            # Kaufe Stock mit höherer Performance
            current_price_sell_company = stock_market_data.get_most_recent_price(sell_company)
            current_price_buy_company = stock_market_data.get_most_recent_price(buy_company)
            cash_after_sell = portfolio.cash + portfolio.get_amount(sell_company)*current_price_sell_company
            amount_buy = math.floor(cash_after_sell/ current_price_buy_company)

            result.buy(buy_company, amount_buy)

            # Kaufe Zusatz-Stock von schlechterer Aktie
            if sell_factor > 1:
                cash_after_buy = cash_after_sell - amount_buy*current_price_buy_company
                amount_buy_2 = math.floor(cash_after_buy/ current_price_sell_company)
                if amount_buy_2>0:
                    print(f"YEAH!")
                    result.buy(sell_company, amount_buy_2)


            # print('--')
            # print(portfolio)
            # print([amout_sell, current_price_sell_company, portfolio.cash, cash_after_sell, current_price_buy_company,
            #        amount_buy])
            # print(result)




        # Erste Version: nur mit Company A
        # if target_price_company_a > current_price_company_a and portfolio.cash > 0:
        #     result.buy(CompanyEnum.COMPANY_A, math.floor(portfolio.cash/current_price_company_a))
        # else:
        #     result.sell(CompanyEnum.COMPANY_A, portfolio.get_amount(CompanyEnum.COMPANY_A))





        return result
