# -*- coding=utf-8 -*-

# Modified: 2025-10-07 12:42:25
import matplotlib.pyplot as plt
import pandas as pd


class StrategyVisualizer:
    """策略可视化工具"""

    @staticmethod
    def plot_strategy(strategy, save_path=None):
        """绘制策略图表"""
        if strategy.results is None:
            raise ValueError("请先运行策略回测")

        df = strategy.results.dropna()

        fig, axes = plt.subplots(3, 1, figsize=(15, 12))

        # 价格和均线
        axes[0].plot(df.index, df['收盘'], label='价格', linewidth=1, color='black')
        axes[0].plot(df.index, df['MA20'], label='MA20', alpha=0.7)
        axes[0].plot(df.index, df['MA60'], label='MA60', alpha=0.7)

        # 标记交易信号
        buy_signals = df[df['交易动作'] > 0]
        sell_signals = df[df['交易动作'] < 0]

        axes[0].scatter(buy_signals.index, buy_signals['收盘'], color='red', marker='^', s=100, label='买入', zorder=5)
        axes[0].scatter(
            sell_signals.index, sell_signals['收盘'], color='green', marker='v', s=100, label='卖出', zorder=5
        )

        axes[0].set_title(f'{strategy.symbol} - 价格走势与交易信号', fontsize=14)
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # 均线得分
        axes[1].plot(df.index, df['综合得分'], label='综合得分', color='purple', linewidth=1)
        axes[1].axhline(y=1.5, color='red', linestyle='--', alpha=0.7, label='买入阈值')
        axes[1].axhline(y=-1.5, color='green', linestyle='--', alpha=0.7, label='卖出阈值')
        axes[1].axhline(y=0, color='gray', linestyle='-', alpha=0.5)
        axes[1].set_title('均线综合得分', fontsize=14)
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        # 资金曲线
        axes[2].plot(df.index, df['策略资金'], label='策略资金', linewidth=2)
        axes[2].plot(df.index, df['基准资金'], label='基准资金', linestyle='--', alpha=0.8)
        axes[2].set_title('资金曲线对比', fontsize=14)
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        axes[2].set_ylabel('资金规模 (元)')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()
