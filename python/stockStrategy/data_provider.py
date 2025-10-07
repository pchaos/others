# -*- coding=utf-8 -*-

# Modified: 2025-10-07 13:37:03

import warnings
from abc import ABC, abstractmethod
from datetime import datetime

import akshare as ak
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')


class DataProvider(ABC):
    """数据提供者抽象基类"""

    @abstractmethod
    def get_data(self, symbol, start_date, end_date):
        """获取历史数据"""
        pass

    @abstractmethod
    def get_current_price(self, symbol):
        """获取当前价格"""
        pass


class AkshareDataProvider(DataProvider):
    """Akshare数据源"""

    def get_data(self, symbol, start_date, end_date=None):
        """
        获取ETF历史数据

        Parameters:
        -----------
        symbol : str
            ETF代码，如 '159915'
        start_date : str
            开始日期，格式 'YYYYMMDD'
        end_date : str
            结束日期，格式 'YYYYMMDD'，默认为今天

        Returns:
        --------
        pd.DataFrame
            包含OHLCV数据的数据框
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")

        print(f"从Akshare获取 {symbol} 数据: {start_date} 至 {end_date}")

        try:
            # 判断市场前缀
            if symbol.startswith('15') or symbol.startswith('16'):
                market_prefix = 'sz'  # 深市
            else:
                market_prefix = 'sh'  # 沪市

            df = ak.stock_zh_a_hist(symbol="159915", period="daily", start_date=start_date, end_date=end_date)

            if not df.empty:
                # 标准化列名
                df.columns = [
                    '日期',
                    '股票代码',
                    '开盘',
                    '最高',
                    '最低',
                    '收盘',
                    '成交量',
                    '成交额',
                    '振幅',
                    '涨跌幅',
                    '涨跌额',
                    '换手率',
                ]
                df['日期'] = pd.to_datetime(df['日期'])
                df.set_index('日期', inplace=True)
                df.sort_index(inplace=True)

                # 选择需要的列
                df = df[['开盘', '最高', '最低', '收盘', '成交量']]
                df = df.astype(float)

                print(f"成功获取 {len(df)} 条数据")
                return df
            else:
                raise ValueError("获取的数据为空")

        except Exception as e:
            print(f"Akshare数据获取失败: {e}")
            print(f"{df[:-5]=}")
            # 返回模拟数据作为备选
            return self._create_fallback_data(symbol, start_date, end_date)

    def get_current_price(self, symbol):
        """
        获取当前价格

        Parameters:
        -----------
        symbol : str
            ETF代码

        Returns:
        --------
        float
            当前价格
        """
        try:
            # 使用Akshare获取实时数据
            if symbol.startswith('15') or symbol.startswith('16'):
                market_prefix = 'sz'
            else:
                market_prefix = 'sh'

            # 获取实时行情
            realtime_df = ak.fund_etf_spot_em()
            target_symbol = f"{market_prefix}{symbol}"

            # 查找对应的ETF
            target_data = realtime_df[realtime_df['代码'] == symbol]
            if not target_data.empty:
                current_price = target_data['最新价'].iloc[0]
                return float(current_price)
            else:
                print(f"无法获取 {symbol} 的实时价格，使用最后收盘价作为替代")
                # 获取历史数据并返回最后收盘价
                hist_data = self.get_data(symbol, '20200101')
                return hist_data['收盘'].iloc[-1] if not hist_data.empty else 100.0

        except Exception as e:
            print(f"获取实时价格失败: {e}，使用默认值")
            return 100.0  # 默认值

    def _create_fallback_data(self, symbol, start_date, end_date):
        """
        创建回退数据（当网络数据获取失败时使用）
        """
        print(f"为 {symbol} 生成回退数据...")

        start_date = pd.to_datetime(start_date)
        if end_date:
            end_date = pd.to_datetime(end_date)
        else:
            end_date = datetime.now()

        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        np.random.seed(42)  # 固定随机种子以便复现

        # 生成随机价格数据（模拟ETF走势）
        prices = [100]  # 起始价格
        for i in range(1, len(dates)):
            # 模拟市场波动
            change = np.random.normal(0.001, 0.02)
            new_price = max(1, prices[-1] * (1 + change))  # 价格不能低于1
            prices.append(new_price)

        df = pd.DataFrame(
            {
                '开盘': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
                '最高': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                '最低': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                '收盘': prices,
                '成交量': [np.random.randint(1000000, 5000000) for _ in prices],
            },
            index=dates,
        )

        # 添加一些趋势
        trend = np.arange(len(df)) * 0.0001
        df['收盘'] = df['收盘'] * (1 + trend)

        print(f"生成 {len(df)} 条回退数据")
        return df


class CSVDataProvider(DataProvider):
    """CSV文件数据源"""

    def __init__(self, file_path):
        self.file_path = file_path

    def get_data(self, symbol, start_date, end_date=None):
        """
        从CSV文件获取数据
        """
        print(f"从CSV文件获取 {symbol} 数据")

        try:
            df = pd.read_csv(self.file_path)

            # 假设CSV包含以下列: date, open, high, low, close, volume, symbol
            if 'date' in df.columns:
                df['日期'] = pd.to_datetime(df['date'])
            elif '日期' in df.columns:
                df['日期'] = pd.to_datetime(df['日期'])
            else:
                raise ValueError("CSV文件中未找到日期列")

            df.set_index('日期', inplace=True)
            df.sort_index(inplace=True)

            # 筛选特定标的
            if 'symbol' in df.columns:
                df = df[df['symbol'] == symbol]

            # 标准化列名
            column_mapping = {'open': '开盘', 'high': '最高', 'low': '最低', 'close': '收盘', 'volume': '成交量'}
            df.rename(columns=column_mapping, inplace=True)

            # 选择需要的列
            available_columns = [col for col in ['开盘', '最高', '最低', '收盘', '成交量'] if col in df.columns]
            df = df[available_columns]

            # 日期筛选
            start_date = pd.to_datetime(start_date)
            if end_date:
                end_date = pd.to_datetime(end_date)
                df = df[(df.index >= start_date) & (df.index <= end_date)]
            else:
                df = df[df.index >= start_date]

            print(f"从CSV成功加载 {len(df)} 条数据")
            return df

        except Exception as e:
            print(f"CSV数据获取失败: {e}")
            raise

    def get_current_price(self, symbol):
        """获取最新价格"""
        try:
            df = self.get_data(symbol, '19000101')
            return df['收盘'].iloc[-1] if not df.empty else 100.0
        except:
            return 100.0


class MockDataProvider(DataProvider):
    """模拟数据源（用于测试）"""

    def get_data(self, symbol, start_date, end_date=None):
        """生成模拟数据"""
        print(f"生成 {symbol} 的模拟数据")

        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        np.random.seed(42)

        # 生成随机价格数据
        prices = [100]
        for i in range(1, len(dates)):
            change = np.random.normal(0.001, 0.02)
            new_price = max(1, prices[-1] * (1 + change))
            prices.append(new_price)

        df = pd.DataFrame(
            {
                '开盘': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
                '最高': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                '最低': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                '收盘': prices,
                '成交量': [np.random.randint(1000000, 5000000) for _ in prices],
            },
            index=dates,
        )

        # 添加一些趋势
        trend = np.arange(len(df)) * 0.0001
        df['收盘'] = df['收盘'] * (1 + trend)
        df['开盘'] = df['收盘'] * 0.998
        df['最高'] = df['收盘'] * 1.015
        df['最低'] = df['收盘'] * 0.985

        print(f"生成 {len(df)} 条模拟数据")
        return df

    def get_current_price(self, symbol):
        """获取模拟当前价格"""
        return 100.0


# 数据源工厂
class DataProviderFactory:
    """数据源工厂类"""

    @staticmethod
    def create_provider(provider_type, **kwargs):
        """
        创建数据提供者

        Parameters:
        -----------
        provider_type : str
            数据源类型: 'akshare', 'csv', 'database', 'mock'
        **kwargs : dict
            初始化参数
        """
        providers = {'akshare': AkshareDataProvider, 'csv': CSVDataProvider, 'mock': MockDataProvider}

        if provider_type not in providers:
            raise ValueError(f"不支持的数据源类型: {provider_type}")

        return providers[provider_type](**kwargs)
