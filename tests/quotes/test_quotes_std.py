import unittest
from datetime import datetime

import pytest

from mootdx.consts import MARKET_SH
from mootdx.exceptions import MootdxValidationException
from mootdx.logger import logger
from mootdx.quotes import Quotes


class TestStdQuotes(unittest.TestCase):
    client = None

    # 初始化工作
    def setup_class(self):
        self.client = Quotes.factory(market='std', timeout=10, verbose=2)  # 标准市场
        logger.debug('初始化工作')

    # 退出清理工作
    def teardown_class(self):
        self.client.client.close()
        del self.client
        logger.debug('退出清理工作')

    def test_quotes(self):
        data = self.client.quotes(symbol='600036')
        self.assertEqual(data.empty, False)

        data = self.client.quotes(symbol='688597')
        self.assertEqual(data.empty, False)

        data = self.client.quotes(symbol=['600036', '600016'])
        self.assertEqual(data.empty, False)

    def test_bars(self):
        data = self.client.bars(symbol='600036', frequency=9, offset=10)
        self.assertEqual(data.empty, False)

    def test_index(self):
        data = self.client.index(frequency=9, market=MARKET_SH, symbol='000001', start=1, offset=2)
        self.assertEqual(data.empty, False)

    def test_minute(self):
        today = datetime.now().strftime('%Y%m%d')
        data0 = self.client.minute(symbol='000001')
        data1 = self.client.minutes(symbol='000001', date=today)
        print(today)
        print(data0)
        print(data1)

        self.assertTrue(data1.equals(data0))

    def test_minutes(self):
        data = self.client.minutes(symbol='000001', date='20171010')
        self.assertEqual(data.empty, False)

    def test_transaction(self):
        data = self.client.transaction(symbol='600036', start=0, offset=10)
        self.assertEqual(data.empty, False)

    def test_transactions(self):
        data = self.client.transactions(symbol='600036', start=0, offset=10, date='20170209')
        self.assertEqual(data.empty, False)

    def test_F10C(self):
        data = self.client.F10C(symbol='000001')
        self.assertTrue(data)

    def test_F10(self):
        data = self.client.F10(symbol='000001', name='公司概况')
        self.assertTrue(data)

    def test_xdxr(self):
        data = self.client.xdxr(symbol='600036')
        self.assertEqual(data.all().empty, False)

    def test_k(self):
        data = self.client.k(symbol='000001', begin='2019-07-03', end='2019-07-10')
        self.assertEqual(data.empty, False)

    def test_get_k_data(self):
        data = self.client.get_k_data(code='600036', start_date='2007-07-03', end_date='2019-07-10')
        self.assertEqual(data.empty, False)

    def test_block(self):
        data = self.client.block()
        self.assertEqual(data.empty, False)

    def test_finance(self):
        data = self.client.finance(symbol='000001')
        self.assertEqual(data.empty, False)

    def test_retry_last_value(self):
        data = self.client.minutes('159995', '20200130')
        logger.debug(f'result => {data}')
        self.assertEqual(data.empty, True)

    def test_bj_quotes(self):
        # todo 无法使用 minutes, F10, F10C, transactions
        # data = self.client.minute(symbol='430090')
        # self.assertEqual(data.empty, False)

        data = self.client.bars(symbol='430090')
        self.assertEqual(data.empty, False)

        data = self.client.transaction(symbol='430090')
        self.assertEqual(data.empty, False)


class TestStdRaises(unittest.TestCase):
    client = None

    # 初始化工作
    def setup_class(self):
        self.client = Quotes.factory(market='std', timeout=10, verbose=2)  # 标准市场

    def test_stock_count_raises(self):
        with pytest.raises(MootdxValidationException) as e:
            self.client.stock_count(3)

        exec_msg = e.value.args[0]
        assert exec_msg == '市场代码错误'

    def test_stocks_raises(self):
        with pytest.raises(MootdxValidationException) as e:
            self.client.stocks(2)

        exec_msg = e.value.args[0]
        assert exec_msg == '市场代码错误, 目前只支持沪深市场'
