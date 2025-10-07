# -*- coding=utf-8 -*-

# Modified: 2025-10-07 12:43:48

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class MovingAverageStrategy:
    """
    均线打分策略核心类
    """

    def __init__(self, data_provider, initial_capital=100000):
        """
        初始化策略

        Parameters:
        -----------
        data_provider : DataProvider
            数据提供者实例
        initial_capital : float
            初始资金
        """
        self.data_provider = data_provider
        self.initial_capital = initial_capital
        self.data = None
        self.results = None

    def load_data(self, symbol, start_date, end_date=None):
        """
        加载数据

        Parameters:
        -----------
        symbol : str
            标的代码
        start_date : str
            开始日期
        end_date : str
            结束日期
        """
        self.symbol = symbol
        self.data = self.data_provider.get_data(symbol, start_date, end_date)
        return self.data

    def calculate_technical_indicators(self, ma_periods=None):
        """
        计算技术指标
        """
        if self.data is None:
            raise ValueError("请先加载数据")

        if ma_periods is None:
            ma_periods = [5, 10, 20, 30, 60]

        df = self.data.copy()

        # 计算移动平均线
        for period in ma_periods:
            df[f'MA{period}'] = df['收盘'].rolling(period).mean()

        # 计算均线斜率
        for period in ma_periods:
            df[f'MA{period}_斜率'] = df[f'MA{period}'].pct_change(5) * 100

        # 计算成交量均线
        df['VMA20'] = df['成交量'].rolling(20).mean()

        self.data = df
        return df

    def _calculate_price_score(self, row):
        """计算价格位置得分"""
        score = 0
        close_price = row['收盘']

        if close_price > row.get('MA60', 0):
            score += 2
        elif close_price > row.get('MA20', 0):
            score += 1
        elif close_price < row.get('MA60', 0):
            score -= 2
        elif close_price < row.get('MA20', 0):
            score -= 1

        return score

    def _calculate_alignment_score(self, row):
        """计算均线排列得分"""
        score = 0
        try:
            ma5 = row.get('MA5', 0)
            ma10 = row.get('MA10', 0)
            ma20 = row.get('MA20', 0)
            ma60 = row.get('MA60', 0)

            if all(pd.notna([ma5, ma10, ma20, ma60])):
                if ma5 > ma10 > ma20 > ma60:
                    score = 2
                elif ma5 > ma60:
                    score = 1
                elif ma5 < ma10 < ma20 < ma60:
                    score = -2
                elif ma5 < ma60:
                    score = -1
        except:
            pass

        return score

    def _calculate_slope_score(self, row):
        """计算均线斜率得分"""
        score = 0
        for period in [5, 20, 60]:
            slope_col = f'MA{period}_斜率'
            slope = row.get(slope_col, 0)
            if pd.notna(slope):
                if slope > 0.5:
                    score += 1
                elif slope < -0.5:
                    score -= 1
        return score

    def _calculate_volume_score(self, row):
        """计算成交量得分"""
        score = 0
        volume = row.get('成交量', 0)
        vma20 = row.get('VMA20', 1)

        if volume > vma20 * 1.2:
            # 根据价格趋势判断成交量意义
            if row['收盘'] > row.get('MA20', row['收盘']):
                score = 1
            else:
                score = -1

        return score

    def calculate_ma_scores(self, weights=None):
        """
        计算均线综合得分

        Parameters:
        -----------
        weights : dict
            各维度权重，默认: {'price': 0.4, 'alignment': 0.3, 'slope': 0.2, 'volume': 0.1}
        """
        if self.data is None:
            raise ValueError("请先计算技术指标")

        if weights is None:
            weights = {'price': 0.4, 'alignment': 0.3, 'slope': 0.2, 'volume': 0.1}

        df = self.data.copy()
        scores = []

        for i in range(len(df)):
            row = df.iloc[i]

            # 跳过数据不足的时期
            if pd.isna(row.get('MA60', np.nan)):
                scores.append(0)
                continue

            # 计算各维度得分
            price_score = self._calculate_price_score(row)
            alignment_score = self._calculate_alignment_score(row)
            slope_score = self._calculate_slope_score(row)
            volume_score = self._calculate_volume_score(row)

            # 加权综合得分
            total_score = (
                price_score * weights['price']
                + alignment_score * weights['alignment']
                + slope_score * weights['slope']
                + volume_score * weights['volume']
            )

            scores.append(round(total_score, 2))

        df['综合得分'] = scores
        self.data = df
        return df

    def generate_trading_signals(self, buy_threshold=1.5, sell_threshold=-1.5, confirmation_days=2):
        """
        生成交易信号
        """
        if self.data is None:
            raise ValueError("请先计算均线得分")

        df = self.data.copy()

        # 原始信号
        df['原始信号'] = 0
        df['原始信号'] = np.where(df['综合得分'] >= buy_threshold, 1, np.where(df['综合得分'] <= sell_threshold, -1, 0))

        # 信号确认
        df['确认信号'] = df['原始信号'].rolling(confirmation_days).mean()
        df['交易信号'] = np.where(df['确认信号'] >= 0.5, 1, np.where(df['确认信号'] <= -0.5, -1, 0))

        # 持仓状态
        df['持仓'] = df['交易信号'].replace(0, method='ffill').fillna(0)

        self.data = df
        return df

    def run_backtest(self, transaction_cost=0.001):
        """
        运行回测
        """
        if self.data is None:
            raise ValueError("请先生成交易信号")

        df = self.data.copy()

        # 计算收益率
        df['日收益率'] = df['收盘'].pct_change()
        df['策略收益率'] = df['持仓'].shift(1) * df['日收益率']

        # 考虑交易成本
        df['交易成本'] = abs(df['持仓'].diff().fillna(0)) * transaction_cost
        df['净收益率'] = df['策略收益率'] - df['交易成本']

        # 计算累计收益
        df['基准累计收益'] = (1 + df['日收益率'].fillna(0)).cumprod()
        df['策略累计收益'] = (1 + df['净收益率'].fillna(0)).cumprod()

        # 计算资金曲线
        df['基准资金'] = self.initial_capital * df['基准累计收益']
        df['策略资金'] = self.initial_capital * df['策略累计收益']

        # 交易记录
        df['交易动作'] = df['持仓'].diff().fillna(0)

        self.results = df
        return df

    def calculate_performance_metrics(self):
        """计算绩效指标"""
        if self.results is None:
            raise ValueError("请先运行回测")

        df = self.results.dropna()

        if len(df) == 0:
            return {}

        # 基本指标
        total_return = df['策略累计收益'].iloc[-1] - 1
        benchmark_return = df['基准累计收益'].iloc[-1] - 1
        excess_return = total_return - benchmark_return

        # 年化指标
        days = (df.index[-1] - df.index[0]).days
        annual_return = (1 + total_return) ** (365 / days) - 1 if days > 0 else 0

        # 风险指标
        volatility = df['净收益率'].std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0

        # 回撤分析
        cumulative_max = df['策略资金'].cummax()
        drawdown = (df['策略资金'] - cumulative_max) / cumulative_max
        max_drawdown = drawdown.min()

        # 交易分析
        trades = df[df['交易动作'] != 0]
        trade_count = len(trades)

        metrics = {
            '总收益率': total_return,
            '基准收益率': benchmark_return,
            '超额收益': excess_return,
            '年化收益率': annual_return,
            '年化波动率': volatility,
            '夏普比率': sharpe_ratio,
            '最大回撤': max_drawdown,
            '总交易次数': trade_count,
            '数据周期': days,
            '最终资金': df['策略资金'].iloc[-1],
        }

        return metrics

    def get_formatted_performance(self):
        """获取格式化的绩效报告"""
        metrics = self.calculate_performance_metrics()

        if not metrics:
            return "无有效绩效数据"

        formatted = {
            '总收益率': f"{metrics['总收益率']:.2%}",
            '基准收益率': f"{metrics['基准收益率']:.2%}",
            '超额收益': f"{metrics['超额收益']:.2%}",
            '年化收益率': f"{metrics['年化收益率']:.2%}",
            '年化波动率': f"{metrics['年化波动率']:.2%}",
            '夏普比率': f"{metrics['夏普比率']:.2f}",
            '最大回撤': f"{metrics['最大回撤']:.2%}",
            '总交易次数': metrics['总交易次数'],
            '数据周期(天)': metrics['数据周期'],
            '最终资金': f"¥{metrics['最终资金']:,.0f}",
        }

        return formatted

    def get_current_signal(self):
        """获取最新交易信号"""
        if self.results is None:
            return None

        latest = self.results.iloc[-1]

        return {
            '日期': latest.name.strftime('%Y-%m-%d'),
            '价格': latest['收盘'],
            '综合得分': latest['综合得分'],
            '持仓': latest['持仓'],
            '信号': '买入' if latest['交易信号'] > 0 else '卖出' if latest['交易信号'] < 0 else '持有',
        }
