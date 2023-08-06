from __future__ import absolute_import
from abc import ABCMeta, abstractmethod
import unittest

__author__ = u'Yonka'


class AbstractStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def req_login(self, conn_info):
        pass

    @abstractmethod
    def req_subscribe(self, symbol):
        pass

    @abstractmethod
    def req_unsubscribe(self, symbol):
        pass

    @abstractmethod
    def req_quota_data(self, quote_data_category):
        pass

    @abstractmethod
    def req_account_detail(self, strategy_id):
        pass

    @abstractmethod
    def req_position_statics(self, strategy_id):
        pass

    @abstractmethod
    def req_order_list(self, strategy_id):
        pass

    @abstractmethod
    def req_order(self, order_info):
        pass

    @abstractmethod
    def req_cancel_order(self, cancel_order_info):
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
