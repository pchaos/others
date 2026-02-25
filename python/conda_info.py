# -*- coding=utf-8 -*-
"""
方法1：在 base 环境中运行您的代码
conda activate base
python conda_info.py
"""
# Modified: 2026-01-16 11:36:39

import os
import sys
import time
import warnings
from contextlib import contextmanager

# 忽略 multiprocessing 的资源泄漏警告
warnings.filterwarnings("ignore", category=UserWarning, module='multiprocessing.resource_tracker')

try:
    from conda.cli import main_info
except ImportError as e:
    print("无法导入 conda 模块。请确保在已安装 conda 的 base 环境中运行此脚本。")
    sys.exit(1)


@contextmanager
def suppress_stderr():
    """
    捕获并隐藏 stderr 输出，用于屏蔽 conda 内部的错误信息。
    """
    try:
        # 尝试获取 stderr 的文件描述符
        stderr_fd = sys.stderr.fileno()
        # 保存原始 stderr
        saved_stderr_fd = os.dup(stderr_fd)

        with open(os.devnull, 'w') as devnull:
            # 将 stderr 重定向到 /dev/null
            os.dup2(devnull.fileno(), stderr_fd)
            try:
                yield
            finally:
                # 恢复原始 stderr
                os.dup2(saved_stderr_fd, stderr_fd)
                os.close(saved_stderr_fd)
    except Exception:
        # 如果无法进行底层重定向（例如在某些特殊环境中），则尝试替换 sys.stderr
        old_stderr = sys.stderr
        with open(os.devnull, 'w') as devnull:
            sys.stderr = devnull
            try:
                yield
            finally:
                sys.stderr = old_stderr


start = time.time()
# 使用 suppress_stderr 上下文管理器来隐藏 conda 内部可能抛出的异常信息
with suppress_stderr():
    info = main_info.get_info_dict()
print(f"响应时间：{time.time()-start:.2f}秒")
print(f"{info}")
