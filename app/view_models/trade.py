"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: trade.py
@time: 2018/12/9 16:31
@desc:
"""
from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, trades):
        self.total = 0
        self.trades = []
        self._parse(trades)

    def _parse(self, trades):
        self.total = len(trades)
        self.trades = [self._map_to_trade(gift) for gift in trades]

    def _map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )
# 心愿清单的viewmodel
class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []

        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list

        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(trade.book),
            'id': trade.id
        }
        return r











