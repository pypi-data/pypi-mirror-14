from abc import ABCMeta, abstractmethod
import unittest
from strategy.bean.bean import StrategyConnectionInfo, StrategyQuoteDataRequest, StrategyRequestOrder, \
    StrategyOrderCancel, StrategyPositionStaticsResultBean, StrategyAccountDetailResultBean, \
    StrategyPositionDetailResultBean, StrategyQuoteDataResult, StrategyError

__author__ = 'Yonka'


class AbstractStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def req_handshake(self, version: str) -> StrategyError:
        pass

    @abstractmethod
    def req_login(self, conn_info: StrategyConnectionInfo) -> StrategyError:
        pass

    @abstractmethod
    def req_subscribe(self, symbol: str) -> StrategyError:
        pass

    @abstractmethod
    def req_unsubscribe(self, symbol: str) -> StrategyError:
        pass

    @abstractmethod
    def req_quota_data(self, quote_data_category: StrategyQuoteDataRequest) -> StrategyQuoteDataResult:
        pass

    @abstractmethod
    def req_account_detail(self, strategy_id: str) -> StrategyAccountDetailResultBean:
        pass

    @abstractmethod
    def req_position_detail(self, strategy_id: str) -> StrategyPositionDetailResultBean:
        pass

    @abstractmethod
    def req_position_statics(self, strategy_id: str) -> StrategyPositionStaticsResultBean:
        pass

    @abstractmethod
    def req_order(self, order_info: StrategyRequestOrder) -> str:
        pass

    @abstractmethod
    def req_cancel_order(self, cancel_order_info: StrategyOrderCancel) -> bool:
        pass


class AbstractNotifyMessageHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_notify_order_detail(self, order_detail):
        pass

    @abstractmethod
    def on_notify_trade_detail(self, trade_detail):
        pass

    @abstractmethod
    def on_notify_order_error(self, order_error):
        pass

    @abstractmethod
    def on_notify_cancel_error(self, order_cancel_error):
        pass

    @abstractmethod
    def on_notify_quote(self, data):
        pass


class TestAbsCls(unittest.TestCase):
    def test_instantiate(self):
        class TCls(AbstractStrategy):
            pass

        TCls()
